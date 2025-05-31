# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.utils.timezone import localtime
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
import random
import logging

# Local imports
from .models import Game, Product, UserProfile, SupportMessage, ClashRoyaleLot, Lot
from .forms import ProductForm, LotForm, SupportForm, SupportMessageForm
from .utils import send_verification_code  # твоя функция отправки кода


User = get_user_model()

@staff_member_required
def admin_chat_view(request, userprofile_id):
    user_profile = UserProfile.objects.get(id=userprofile_id)
    current_user = request.user.userprofile
    current_user_id = request.user.id  # Передадим в шаблон ID текущего юзера
    is_admin = request.user.is_staff  # Проверяем, является ли текущий пользователь администратором

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            # Если это администратор, то сообщение от поддержки
            is_from_support = is_admin

            new_message = SupportMessage.objects.create(
                message=message,
                sender=current_user,
                recipient = user_profile.user if is_admin else User.objects.get(username='admin'),
                user=current_user.user,
                is_from_support=is_from_support,  # Устанавливаем правильное значение
                is_answered=not is_from_support
            )

            # Возвращаем HTML, который будет вставлен в чат
            html = f'''
            <div class="message {'from-support' if new_message.is_from_support else 'from-user'}">
                <strong>{'Поддержка' if new_message.is_from_support else 'Вы'}:</strong> {new_message.message}
            </div>
            '''
            return HttpResponse(html)

    # Загружаем все сообщения
    messages = SupportMessage.objects.filter(user=user_profile.user).order_by('timestamp')

    return render(request, 'admin_chat.html', {
        'userprofile': user_profile,
        'current_user': current_user,
        'current_user_id': current_user_id,
        'messages': messages
    })

@login_required(login_url='login')
def brawl_stars_products(request):
    brawl_stars_game = Game.objects.filter(name="Brawl Stars").first()
    lots = Lot.objects.filter(game=brawl_stars_game, user=request.user)
    return render(request, 'chatapp/brawl_stars.html', {'lots': lots})

@login_required(login_url='login')
def profile_view(request):
    user = request.user
    user_lots = Lot.objects.filter(user=user)  # ИСПРАВИЛ: было owner=user

    games = Game.objects.all()
    game_lots = {}

    for game in games:
        game_lots[game] = user_lots.filter(game=game)

    context = {
        'username': user.username,
        'registration_date': localtime(user.date_joined),
        'avatar_url': 'https://via.placeholder.com/100',  # заменишь позже
        'balance': user.userprofile.balance if hasattr(user, 'userprofile') else 0,
        'games': games,
        'game_lots': game_lots,
    }
    return render(request, 'Profile.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Проверка на уникальность никнейма
        if User.objects.filter(username=username).exists():
            messages.error(request, "Никнейм уже используется.")
        else:
            user = User.objects.create_user(username=username, password=password)

            login(request, user)  # Авторизация пользователя
            return redirect('home')  # Перенаправление на главную страницу

    return render(request, 'chatapp/register.html')

def home_view(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def create_product(request, game_name):
    try:
        game = Game.objects.get(name=game_name)
    except Game.DoesNotExist:
        return HttpResponse("Такой игры нет.", status=404)

    if request.method == 'POST':
        form = LotForm(request.POST)
        if form.is_valid():
            lot = form.save(commit=False)
            lot.user = request.user
            lot.game = game
            lot.save()
            return redirect('profile')
    else:
        form = LotForm()
    return render(request, 'chatapp/create_product.html', {'form': form, 'game': game})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProductForm(instance=product)
    return render(request, 'chatapp/edit_product.html', {'form': form, 'product': product})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'chatapp/product_detail.html', {'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)
    product.delete()
    return redirect('profile')

@login_required(login_url='login')
def clash_lots_view(request):
    clash_game = Game.objects.get(name="Clash of Clans")
    lots = Lot.objects.filter(game=clash_game)
    return render(request, 'chatapp/clash_lots.html', {'lots': lots})

@login_required
def create_clash_lot(request):
    clash_game = Game.objects.get(name="Clash of Clans")
    if request.method == 'POST':
        form = LotForm(request.POST)
        if form.is_valid():
            lot = form.save(commit=False)
            lot.user = request.user
            lot.game = clash_game
            lot.save()
            return redirect('profile')
    else:
        form = LotForm()
    return render(request, 'chatapp/create_lot.html', {'form': form})

@login_required
def edit_lot(request, lot_id):
    lot = get_object_or_404(Lot, id=lot_id)
    if request.method == 'POST':
        form = LotForm(request.POST, instance=lot)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Или куда перенаправить после сохранения
    else:
        form = LotForm(instance=lot)

    return render(request, 'chatapp/edit_lot.html', {'form': form, 'lot': lot})

@login_required
def delete_lot(request, lot_id):
    lot = get_object_or_404(Lot, id=lot_id)

    # Проверяем, что пользователь является владельцем лота
    if lot.user != request.user:
        return redirect('profile')  # Если это не его лот, редиректим на профиль

    # Если запрос - GET, то показываем страницу с подтверждением удаления
    if request.method == 'GET':
        return render(request, 'chatapp/delete.html', {'lot': lot})

    # Если запрос - POST, удаляем лот и редиректим на профиль
    if request.method == 'POST':
        lot.delete()
        return redirect('profile')

@login_required
def edit_lot_view(request, lot_id):
    lot = get_object_or_404(Lot, id=lot_id, user=request.user)

    if request.method == 'POST':
        form = LotForm(request.POST, instance=lot)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = LotForm(instance=lot)

    return render(request, 'edit_lot.html', {'form': form, 'lot': lot})


@login_required
def finances(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    profile = UserProfile.objects.get(user=request.user)
    balance = profile.balance
    return render(request, 'chatapp/finances.html', {
        'transactions': transactions,
        'balance': balance,
    })

def rules_view(request):
    return render(request, 'chatapp/rules.html')

@login_required
def settings_view(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        # Обработка загрузки нового аватара
        avatar = request.FILES.get('avatar')
        if avatar:
            user_profile.avatar = avatar
            user_profile.save()
            return redirect('settings')  # имя в urls останется прежним

    return render(request, 'chatapp/settings.html', {'user_profile': user_profile})

@login_required
def delete_avatar(request):
    user_profile = request.user.userprofile
    if request.method == 'GET':
        user_profile.avatar.delete()  # Удаляет файл аватара
        user_profile.save()
        return redirect('settings')

def users(request):
    all_users = User.objects.all().select_related('userprofile')
    return render(request, 'chatapp/users.html', {'users': all_users})

@login_required
def create_or_edit_cr_lot(request, lot_id=None):
    if lot_id:
        # Редактирование лота
        lot = get_object_or_404(ClashRoyaleLot, id=lot_id)
        if lot.user != request.user:
            return redirect('cr_lots')  # если не принадлежит текущему пользователю, редиректим
        form = ClashRoyaleLotForm(request.POST or None, instance=lot)
    else:
        # Создание нового лота
        form = ClashRoyaleLotForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        lot = form.save(commit=False)
        lot.user = request.user
        lot.save()
        return redirect('cr_lots')  # редирект на страницу списка лотов
    
    return render(request, 'chatapp/edit_lot.html', {'form': form, 'lot': lot if lot_id else None})

@login_required(login_url='login')
def cr_lots(request):
    game = Game.objects.get(name="Clash Royale")
    lots = Lot.objects.filter(user=request.user, game=game)  # Получаем все лоты текущего пользователя
    return render(request, 'chatapp/cr_lots.html', {'lots': lots})


@login_required
def support_view(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            # Сохраняем сообщение, связываем с текущим пользователем
            message = form.save(commit=False)
            message.user = request.user
            message.save()

            # После успешной отправки формы перенаправляем на страницу чата
            return redirect('support_chat')  # 'support_chat' — это имя пути для чата
        return HttpResponse(status=400)  # Неверные данные
    else:
        form = SupportForm()

    return render(request, 'chatapp/support.html', {'form': form})

@login_required
def support_chat(request):
    if request.method == 'POST':
        form = SupportMessageForm(request.POST, user=request.user)
        if form.is_valid():
            msg = form.save()

            message_html = f"""
                <div class="message {'from-support' if msg.is_from_support else 'from-user'}">
                    <strong>{'Поддержка' if msg.is_from_support else 'Вы'}:</strong> {msg.message}
                </div>
            """
            return HttpResponse(message_html)

    else:
        form = SupportMessageForm(user=request.user)

    messages = SupportMessage.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'chatapp/support_chat.html', {'form': form, 'messages': messages})

def admin_chat_list(request):
    # Получаем всех пользователей с активными чатами
    users_with_chats = User.objects.filter(supportmessage__isnull=False).distinct()
    return render(request, 'admin_chat_list.html', {'users_with_chats': users_with_chats})
