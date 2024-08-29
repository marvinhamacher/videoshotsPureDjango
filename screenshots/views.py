# made by marvin hamacher, marvin scharfe, niko nikolovski
from datetime import timedelta

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django_minio_backend import MinioBackend
from minio import Minio, S3Error

from videoshotsPureDjango import settings
from .forms import ScreenshotForm
from .models import (Screenshot)
from .serializers import ScreenshotSerializer

client = Minio(
    "localhost:9000",
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False  # Use True if using HTTPS
)

def generate_presigned_url(object_name):
    url = client.presigned_get_object(settings.MINIO_PRIVATE_BUCKETS[0], object_name)
    return url



def home(request):
    images = Screenshot.objects.all() # Gibt alle Plan als query einem Objekt
    images = images.order_by("-id")
    image_fields = []
    for n in images:
        image_data = {
            'screenshot_url': f'{generate_presigned_url(str(n.screenshot))}',
            'image': n
        }
        image_fields.append(image_data)

    context = {
        'images': image_fields
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

class ImageDetail(DetailView):
    model = Screenshot
    template_name = "imagedetails.html"


class ImageDeletion(DeleteView):
    model = Screenshot
    context_object_name = 'image'
    template_name = "deleteimage.html"
    success_url = reverse_lazy("home")


