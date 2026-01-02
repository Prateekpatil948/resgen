"""
Django views for Resume Builder application.
Handles:
- Auth
- Resume CRUD
- Template preview
- Resume analysis (Grok)
- AI suggestions
- PDF download
"""

from types import SimpleNamespace
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
import json
import pdfkit  # type: ignore
import PyPDF2  # type: ignore

from .models import Profile
from .forms import ExtendedUserCreationForm
from .analyse_ai import evaluate_resume_with_groq

from .ai_suggestions import generate_ai_editing_suggestions


# ======================
# AUTHENTICATION
# ======================

def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                return redirect("welcome")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def custom_logout(request):
    logout(request)
    return redirect("welcome")


def signup(request):
    if request.method == "POST":
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, email=user.email)
            login(request, user)
            return redirect("welcome")
    else:
        form = ExtendedUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


# ======================
# PUBLIC PAGES
# ======================

def home(request):
    return render(request, "pdf/home.html")


def welcome_page(request):
    return render(request, "pdf/welcome.html")


def generate_options(request):
    return render(request, "pdf/generate_options.html")


def template_preview(request, template_id="1"):
    templates = [
        {"id": "1", "name": "Classic"},
        {"id": "2", "name": "Modern"},
        {"id": "3", "name": "Professional"},
        {"id": "4", "name": "Elegant"},
        {"id": "5", "name": "Creative"},
    ]

    if template_id not in [t["id"] for t in templates]:
        template_id = "1"

    return render(request, "pdf/template_preview.html", {
        "templates": templates,
        "selected_template": template_id,
        "selected_template_name": next(
            t["name"] for t in templates if t["id"] == template_id
        )
    })


# ======================
# RESUME CREATE / EDIT
# ======================

@login_required(login_url="login")
def generate_resume(request):
    template_choice = request.GET.get("template", "1")
    profile_id = request.GET.get("profile_id")

    def collect(prefix):
        data = {}
        for k, v in request.POST.items():
            if k.startswith(prefix):
                try:
                    _, idx, field = k.split("_", 2)
                    data.setdefault(idx, {})[field] = v
                except ValueError:
                    pass
        return [data[k] for k in sorted(data)]

    if request.method == "POST":
        education = collect("education")
        experience = collect("experience")
        projects = collect("project")

        if profile_id:
            profile = get_object_or_404(Profile, id=profile_id, user=request.user)
            profile.first_name = request.POST.get("first_name", "")
            profile.last_name = request.POST.get("last_name", "")
            profile.email = request.POST.get("email", "")
            profile.phone = request.POST.get("phone", "")
            profile.linkedin_id = request.POST.get("linkedin", "")
            profile.summary = request.POST.get("objective", "")
            profile.skills = request.POST.get("skills", "")
            profile.certifications = request.POST.get("certifications", "")
            profile.education = education
            profile.experience = experience
            profile.projects = projects
            profile.template_choice = request.POST.get("template_choice", "1")
            profile.save()
        else:
            profile = Profile.objects.create(
                user=request.user,
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                email=request.POST["email"],
                phone=request.POST["phone"],
                linkedin_id=request.POST.get("linkedin", ""),
                summary=request.POST.get("objective", ""),
                skills=request.POST.get("skills", ""),
                certifications=request.POST.get("certifications", ""),
                education=education,
                experience=experience,
                projects=projects,
                template_choice=request.POST.get("template_choice", "1"),
            )

        return JsonResponse({
            "success": True,
            "profile_id": profile.id,
            "preview_url": reverse("preview_resume", args=[profile.id]),
        })

    if profile_id:
        profile = get_object_or_404(Profile, id=profile_id, user=request.user)
        return render(request, "pdf/generate.html", {
            "profile": profile,
            "is_edit": True,
            "template_choice": template_choice,
        })

    return render(request, "pdf/generate.html", {
        "is_edit": False,
        "template_choice": template_choice,
    })


# ======================
# PREVIEW / DOWNLOAD
# ======================

@login_required
def preview_resume(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    return render(request, "pdf/preview.html", {"profile": profile})


@login_required
def preview_resume_content(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    return render(request, "pdf/preview_content.html", {"profile": profile})


@login_required
def download_resume(request, id):
    profile = get_object_or_404(Profile, id=id, user=request.user)
    html = render_to_string("pdf/template1.html", {"profile": profile})
    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="{profile.first_name}_resume.pdf"'
    )
    return response


@login_required
def list_profiles(request):
    profiles = Profile.objects.filter(user=request.user).order_by("-id")
    paginator = Paginator(profiles, 5)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "pdf/list.html", {"page_obj": page})


@login_required
def delete_resume(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    profile.delete()
    return redirect("list")


# ======================
# AI ANALYSIS (GROK)
# ======================

@login_required
def analyze_uploaded_resume(request):
    if request.method == "POST":
        resume_file = request.FILES.get("resume_file")
        job_description = request.POST.get("job_description", "")

        reader = PyPDF2.PdfReader(resume_file)
        resume_text = "".join(p.extract_text() or "" for p in reader.pages)

        score_data = evaluate_resume_with_groq(resume_text, job_description)

        temp_profile = SimpleNamespace(
            score=score_data.get("overall_score", 0),
            feedback=score_data.get("summary", ""),
            strengths=score_data.get("strengths", []),
            weaknesses=score_data.get("weaknesses", []),
            suggestions=score_data.get("suggestions", []),
        )

        return render(request, "pdf/resume_score_result.html", {
            "profile": temp_profile,
            "score_data": score_data,
            "from_upload": True,
        })

    return render(request, "pdf/resume_score.html")


@login_required
def analyze_profile_resume(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)

    resume_text = f"""
    Name: {profile.first_name} {profile.last_name}
    Summary: {profile.summary}
    Skills: {profile.skills}
    Education: {json.dumps(profile.education)}
    Experience: {json.dumps(profile.experience)}
    Projects: {json.dumps(profile.projects)}
    """

    score_data = evaluate_resume_with_groq(resume_text)

    profile.score = score_data.get("overall_score", 0)
    profile.feedback = score_data.get("summary", "")
    profile.strengths = score_data.get("strengths", [])
    profile.weaknesses = score_data.get("weaknesses", [])
    profile.suggestions = score_data.get("suggestions", [])
    profile.last_analyzed = timezone.now()
    profile.save()

    return render(request, "pdf/resume_score_result.html", {
        "profile": profile,
        "score_data": score_data,
        "from_upload": False,
    })


# ======================
# AI SUGGESTIONS
# ======================

@csrf_exempt
@require_POST
def get_ai_suggestions(request):
    data = json.loads(request.body)
    profile_id = data.get("profile_id")
    resume_text = data.get("resume_text", "")

    if profile_id:
        profile = Profile.objects.get(id=profile_id)
        analysis_data = {
            "weaknesses": profile.weaknesses,
            "suggestions": profile.suggestions,
            "score_metrics": profile.score_metrics,
        }
    else:
        analysis_data = {}

    enhanced = generate_ai_editing_suggestions(analysis_data, resume_text)

    return JsonResponse({
        "success": True,
        "ai_suggestions": enhanced.get("ai_suggestions_for_edit", []),
    })
