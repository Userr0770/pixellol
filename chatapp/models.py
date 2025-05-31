from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime
from django import forms

class Game(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Lot(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bio = models.TextField(blank=True)
    
    # Новые поля
    online_status = models.BooleanField(default=False)  # True - онлайн, False - оффлайн
    registration_date = models.DateTimeField(auto_now_add=True)  # Дата регистрации
    reviews_count = models.PositiveIntegerField(default=0)  # Количество отзывов
    rating = models.FloatField(default=0.0)  # Рейтинг продавца

    def __str__(self):
        return self.user.username

# Автоматическое создание профиля при регистрации пользователя
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()

class ClashRoyaleLot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)  # Добавляем связь с игрой
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = timezone.now()

    def __str__(self):
        return self.title

class SupportMessage(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_from_support = models.BooleanField(default=False)  # Это добавлено

    def __str__(self):
        return f"{'Support' if self.is_from_support else self.user.username}: {self.message[:30]}"