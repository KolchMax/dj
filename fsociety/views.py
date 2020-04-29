from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate
from .models import Message
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import logout
import json
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'fsociety/index.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        print("index")
        return User.objects.order_by('-id')


def chat_view(request, pk):
    print("chat_view")
    receiver = get_object_or_404(User, pk=pk)
    return render(request, 'fsociety/chat.html', {'receiver': receiver})


def get_messages(request, pk):
    print("get_messages")
    msg1 = Message.objects.filter(receiver_id=pk).filter(sender_id=request.user.id)
    msg2 = Message.objects.filter(receiver_id=request.user.id).filter(sender_id=pk)
    messages = (msg1 | msg2).order_by("-date_time").reverse()
    response = []
    for m in messages:
        el = {
            'text': m.text,
            'datetime': m.date_time,
            'receiver': m.receiver.username,
            'sender': m.sender.username
              }
        response.append(el)
    return JsonResponse({'data': response})


def set_messages(request, pk):
    print("set_messages")
    print(request.user)
    receiver = get_object_or_404(User, pk=pk)
    print(receiver)
    new_msg = Message(text=request.POST['new_message'],
                      receiver_id=request.POST['receiver_id'],
                      sender_id=request.user.id)
    print(new_msg)
    Message.save(new_msg)
    return render(request, 'fsociety/chat.html', {'receiver': receiver})
