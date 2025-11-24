from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import UploadForm

def index(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        return render(request, 'gallery/index.html', {'posts' : posts})

def image_upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery:success')
    else:
        form = UploadForm()
    return render(request, 'gallery/upload.html', {'form' : form})

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'gallery/post_confirm_delete.html'
    success_url = reverse_lazy('gallery:index')

