# ปภังกร — User / Kiosk Side

import json
import base64
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.utils import timezone
from django.http import JsonResponse

# Models ที่ต้องใช้
from lab_management.models import Computer, Software, SiteConfig, Booking, UsageLog


class IndexView(View):
    def get(self, request):
        # ดึง Config ของระบบ (ถ้ายังไม่มีในฐานข้อมูลให้คืนค่า None ไปก่อน)
        config = SiteConfig.objects.first()
        
        # รับค่า pc_id จาก URL Parameter (เช่น /kiosk/?pc=PC-01) 
        pc_name = request.GET.get('pc', 'Unknown')
        
        context = {
            'config': config,
            'computer_name': pc_name
        }
        return render(request, 'cklab/kiosk/index.html', context)

    def post(self, request):
        pass


class StatusView(View):
    def get(self, request, pc_id):
        # API สำหรับคืนค่าสถานะเครื่อง ให้ JS (timer.js, auth.js) เช็คแบบ Real-time
        computer = get_object_or_404(Computer, name=pc_id)
        config = SiteConfig.objects.first()
        
        # ค้นหาการจองคิวถัดไปของเครื่องนี้
        next_booking = Booking.objects.filter(
            computer=computer,
            status='APPROVED',
            start_time__gte=timezone.now()
        ).order_by('start_time').first()

        data = {
            'pc_id': computer.name,
            'status': computer.status,
            'is_open': config.is_open if config else False,
            'next_booking_start': next_booking.start_time.isoformat() if next_booking else None
        }
        return JsonResponse(data)


class VerifyUserAPIView(View):
    def post(self, request):
        # API สำหรับตรวจสอบรหัสนักศึกษา (เชื่อมกับ UBU API)
        try:
            body = json.loads(request.body)
            student_id = body.get('student_id', '').strip()

            if not student_id:
                return JsonResponse({'status': 'error', 'message': 'กรุณาระบุรหัสนักศึกษา'}, status=400)

            # 1. ขอ Token 
            login_url = "https://esapi.ubu.ac.th/api/v1/auth/login"
            login_payload = {
                "username": "dssiapi",
                "password": "it[vk0kipN;kFp-v,k"
            }
            token_response = requests.post(login_url, json=login_payload, timeout=10)
            token_data = token_response.json()

            if token_response.status_code != 200 or 'access_token' not in token_data:
                return JsonResponse({'status': 'error', 'message': 'ไม่สามารถเชื่อมต่อระบบของมหาวิทยาลัยได้'}, status=500)

            access_token = token_data['access_token']

            # 2. เข้ารหัสรหัสนักศึกษาเป็น Base64
            encoded_id = base64.b64encode(student_id.encode('utf-8')).decode('utf-8')

            # 3. ดึงข้อมูลนักศึกษา
            data_url = "https://esapi.ubu.ac.th/api/v1/student/reg-data"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            data_payload = {"loginName": encoded_id}
            data_response = requests.post(data_url, headers=headers, json=data_payload, timeout=10)
            result = data_response.json()

            if result.get('statusCode') == 200 and result.get('data'):
                user_data = result['data'][0]
                full_name = f"{user_data.get('USERPREFIXNAME', '')}{user_data.get('USERNAME', '')} {user_data.get('USERSURNAME', '')}"
                
                # คำนวณชั้นปี
                entry_year_str = student_id[:2]
                try:
                    current_thai_year = timezone.now().year + 543
                    current_year_short = current_thai_year % 100
                    student_year = max(1, (current_year_short - int(entry_year_str)) + 1)
                except:
                    student_year = "-"

                return JsonResponse({
                    'status': 'success',
                    'data': {
                        'id': student_id,
                        'name': full_name.strip(),
                        'faculty': user_data.get('FACULTYNAME', 'มหาวิทยาลัยอุบลราชธานี'),
                        'role': 'student',
                        'level': user_data.get('LEVELNAME', 'ปริญญาตรี'),
                        'year': str(student_year)
                    }
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'ไม่พบข้อมูลในระบบ (รหัสผิด หรือไม่ได้ลงทะเบียน)'}, status=404)

        except requests.exceptions.RequestException:
            return JsonResponse({'status': 'error', 'message': 'ต้องเชื่อมต่ออินเทอร์เน็ตของมหาวิทยาลัย'}, status=503)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


class CheckinView(View):
    def get(self, request, pc_id):
        # หากเข้าด้วย GET ให้พากลับไปหน้า Index
        return redirect(f"{reverse('kiosk_index')}?pc={pc_id}")

    def post(self, request, pc_id):
        computer = get_object_or_404(Computer, name=pc_id)
        config = SiteConfig.objects.first()
        
        # ตรวจสอบว่าแล็บเปิดอยู่และเครื่องว่างหรือไม่
        if (config and not config.is_open) or computer.status not in ['AVAILABLE', 'RESERVED']:
            return redirect(f"{reverse('kiosk_index')}?pc={pc_id}&error=unavailable")

        # รับข้อมูลจาก Form (auth.js ส่งมา)
        user_id = request.POST.get('user_id')
        user_name = request.POST.get('user_name')
        user_type = request.POST.get('user_type', 'student')
        department = request.POST.get('department', '')
        user_year = request.POST.get('user_year', '') 
        
        # บันทึกข้อมูลการเข้าใช้งานลง UsageLog
        software_name = computer.Software.name if computer.Software else None
        usage_log = UsageLog.objects.create(
            user_id=user_id,
            user_name=user_name,
            user_type=user_type,
            department=department,
            user_year=user_year,  
            computer=computer.name,
            Software=software_name
        )

        # เปลี่ยนสถานะเครื่องเป็น IN_USE
        computer.status = 'IN_USE'
        computer.save()

        # นำทางไปหน้าจับเวลา
        return render(request, 'cklab/kiosk/timer.html', {'computer': computer, 'log_id': usage_log.id})


class CheckoutView(View):
    def get(self, request, pc_id):
        return redirect(f"{reverse('kiosk_index')}?pc={pc_id}")

    def post(self, request, pc_id):
        computer = get_object_or_404(Computer, name=pc_id)
        
        # หาการใช้งานปัจจุบันของเครื่องนี้ที่ยังไม่ได้ Checkout
        usage_log = UsageLog.objects.filter(computer=computer.name, end_time__isnull=True).last()
        
        if usage_log:
            # ลงเวลาสิ้นสุด
            usage_log.end_time = timezone.now()
            usage_log.save()

        # คืนสถานะเครื่องให้กลับมาว่าง
        computer.status = 'AVAILABLE'
        computer.save()

        # ส่งต่อไปหน้าประเมินความพึงพอใจ
        log_id = usage_log.id if usage_log else 0
        return redirect('kiosk_feedback', pc_id=computer.name, software_id=log_id)


class FeedbackView(View):
    def get(self, request, pc_id, software_id):
        context = {
            'pc_id': pc_id,
            'log_id': software_id  
        }
        return render(request, 'cklab/kiosk/feedback.html', context)

    def post(self, request, pc_id, software_id):
        # รับค่าคะแนนและคอมเมนต์
        score = request.POST.get('satisfaction_score')
        comment = request.POST.get('comment', '')

        # อัปเดตข้อมูล UsageLog
        try:
            usage_log = UsageLog.objects.get(id=software_id)
            if score:
                usage_log.satisfaction_score = int(score)
            if comment:
                usage_log.comment = comment
            usage_log.save()
        except UsageLog.DoesNotExist:
            pass

        # กลับหน้าแรกเมื่อประเมินเสร็จ
        return redirect(f"{reverse('kiosk_index')}?pc={pc_id}")