from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Post
from .forms import UploadForm

class IndexView(ListView):
    model = Post
    template_name = 'gallery/index.html'
    context_object_name = 'posts'
    paginate_by = 6
    ordering = ['-pub_date']

class ImageUploadView(CreateView):
    model = Post
    form_class = UploadForm
    template_name = 'gallery/upload.html'
    success_url = reverse_lazy('gallery:success')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'gallery/post_confirm_delete.html'
    success_url = reverse_lazy('gallery:index')

