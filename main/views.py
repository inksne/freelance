from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden

from rest_framework import generics
from rest_framework.views import View
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .serializers import RegisterSerializer
from .decorators import jwt_required
from .forms import OrderForm, ResponseForm, ReviewForm
from .models import Order, Review, OrderResponse


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
    

@jwt_required
def DeleteOrderView(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.customer != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот заказ.")
    order.delete()
    return redirect('/authenticated/')
    

def OrdersView(request):
    orders = Order.objects.all()
    for order in orders:
        order.response_count = order.responses.count()
    return render(request, 'index.html', {'orders': orders})


@jwt_required
def AuthOrdersView(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    orders = Order.objects.all()
    for order in orders:
        order.response_count = order.responses.count()
        if order.customer == request.user:
            order.responses_list = order.responses.all()
        else:
            order.responses_list = None

    return render(request, 'all_orders.html', {'orders': orders})


@jwt_required
def AddResponse(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.responses.filter(user=request.user).exists():
        messages.info(request, "Вы уже откликнулись на этот заказ.")
        return redirect('authenticated')

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.order = order
            response.user = request.user
            response.save()
            return redirect('authenticated')
    else:
        form = ResponseForm()

    return render(request, 'add_response.html', {'form': form, 'order': order})


@jwt_required
def MyProfileView(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    user = request.user
    reviews = Review.objects.filter(reviewed_user=user)
    return render(request, 'profile.html', {'user': user, 'reviews': reviews})


@jwt_required
def UserProfileView(request, user_id):
    user = get_object_or_404(User, id=user_id)
    reviews = Review.objects.filter(reviewed_user=user)

    can_leave_review = True

    if request.method == 'POST' and can_leave_review:
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.instance.reviewer = request.user
            form.instance.reviewed_user = user
            form.save()
            messages.success(request, "Отзыв успешно оставлен!")
            return redirect('user_profile', user_id=user.id)
    else:
        form = ReviewForm()

    return render(request, 'profile.html', {
        'user': user,
        'form': form,
        'reviews': reviews,
        'can_leave_review': can_leave_review,
    })


@jwt_required
def DeleteReviewView(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.reviewer != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот отзыв")
    review.delete()
    return redirect('/authenticated/')