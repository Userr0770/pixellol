# utils.py
import random
import string
from django.core.mail import send_mail
from django.conf import settings

def generate_verification_code():
    """Генерация 6-значного кода для подтверждения."""
    return ''.join(random.choices(string.digits, k=6))

def send_verification_code(email, code):
    """Отправка кода подтверждения на email."""
    subject = 'Ваш код подтверждения'
    message = f'Ваш код подтверждения: {code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        # Логирование или обработка ошибок отправки почты
        print(f"Ошибка отправки email: {e}")