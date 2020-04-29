from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate
from .models import Message
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import logout, login

import json
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'fsociety/index.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return None
        print("index")
        return User.objects.order_by('-id')


class AboutView(generic.ListView):
    template_name = 'fsociety/about.html'

    def get_queryset(self):
        return None


def chat_view(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'fsociety/signin.html')
    print("chat_view")
    receiver = get_object_or_404(User, pk=pk)
    return render(request, 'fsociety/chat.html', {'receiver': receiver})


def get_messages(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'fsociety/signin.html')
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
    if not request.user.is_authenticated:
        return render(request, 'fsociety/signin.html')
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


def logout_view(request):
    logout(request)
    return render(request, 'fsociety/signin.html')


def sign_in_form(request):
    return render(request, 'fsociety/signin.html')


def login_view(request):
    print(request.POST)
    user = authenticate(username=request.POST['username'],
                        password=request.POST['password'])
    if user is not None:
        if user.is_active:
            login(request, user)
            print("User is valid, active and authenticated")
            return HttpResponseRedirect(reverse('fsociety:index', args=()))
        else:
            print("The password is valid, but the account has been disabled!")
            return render(request, 'fsociety/signin.html', {'message': 'Your account disabled'})
    else:
        # the authentication system was unable to verify the username and password
        print("The username and password were incorrect.")
        return render(request, 'fsociety/signin.html', {'message': 'Incorrect username or password'})
