from django.urls import path
from . import views, admin
from django.contrib.auth import views as auth_views
from .views import home_view, settings_view, admin_chat_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='chatapp/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('brawl-stars/', views.brawl_stars_products, name='brawl_stars_products'),
    path("", home_view, name='home'),
    path('create/<str:game_name>/', views.create_product, name='create_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('products/brawl-stars/', views.brawl_stars_products, name='brawl_stars'),
    path('clash-of-clans/', views.clash_lots_view, name='clash_lots'),
    path('clash-of-clans/create/', views.create_clash_lot, name='create_clash_lot'),
    path('lot/<int:lot_id>/edit/', views.edit_lot, name='edit_lot'),
    path('lot/<int:lot_id>/delete/', views.delete_lot, name='delete_lot'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='chatapp/reset_password.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='chatapp/reset_password_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name='password_reset_complete'),
    path('UserProfile/', views.UserProfile, name='UserProfile'),
    path('finances/', views.finances, name='chatapp/finances'),
    path('rules/', views.rules_view, name='chatapp/rules'),
    path('settings/', views.settings_view, name='settings'),
    path('delete-avatar/', views.delete_avatar, name='delete_avatar'),
    path('users/<int:user_id>/', views.users, name='users'),
    path('clashroyale/', views.cr_lots, name='cr_lots'),
    path('clashroyale/create/', views.create_product, name='create_cr_lot'),
    path('clashroyale/edit/<int:lot_id>/', views.edit_lot, name='edit_cr_lot'),
    path('support/', views.support_view, name='support'),
    path('support/chat/', views.support_chat, name='support_chat'),
    path('chat/<int:userprofile_id>/', views.admin_chat_view, name='admin_chat'),
    path('admin/chats/', views.admin_chat_list, name='admin_chat_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обрабатываем статические файлы, если проект в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)