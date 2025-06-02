"""
Django views for Resume Builder application.

This module handles all view logic including:
- User authentication (login, logout, signup)
- Resume generation and management
- Resume analysis and AI suggestions
- PDF generation and downloads
"""

from types import SimpleNamespace
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseServerError, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.core.serializers.json import DjangoJSONEncoder
import json
import pdfkit  # type: ignore
import PyPDF2  # type: ignore

from .models import Profile
from .forms import ExtendedUserCreationForm
from .analyse_ai import evaluate_resume_with_gemini
from .ai_suggestions import generate_ai_editing_suggestions


# ======================
# Authentication Views
# ======================

def custom_login(request):
    """Handle user login with Django's authentication system."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('welcome')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def custom_logout(request):
    """Handle user logout."""
    logout(request)
    return redirect('welcome')


def signup(request):
    """Handle new user registration with extended profile information."""
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create associated profile
            Profile.objects.create(
                user=user,
                email=user.email,
            )
            
            login(request, user)
            return redirect('welcome')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# ======================
# Public Views
# ======================

def home(request):
    """Render the home page."""
    return render(request, 'pdf/home.html')


def welcome_page(request):
    """Render the welcome page with features and testimonials."""
    context = {
        'features': [
            'Create professional resumes in minutes',
            'Multiple template options',
            'Download as PDF',
            'AI-powered resume analysis',
            'User-friendly interface'
        ],
        'testimonials': [
            {'name': 'John D.', 'quote': 'Landed my dream job thanks to the resume I created here!'},
            {'name': 'Sarah M.', 'quote': 'The templates are modern and professional.'}
        ]
    }
    return render(request, 'pdf/welcome.html', context)


def generate_options(request):
    """Display options for resume generation."""
    return render(request, 'pdf/generate_options.html')


def template_preview(request, template_id='1'):
    """Preview available resume templates."""
    templates = [
        {'id': '1', 'name': 'Classic', 'image': 'images/template1-thumb.png'},
        {'id': '2', 'name': 'Modern', 'image': 'images/template2-thumb.png'},
        {'id': '3', 'name': 'Professional', 'image': 'images/template3-thumb.png'},
        {'id': '4', 'name': 'Elegant', 'image': 'images/template4-thumb.png'},
        {'id': '5', 'name': 'Creative', 'image': 'images/template5-thumb.png'},
    ]
    
    if template_id not in [t['id'] for t in templates]:
        template_id = '1'
    
    return render(request, 'pdf/template_preview.html', {
        'templates': templates,
        'selected_template': template_id,
        'selected_template_name': next(t['name'] for t in templates if t['id'] == template_id)
    })


# ======================
# Resume Management Views
# ======================

@login_required(login_url='login')
def generate_resume(request):
    """
    Handle resume creation and editing.
    
    GET: Display the resume form with selected template
    POST: Save resume data to profile
    """
    template_choice = request.GET.get('template', '1')
    profile_id = request.GET.get('profile_id')
    
    if request.method == 'POST':
        try:
            def process_dynamic_fields(prefix):
                """Helper to process dynamic form fields (education, experience, projects)."""
                fields = {}
                for key in request.POST:
                    if key.startswith(prefix):
                        try:
                            _, index, field_name = key.split('_', 2)
                            if index not in fields:
                                fields[index] = {}
                            fields[index][field_name] = request.POST[key]
                        except ValueError:
                            continue
                return [fields[key] for key in sorted(fields.keys())]

            education = process_dynamic_fields('education')
            experience = process_dynamic_fields('experience')
            projects = process_dynamic_fields('project')

            if profile_id:
                # Update existing profile
                profile = get_object_or_404(Profile, pk=profile_id, user=request.user)
                profile.first_name = request.POST.get('first_name', '')
                profile.last_name = request.POST.get('last_name', '')
                profile.email = request.POST.get('email', '')
                profile.phone = request.POST.get('phone', '')
                profile.linkedin_id = request.POST.get('linkedin', '')
                profile.summary = request.POST.get('objective', '')
                profile.skills = request.POST.get('skills', '')
                profile.certifications = request.POST.get('certifications', '')
                profile.education = education
                profile.experience = experience
                profile.projects = projects
                profile.template_choice = request.POST.get('template_choice', '1')
                profile.save()
            else:
                # Create new profile
                profile = Profile.objects.create(
                    user=request.user,
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['email'],
                    phone=request.POST['phone'],
                    linkedin_id=request.POST.get('linkedin', ''),
                    summary=request.POST.get('objective', ''),
                    skills=request.POST.get('skills', ''),
                    certifications=request.POST.get('certifications', ''),
                    education=education,
                    experience=experience,
                    projects=projects,
                    template_choice=request.POST.get('template_choice', '1')
                )

            return JsonResponse({
                'success': True,
                'profile_id': profile.id,
                'template': request.POST.get('template_choice', '1'),
                'preview_url': reverse('preview_content', kwargs={'profile_id': profile.id}),
                'message': 'Resume saved successfully'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)

    # Handle GET request
    if profile_id:
        profile = get_object_or_404(Profile, pk=profile_id, user=request.user)
        return render(request, 'pdf/generate.html', {
            'template_choice': template_choice,
            'is_edit': True,
            'profile': profile
        })
    
    return render(request, 'pdf/generate.html', {
        'template_choice': template_choice,
        'is_edit': False
    })


@login_required
def preview_resume(request, profile_id):
    """Preview resume with selected template."""
    try:
        profile = get_object_or_404(Profile, pk=profile_id, user=request.user)
        template = request.GET.get('template', profile.template_choice)
        
        if template != profile.template_choice:
            profile.template_choice = template
            profile.save()
        
        # Normalize education data keys
        normalized_education = [
            {key.replace('/', '_'): value for key, value in edu.items()}
            for edu in profile.education
        ]
        
        context = {
            'user_profile': profile,
            'education': normalized_education,
            'experience': profile.experience,
            'projects': profile.projects,
            'current_template': template
        }
        
        # Check if this is a request for the template-only view
        if request.GET.get('template_only'):
            template_mapping = {
                '1': 'pdf/template1.html',
                '2': 'pdf/template2.html',
                '3': 'pdf/template3.html',
                '4': 'pdf/template4.html',
                '5': 'pdf/template5.html',
            }
            return render(request, template_mapping[template], context)
        
        return render(request, 'pdf/preview.html', context)
    except Exception as e:
        return HttpResponseServerError(str(e))


@login_required
def preview_resume_content(request, profile_id):
    """Render resume content for modal preview."""
    template = request.GET.get('template', '1')
    profile = get_object_or_404(Profile, pk=profile_id, user=request.user)
    
    normalized_education = [
        {key.replace('/', '_'): value for key, value in edu.items()}
        for edu in profile.education
    ]
    
    context = {
        'user_profile': profile,
        'education': normalized_education,
        'experience': profile.experience,
        'projects': profile.projects,
        'is_modal': True
    }
    
    template_mapping = {
        '1': 'pdf/template1.html',
        '2': 'pdf/template2.html',
        '3': 'pdf/template3.html',
    }
    
    return render(request, template_mapping.get(template, 'pdf/template1.html'), context)


@login_required
def download_resume(request, id):
    """Generate and download resume as PDF."""
    try:
        profile = get_object_or_404(Profile, pk=id, user=request.user)
        template = request.GET.get('template', profile.template_choice)
        
        template_mapping = {
            '1': 'pdf/template1.html',
            '2': 'pdf/template2.html',
            '3': 'pdf/template3.html',
            '4': 'pdf/template4.html',
            '5': 'pdf/template5.html',
        }
        template_name = template_mapping.get(template, 'pdf/template1.html')
        
        # Normalize data for template
        def normalize_data(data):
            return [
                {key.lower().replace(' ', '_').replace('-', '_'): value 
                 for key, value in item.items()}
                for item in data
            ]
        
        context = {
            'user_profile': profile,
            'education': normalize_data(profile.education),
            'experience': normalize_data(profile.experience),
            'projects': normalize_data(profile.projects),
            'is_pdf': True
        }
        
        html = render_to_string(template_name, context)
        
        options = {
            'page-size': 'Letter',
            'encoding': "UTF-8",
            'enable-local-file-access': '',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'quiet': ''
        }
        
        pdf = pdfkit.from_string(html, False, options=options)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"{profile.first_name}_{profile.last_name}_resume.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
        
    except Exception as e:
        return HttpResponse(f"PDF generation error: {str(e)}", status=500)


@login_required
def list_profiles(request):
    """List all user's resume profiles with pagination."""
    profiles = Profile.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(profiles, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pdf/list.html', {'page_obj': page_obj})


@login_required
def delete_resume(request, profile_id):
    """Delete a resume profile."""
    if request.method == 'POST':
        profile = get_object_or_404(Profile, id=profile_id, user=request.user)
        profile.delete()
        return redirect('list')
    return redirect('list')


# ======================
# Resume Analysis Views
# ======================

# @login_required
def analyze_uploaded_resume(request):
    """Analyze uploaded PDF resume with AI."""
    if request.method == 'POST':
        resume_file = request.FILES.get('resume_file')
        job_description = request.POST.get('job_description', '')
        
        if not resume_file:
            return render(request, 'pdf/resume_score.html', {
                'error': 'Please upload a PDF file'
            })

        try:
            # Extract text from PDF
            pdf_reader = PyPDF2.PdfReader(resume_file)
            resume_text = "".join(page.extract_text() or "" for page in pdf_reader.pages)
            
            # Get AI analysis
            score_data = evaluate_resume_with_gemini(resume_text, job_description)

            # Process analysis results
            if isinstance(score_data.get('strengths'), str):
                score_data['strengths'] = [s.strip() for s in score_data['strengths'].split(',') if s.strip()]
            if isinstance(score_data.get('weaknesses'), str):
                score_data['weaknesses'] = [w.strip() for w in score_data['weaknesses'].split(',') if w.strip()]

            # Store in session
            request.session.update({
                'weaknesses': score_data.get('weaknesses', []),
                'suggestions': score_data.get('suggestions', []),
                'score_metrics': score_data.get('score_metrics', {}),
                'resume_text': resume_text
            })

            temp_profile = SimpleNamespace(
                id=None,
                first_name="Uploaded",
                last_name="Resume",
                email="",
                score=score_data.get('overall_score', 0),
                feedback=score_data.get('summary', 'No feedback available'),
                score_metrics=score_data.get('score_metrics', {}),
                last_analyzed=timezone.now(),
                strengths=score_data.get('strengths', []),
                weaknesses=score_data.get('weaknesses', []),
                suggestions=score_data.get('suggestions', []),
                resume_text=resume_text
            )
            
            return render(request, 'pdf/resume_score_result.html', {
                'profile': temp_profile,
                'score_data': score_data,
                'from_upload': True
            })
            
        except Exception as e:
            return render(request, 'pdf/resume_score.html', {
                'error': f"Error processing PDF: {str(e)}"
            })
    
    return render(request, 'pdf/resume_score.html')


# @login_required
def analyze_profile_resume(request, profile_id):
    """Analyze existing profile resume with AI."""
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    
    if request.method == 'POST':
        job_description = request.POST.get('job_description', '')
        
        resume_text = f"""
        Name: {profile.first_name} {profile.last_name}
        Summary: {profile.summary}
        Skills: {profile.skills}
        Education: {json.dumps(profile.education)}
        Experience: {json.dumps(profile.experience)}
        Projects: {json.dumps(profile.projects)}
        """
        
        score_data = evaluate_resume_with_gemini(resume_text, job_description)

        # Update profile with analysis results
        profile.score = score_data.get('overall_score', 0)
        profile.feedback = score_data.get('summary', 'No feedback available')
        profile.score_metrics = score_data.get('score_metrics', {})
        profile.strengths = score_data.get('strengths', [])
        profile.weaknesses = score_data.get('weaknesses', [])
        profile.suggestions = score_data.get('suggestions', [])
        profile.last_analyzed = timezone.now()
        profile.save()
        
        return render(request, 'pdf/resume_score_result.html', {
            'profile': profile,
            'score_data': score_data,
            'from_upload': False
        })
    
    return render(request, 'pdf/resume_score.html', {
        'profile': profile,
        'job_description': getattr(profile, 'last_job_description', '')
    })


@require_POST
@csrf_exempt
def get_ai_suggestions(request):
    """Get AI-powered editing suggestions for resume."""
    try:
        data = json.loads(request.body)
        profile_id = data.get('profile_id')
        resume_text = data.get('resume_text', '')
        
        # Get existing analysis data
        if profile_id:
            profile = Profile.objects.get(id=profile_id, user=request.user)
            analysis_data = {
                'weaknesses': profile.weaknesses,
                'suggestions': profile.suggestions,
                'score_metrics': profile.score_metrics
            }
        else:
            analysis_data = {
                'weaknesses': request.session.get('weaknesses', []),
                'suggestions': request.session.get('suggestions', []),
                'score_metrics': request.session.get('score_metrics', {})
            }
        
        # Generate AI suggestions
        enhanced_analysis = generate_ai_editing_suggestions(analysis_data, resume_text)
        
        # Save results
        if profile_id:
            profile.ai_suggestions = enhanced_analysis.get('ai_suggestions_for_edit', [])
            profile.save()
        else:
            request.session['ai_suggestions'] = enhanced_analysis.get('ai_suggestions_for_edit', [])
        
        return JsonResponse({
            'success': True,
            'ai_suggestions': enhanced_analysis.get('ai_suggestions_for_edit', [])
        })
        
    except Profile.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Profile not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    


