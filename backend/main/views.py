from . forms import Registration
from . serializers import *
from . models import *

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
import uuid
from rest_framework.response import Response

@login_required
def index(request):
    return render(request, 'main/homepage.html')

def registration(request):
    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            form.save() 
            auth = authenticate(request,
                                username=request.POST['username'],
                                password=request.POST['password1'])
            login(request, auth)
            return HttpResponseRedirect("/")
            messages.success(request, 'Спасибо за регистрацию')
        else:
            messages.error(request, 'Форма заполнена неправильно',
                           extra_tags='danger')
            form = Registration(request.POST)
            return render(request, 'registration/registration.html',
            			  {'form': form})
    else:
        form = Registration()
        return render(request, 'registration/registration.html',
                      {'form': form})

@login_required
def token(request):
    user = request.user
    print(user)
    if Tokens.objects.filter(user=user):
        messages.success(request, 'Токен уже сгенерирован')
    else:
        post = Tokens(user=user, token=uuid.uuid4())
        post.save()
    return HttpResponseRedirect("/")
    messages.success(request, 'Токен сгенерирован')


class MessagesAPI(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = MessagesSerializer
    queryset = Messages.objects.all()


class TokensAPI(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = TokensSerializer
    queryset = Tokens.objects.all()