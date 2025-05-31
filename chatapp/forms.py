from django import forms
from .models import Game, Product, UserProfile, SupportMessage, Lot, ClashRoyaleLot

class LotForm(forms.ModelForm):
    class Meta:
        model = Lot
        fields = ['title', 'description', 'price']  # Убираем поле 'game'

    def save(self, commit=True):
        lot = super().save(commit=False)
        # Присваиваем игру "Brawl Stars" при сохранении
        lot.game = Game.objects.get(name='Brawl Stars')
        if commit:
            lot.save()
        return lot

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price']  # Убираем поле 'game'

    def save(self, commit=True):
        product = super().save(commit=False)
        # Присваиваем игру "Brawl Stars" при сохранении
        product.game = Game.objects.get(name='Brawl Stars')
        if commit:
            product.save()
        return product

class ClashRoyaleLotForm(forms.ModelForm):
    class Meta:
        model = ClashRoyaleLot
        fields = ['title', 'description', 'price']

class SupportForm(forms.ModelForm):
    class Meta:
        model = SupportMessage
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Сообщение'}),
                  }

class SupportMessageForm(forms.ModelForm):
    class Meta:
        model = SupportMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'id': 'id_message', 'rows': 2, 'placeholder': 'Введите сообщение...'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Получаем пользователя из kwargs
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
            instance.sender = self.user.userprofile
            # Назначаем получателя как админа (используем профиль пользователя)
            instance.recipient = UserProfile.objects.get(user__username='admin')  # Получаем профиль администратора
            instance.is_from_support = self.user.is_staff or self.user.is_superuser
        if commit:
            instance.save()
        return instance