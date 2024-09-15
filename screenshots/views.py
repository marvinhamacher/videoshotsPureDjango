# made by marvin hamacher, marvin scharfe, niko nikolovski
from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django_minio_backend import MinioBackend
from minio import Minio, S3Error

from videoshotsPureDjango import settings
from .forms import ScreenshotForm
from .models import (Screenshot)

def home(request):
    images = Screenshot.objects.all() # Gibt alle Plan als query einem Objekt
    images = images.order_by("-id")
    context = {
        'images': images
    }
    return render(request, 'homepage.html', context)



class ImageCreation(CreateView):
    model = Screenshot
    template_name = 'createimage.html'
    form_class = ScreenshotForm
    success_url = reverse_lazy("home")

class ImageUpdate(UpdateView):
    model = Screenshot
    template_name = "updateimage.html"
    form_class = ScreenshotForm
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)

def imageDetail(request,pk):
    image = get_object_or_404(Screenshot, id=pk)
    context = {
        'item': image,
    }
    return render(request,template_name="imagedetails.html",context=context)

class ImageDeletion(DeleteView):
    model = Screenshot
    context_object_name = 'image'
    template_name = "deleteimage.html"
    success_url = reverse_lazy("home")


