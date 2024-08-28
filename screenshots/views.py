# made by marvin hamacher, marvin scharfe, niko nikolovski
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from .forms import ScreenshotForm
from .models import (Screenshot)


def home(request):
    images = Screenshot.objects.all() # Gibt alle Plan als query einem Objekt
    sorted_images = images.order_by("-id")
    context = {
        'images': sorted_images,
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


