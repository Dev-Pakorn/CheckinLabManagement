# ปภังกร — Login / Logout
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from lab_management.models import SiteConfig, AdminonDuty

class LoginView(auth_views.LoginView):
    template_name = 'cklab/admin/admin-login.html'

    def form_valid(self, form):
        # ทำการ Login ให้สำเร็จก่อน
        response = super().form_valid(form)
        user = form.get_user()
        
        # ดึงหรือสร้าง Object SiteConfig และ AdminonDuty (ID=1 เพราะมีแค่อันเดียวในระบบ)
        config, _ = SiteConfig.objects.get_or_create(id=1)
        admin_duty, _ = AdminonDuty.objects.get_or_create(id=1)
        
        # อัปเดตข้อมูลผู้ดูแลเครื่องที่เพิ่งล็อกอิน
        admin_duty.admin_on_duty = user.get_full_name() or user.username
        admin_duty.contact_email = user.email
        admin_duty.contact_phone = "-" # ใส่ขีดไว้ก่อน (หากมีการทำระบบ Profile เพิ่มค่อยมาแก้ดึงเบอร์โทรตรงนี้)
        admin_duty.save()

        # ผูกเข้ากับ SiteConfig
        config.admin_on_duty = admin_duty
        config.save()

        return response


class LogoutView(auth_views.LogoutView):
    # กำหนด URL Name ที่จะให้เด้งไปหลัง Logout (เดี๋ยวเราไปตั้งชื่อนี้ใน urls.py กัน)
    next_page = 'login' 

    def dispatch(self, request, *args, **kwargs):
        # ดึง SiteConfig ปัจจุบัน
        config = SiteConfig.objects.filter(id=1).first()
        
        if config and config.admin_on_duty:
            # ล้างข้อมูลของ AdminonDuty เมื่อกดออกจากระบบ
            admin_duty = config.admin_on_duty
            admin_duty.admin_on_duty = None
            admin_duty.contact_phone = None
            admin_duty.contact_email = None
            admin_duty.save()

        # เคลียร์ Session ออกจากระบบ
        return super().dispatch(request, *args, **kwargs)