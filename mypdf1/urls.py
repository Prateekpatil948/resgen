from django.contrib import admin
from django.urls import path
from pdf import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome_page, name='welcome'), 
    path('home/', views.home, name='home'),
    path('generate/', views.generate_options, name='generate_options'),
    path('generate/resume/', views.generate_resume, name='generate_resume'),
    path('view/<int:profile_id>', views.preview_resume, name='preview_resume'),
    path('download/<int:id>/', views.download_resume, name='download'),
    path('list/', views.list_profiles, name='list'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('delete/<int:profile_id>/', views.delete_resume, name='delete_resume'),
    path('templates/', views.template_preview, name='template_preview'),
    path('templates/<str:template_id>/', views.template_preview, name='template_preview'),
    path('preview/<int:profile_id>/', views.preview_resume, name='preview_resume'),
    # Resume analysis URLs
    path('resume/analyze/', views.analyze_uploaded_resume, name='analyze_resume'),
    path('profile/<int:profile_id>/analyze/', views.analyze_profile_resume, name='analyze_profile_resume'),
    path('preview_content/<int:profile_id>', views.preview_resume_content, name='preview_content'),
    
    # New AI suggestions endpoint
    path('get-ai-suggestions/', views.get_ai_suggestions, name='get_ai_suggestions'),
]