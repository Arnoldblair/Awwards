from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
import cloudinary
import cloudinary.uploader
import cloudinary.api


# api
from django.http import JsonResponse
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,ProjectSerializer
from .permissions import IsAdminOrReadOnly


# Create your views here.
def index(request):  # Home page
    project = Project.objects.all()
    # get the latest project from the database
    latest_project = project[0]
    # get project rating
    rating = Rating.objects.filter(project_id=latest_project.id).first()
    # print(latest_project.id)

    return render(
        request, "index.html", {"projects": project, "project_home": latest_project, "rating": rating}
    )


# single project page
def project_details(request, project_id):
    project = Project.objects.get(id=project_id)
    # get project rating
    rating = Rating.objects.filter(project=project)
    return render(request, "project.html", {"project": project, "rating": rating})


@login_required(login_url="/accounts/login/")
def profile(request):  # view profile
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()  # get profile
    project = Project.objects.filter(user_id=current_user.id).all()  # get all projects
    return render(request, "profile.html", {"profile": profile, "images": project})
