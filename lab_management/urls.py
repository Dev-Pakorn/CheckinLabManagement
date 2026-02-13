from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. ฝั่งผู้ใช้งาน (User / Kiosk) - ผู้รับผิดชอบ: ปภังกร
    path('', views.index, name='index'),
    path('confirm/', views.confirm, name='confirm'),
    path('timer/', views.timer, name='timer'),
    path('feedback/', views.feedback, name='feedback'),

    # 2. ระบบ Login - ผู้รับผิดชอบ: สถาพร
    path('admin-portal/login/', auth_views.LoginView.as_view(template_name='cklab/admin/admin-login.html'), name='login'),
    path('admin-portal/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # 3. ฝั่งผู้ดูแลระบบ (Admin Portal)
    path('admin-portal/monitor/', views.admin_monitor, name='admin_monitor'), # ธนสิทธิ์
    path('api/monitor-data/', views.api_monitor_data, name='api_monitor_data'), # ธนสิทธิ์
    path('admin-portal/booking/', views.admin_booking, name='admin_booking'), # อัษฎาวุธ
    path('admin-portal/manage-pc/', views.admin_manage_pc, name='admin_manage_pc'), # ณัฐกรณ์
    path('admin-portal/software/', views.admin_software, name='admin_software'), # ลลิดา
    path('admin-portal/report/', views.admin_report, name='admin_report'), # เขมมิกา
    path('admin-portal/config/', views.admin_config, name='admin_config'), # ภานุวัฒน์
]