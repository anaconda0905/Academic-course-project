"""AoneBrains URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.views.static import serve


def dashboard(request):
    if request.user.is_anonymous:
        return redirect("aonebrains_main:Home")
    elif request.user.account_type == "school":
        return redirect("schools:dashboard")
    elif request.user.account_type == "teacher":
        return redirect("schools:teachers:dashboard")
    elif request.user.account_type == "admin":
        return redirect("accounts:admin_dashboard")
    elif request.user.account_type == "curator":
        return redirect("accounts:curator_dashboard")
    elif request.user.account_type == "editor":
        return redirect("accounts:editor_dashboard")
    elif request.user.account_type == "super admin":
        return redirect("accounts:super_admin_dashboard")
    elif request.user.account_type == "marketer":
        return redirect("accounts:marketer_dashboard")
    else:
        return redirect("aonebrains_main:Home")


urlpatterns = [
                  path('dashboard', dashboard, name='dashboard'),
                  path('', include("aonebrains_main.urls")),
                  path('courses/', include("aonebrains_courses.urls")),
                  path('courses/', include("aonebrains_quiz.urls")),
                  path('aDmInPanel_URL-Should_AlwaYs_HardER_toGetTO__ThatPage/admin/', admin.site.urls),
                  path('', include('user_sessions.urls', 'user_sessions')),
                  path('accounts/', include('accounts.urls')),
                  # path('accounts/', include('registration.backends.admin_approval.urls')),
                  path('school/courses/', include("school_courses.urls")),
                  path('', include('schools.urls')),
                  path('media/<str:path>/', serve, {'document_root': settings.MEDIA_ROOT}),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
