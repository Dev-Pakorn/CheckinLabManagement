# เขมมิกา — Report + Export CSV
import json
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import timezone
from ..models import UsageLog

class AdminReportView(LoginRequiredMixin, View):
    def get(self, request):
        # 1. ดึงข้อมูลประวัติการใช้งานเฉพาะที่กดออกจากระบบแล้ว (มี end_time)
        logs = UsageLog.objects.exclude(end_time__isnull=True)
        
        log_data = []
        for log in logs:
            # คำนวณเวลาการใช้งาน (เป็นนาที)
            duration = 0
            if log.end_time and log.start_time:
                duration_td = log.end_time - log.start_time
                duration = int(duration_td.total_seconds() / 60)
            
            # จัดการเรื่อง Software และเช็คว่าเป็น AI หรือไม่
            used_software = []
            is_ai = False
            if log.Software:
                # สมมติว่าเก็บชื่อโปรแกรมโดยใช้ลูกน้ำคั่น (เช่น "VS Code, ChatGPT")
                sw_list = [s.strip() for s in log.Software.replace(',', ';').split(';')]
                used_software = sw_list
                
                # เช็คคำเพื่อแยกหมวด AI
                ai_keywords = ['ai', 'gpt', 'claude', 'gemini', 'copilot']
                is_ai = any(kw in s.lower() for s in sw_list for kw in ai_keywords)

            # แปลง Role ให้ตรงกับเงื่อนไขในไฟล์ JS
            role_map = {'student': 'student', 'staff': 'staff', 'guest': 'external'}

            # สร้าง Dictionary ให้หน้าตาเหมือนใน mock-db ทุกประการ
            log_dict = {
                'timestamp': log.end_time.isoformat(),
                'startTime': log.start_time.isoformat(),
                'action': 'END_SESSION',
                'userId': log.user_id or '-',
                'userName': log.user_name or 'Unknown',
                'userRole': role_map.get(log.user_type, 'external'),
                'userFaculty': log.department or '',
                'userYear': log.user_year or '',
                'pcId': log.computer.replace('PC-', '') if log.computer else '',
                'durationMinutes': duration,
                'usedSoftware': used_software,
                'isAIUsed': is_ai,
                'satisfactionScore': log.satisfaction_score,
                'comment': log.comment or ''
            }
            log_data.append(log_dict)

        # 2. แปลงเป็น JSON String ส่งไปให้ Template
        context = {
            'logs_json': log_data
        }
        return render(request, 'cklab/admin/admin-report.html', context)

    def post(self, request):
        pass

class AdminReportExportView(LoginRequiredMixin, View):
    def get(self, request):
        # หน้า Report มีปุ่ม Export CSV ทำงานผ่าน JavaScript อยู่แล้ว
        # View นี้อาจจะปล่อยว่างไว้ หรือเอาไว้ทำ Export ผ่าน Server ในอนาคต
        pass

    def post(self, request):
        pass