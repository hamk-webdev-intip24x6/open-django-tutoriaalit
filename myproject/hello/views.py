from django.shortcuts import render
from django.views.generic import ListView
from .models import Message
 
# def index(request):
#     context = {"latest_message_list": Message.objects.order_by('-date')[:10]}
#     return render(request, 'hello/index.html', context)

def second(request):
    context = {}
    return render(request, 'hello/second.html', context)

class IndexView(ListView):
    template_name = 'hello/index.html'
    context_object_name = 'latest_message_list'

    def get_queryset(self):
        """Return the last 10 published messages."""
        return Message.objects.order_by('-date')[:10]