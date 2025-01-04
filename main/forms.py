from django import forms
from .models import Order

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