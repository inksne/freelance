from django import forms
from .models import Order, OrderResponse, Review

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'category', 'description', 'attachment']
        labels = {
            'name': 'Название',
            'category': 'Категория',
            'description': 'Описание',
            'attachment': 'Вложение',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите название заказа'}),
            'category': forms.Select(),
            'description': forms.Textarea(attrs={'placeholder': 'Введите описание'}),
            'attachment': forms.ClearableFileInput(),
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = OrderResponse
        fields = ['message']
        labels = {'message': 'Ваш отклик'}
        widgets = {'message': forms.Textarea(attrs={'placeholder': 'Введите ваш отклик на заказ'})}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'message']
        labels = {
            'rating': 'Рейтинг',
            'message': 'Сообщение',
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }