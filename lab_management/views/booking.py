# อัษฎาวุธ — Booking
import json
import csv
import io
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone

from lab_management.models import Booking, Computer, Software

# ==========================================
# 1. โหลดหน้าจอจัดการการจอง (HTML)
# ==========================================
class AdminBookingView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'cklab/admin/admin-booking.html')

# ==========================================
# 2. นำเข้าข้อมูลด้วยไฟล์ CSV
# ==========================================
class AdminImportBookingView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'cklab/admin/admin-booking-import.html')

    def post(self, request):
        csv_file = request.FILES.get('csv_file')
        
        if not csv_file or not csv_file.name.endswith('.csv'):
            messages.error(request, '❌ กรุณาอัปโหลดไฟล์นามสกุล .csv เท่านั้น')
            return redirect('admin_booking_import')

        try:
            decoded_file = csv_file.read().decode('utf-8-sig')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            success_count = 0
            for row in reader:
                pc_name = row.get('pc_name')
                computer = Computer.objects.filter(name=pc_name).first()
                
                if not computer:
                    continue 
                    
                # ปรับให้ตรงกับ Model: ใช้ student_id
                # และรวมวันที่/เวลาให้เป็น DateTimeField
                start_dt = datetime.strptime(f"{row.get('date')} {row.get('start_time')}", '%Y-%m-%d %H:%M')
                end_dt = datetime.strptime(f"{row.get('date')} {row.get('end_time')}", '%Y-%m-%d %H:%M')

                Booking.objects.create(
                    student_id=row.get('user_id'), # แมพ user_id ลง student_id
                    computer=computer,
                    start_time=timezone.make_aware(start_dt),
                    end_time=timezone.make_aware(end_dt),
                    status='APPROVED'
                )
                success_count += 1
                
            messages.success(request, f'✅ นำเข้าข้อมูลสำเร็จ {success_count} รายการ')
        except Exception as e:
            messages.error(request, f'❌ เกิดข้อผิดพลาดในการอ่านไฟล์: {str(e)}')
            
        return redirect('admin_booking')

# ==========================================
# 3. API สำหรับ JavaScript ดึงข้อมูลทั้งหมด
# ==========================================
class AdminBookingDataAPIView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            # 1. ดึงข้อมูลเครื่องคอมพิวเตอร์
            pcs = Computer.objects.all().order_by('name')
            
            pc_list = []
            for p in pcs:
                # เรียกใช้ฟิลด์ Software (S ตัวใหญ่) ตาม Model
                sw_name = p.Software.name if p.Software else '-'
                sw_type = p.Software.type if p.Software else 'General'

                pc_list.append({
                    'id': p.name, 
                    'name': p.name,
                    'status': p.status,
                    'software_name': sw_name,
                    'software_type': sw_type,
                })
            
            # 2. ดึงข้อมูล Software
            softwares = Software.objects.all()
            sw_list = [{'id': s.id, 'name': s.name, 'type': s.type} for s in softwares]
            
            # 3. ดึงข้อมูลรายการจอง
            bookings = Booking.objects.all().order_by('-start_time')
            booking_list = []
            for b in bookings:
                booking_list.append({
                    'id': b.id,
                    'user_id': b.student_id, # ตามชื่อฟิลด์ใน Model
                    'user_name': b.student_id, # เนื่องจาก Model Booking ไม่มี user_name จึงใช้รหัสแทน
                    'pc_name': b.computer.name if b.computer else '-',
                    'date': b.start_time.strftime('%Y-%m-%d') if b.start_time else '',
                    'start_time': b.start_time.strftime('%H:%M') if b.start_time else '',
                    'end_time': b.end_time.strftime('%H:%M') if b.end_time else '',
                    'status': b.status,
                    'software': b.computer.Software.name if b.computer and b.computer.Software else '-'
                })
                
            return JsonResponse({
                'status': 'success', 
                'pcs': pc_list, 
                'software': sw_list, 
                'bookings': booking_list
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# ==========================================
# 4. API สำหรับเพิ่มการจอง (จาก Modal)
# ==========================================
class AdminBookingAddAPIView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            pc_name = data.get('pc_name')
            computer = get_object_or_404(Computer, name=pc_name)
            
            # รวมวันที่และเวลา
            start_dt = datetime.strptime(f"{data.get('date')} {data.get('start_time')}", '%Y-%m-%d %H:%M')
            end_dt = datetime.strptime(f"{data.get('date')} {data.get('end_time')}", '%Y-%m-%d %H:%M')

            Booking.objects.create(
                student_id=data.get('user_id'), # ตาม Model
                computer=computer,
                start_time=timezone.make_aware(start_dt),
                end_time=timezone.make_aware(end_dt),
                status='APPROVED'
            )
            return JsonResponse({'status': 'success', 'message': 'บันทึกสำเร็จ'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# ==========================================
# 5. API สำหรับเปลี่ยนสถานะ / ยกเลิกการจอง
# ==========================================
class AdminBookingStatusAPIView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            booking = get_object_or_404(Booking, id=pk)
            data = json.loads(request.body)
            new_status = data.get('status')
            if new_status:
                booking.status = new_status
                booking.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

class AdminBookingDetailView(LoginRequiredMixin, View):
    def get(self, request, pk): pass
    def post(self, request, pk): pass