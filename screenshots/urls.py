
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('add/', ImageCreation.as_view(), name="create_image"),
    path('update-image/<int:pk>/', ImageUpdate.as_view(), name='update_image'),
    path('image-detail/<int:pk>/', imageDetail, name='image_detail'),
    path('delete-image/<int:pk>/', ImageDeletion.as_view(), name='delete_image'),

]