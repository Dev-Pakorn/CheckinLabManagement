# ปภังกร — Login / Logout
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
# ลบ AdminonDuty ออก เพราะมันไม่มีอยู่จริงใน models.py
from lab_management.models import SiteConfig 

class LoginView(auth_views.LoginView):
    template_name = 'cklab/admin/admin-login.html'

    def form_valid(self, form):
        # 1. ทำการ Login ให้สำเร็จก่อน
        response = super().form_valid(form)
        user = form.get_user()
        
        # 2. ดึงข้อมูลการตั้งค่า (SiteConfig) ออกมา (ID=1)
        # ถ้ายังไม่มีระบบจะสร้างให้ใหม่ทันที (get_or_create)
        config, created = SiteConfig.objects.get_or_create(id=1)
        
        # 3. อัปเดตข้อมูลผู้ดูแลเครื่องลงไปใน SiteConfig โดยตรง
        # เพราะใน models.py คุณกำหนดให้ admin_on_duty เป็น CharField (เก็บตัวอักษร)
        config.admin_on_duty = user.get_full_name() or user.username
        config.contact_email = user.email
        config.contact_phone = "-" # ใส่ขีดไว้ก่อน ตาม Logic เดิมของคุณ
        
        # 4. บันทึกข้อมูลลงฐานข้อมูล
        config.save()

        return response


class LogoutView(auth_views.LogoutView):
    # กำหนด URL Name ที่จะให้เด้งไปหลัง Logout
    next_page = 'admin_login' 

    def dispatch(self, request, *args, **kwargs):
        # 1. ดึง SiteConfig ปัจจุบัน
        config = SiteConfig.objects.filter(id=1).first()
        
        # 2. ถ้ามี Config อยู่ ให้ล้างข้อมูลคนเข้าเวรออก
        if config:
            config.admin_on_duty = None
            config.contact_email = None
            config.contact_phone = None
            config.save()

        # 3. เคลียร์ Session ออกจากระบบตามปกติของ Django
        return super().dispatch(request, *args, **kwargs)