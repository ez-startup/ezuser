from .serializers import GroupSerializer, SignUpSerializer, TokenSerializer, RefreshTokenSerializer, PasswordChangeSerializer, UserRegisterSerializer, UserSerializer
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics, permissions, serializers
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from usermanager.models import User
import requests, os
from .forms import UserLoginForm, UserRegisterForm
from dotenv import load_dotenv
load_dotenv()


# Oauth2 
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse

class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')

@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)

# Create your views here.
def index(request):
    text = "Welcome to User Manager!"
    return render(request, "base.html",{'text':text})

# first we define the serializers
auth_server = "http://localhost:8000"
def UserLogin(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            r = requests.post(auth_server + '/auth/token/',
                data={
                    'grant_type': 'password',
                    'username': form.cleaned_data.get('username'),
                    'password': form.cleaned_data.get('password'),
                    'client_id': os.environ.get('rs-id'),
                    'client_secret': os.environ.get('rs-secret'),
                },
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            )
            response_json = r.json()
            print(response_json)
            login(request, user)
            
            if next:
                return redirect(next)  # Redirect to the 'next' URL
            return redirect('/auth/applications/')  # Default redirect if 'next' is not specified

    context = {
        'form': form,
    }
    return render(request, "authentication/login.html", context)

def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)

        r = requests.post(auth_server + '/token/',
        data = {
            'grant_type': 'password',
            'username': form.cleaned_data.get('username'),
            'password': form.cleaned_data.get('password'),
            'client_id': os.environ.get('rs-id'),
            'client_secret': os.environ.get('rs-secret'),
        },
        headers= {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        )
        r.json()
        print(r.json())

        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/account/login/')
    context = {
        'form': form
    }
    return render(request, "authentication/signup.html", context)

class UserRegister(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


def logout_view(request):
    logout(request)
    return redirect('/home')


# Create the API views
class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer