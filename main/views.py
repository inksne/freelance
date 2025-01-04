from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.db.models import Q
from rest_framework import generics
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.renderers import JSONRenderer
from .serializers import RegisterSerializer
from .decorators import jwt_required
from .forms import OrderForm


async def BaseView(request):
    return render(request, 'index.html')


async def AboutUsView(request):
    return render(request, 'about_us.html')


class RegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')  
    
    def post(self, request, *args, **kwargs):
        print('Request data:', request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('/login/')
        print(serializer.errors)
        return Response(serializer.errors, status=400)
    

async def AuthView(request):
    return render(request, 'authenticated.html')


@method_decorator(jwt_required, name='dispatch')
class AddOrderView(View):
    template_name = 'add_order.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')
        form = OrderForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/login/')

        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.save()
            return redirect('/authenticated/')

        return render(request, self.template_name, {'form': form})

