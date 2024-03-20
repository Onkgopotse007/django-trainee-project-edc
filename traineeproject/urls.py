"""
URL configuration for traineeproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from traineeproject.admin_site import traineeproject_admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('subject_consent/', include('subjectconsentquestionnaire.urls')),
    path('community_involvement/', include('communityinvolvementquestionnaire.urls')),
    path('education/', include('educationquestionnaire.urls')),
    path('enrollment/', include('enrollmentquestionnaire.urls')),
    path('trainee_admin/', traineeproject_admin.urls),
]
