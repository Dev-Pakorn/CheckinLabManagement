# สถาพร — Login / Logout
from django.contrib.auth import views as auth_views


class LoginView(auth_views.LoginView):
    template_name = 'cklab/admin/admin-login.html'

# LogoutView สามารถใช้ Django's built-in LogoutView ได้เลย โดยกำหนด next_page ให้กลับไปที่หน้า index ของ admin
class LogoutView(auth_views.LogoutView):
    next_page = '/'
