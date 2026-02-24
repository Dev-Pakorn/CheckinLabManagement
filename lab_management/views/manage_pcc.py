# lab_management/views/manage_pc.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages # นำเข้า messages สำหรับแจ้งเตือน
from django.db import IntegrityError # นำเข้า IntegrityError สำหรับดักจับชื่อซ้ำ

# นำเข้า Models ที่ต้องใช้
from ..models import Computer, Software

class AdminManagePcView(LoginRequiredMixin, View):
    def get(self, request):
        # ดึงข้อมูล Computer ทั้งหมด
        pcs = Computer.objects.all().order_by('name')
        # ดึงข้อมูล Software ทั้งหมดเพื่อเตรียมไว้แสดงใน Dropdown/Modal
        softwares = Software.objects.all()
        
        context = {
            'computers': pcs,  
            'softwares': softwares,
        }
        return render(request, 'cklab/admin/admin-manage-pc.html', context)


class AdminAddPcView(LoginRequiredMixin, View):
    def get(self, request):
        return redirect('admin_manage_pc') 

    def post(self, request):
        # รับค่าจาก Form
        name = request.POST.get('name')
        status = request.POST.get('status', 'AVAILABLE')
        software_id = request.POST.get('software_id')
        description = request.POST.get('description', '')

        # ค้นหา Software object หากมีการส่ง id มา
        software_obj = None
        if software_id:
            software_obj = Software.objects.filter(id=software_id).first()

        # สร้างข้อมูล PC ใหม่ พร้อมดักจับ Error กรณีชื่อเครื่องซ้ำ
        if name:
            try:
                Computer.objects.create(
                    name=name,
                    status=status,
                    installed_software=software_obj,
                    description=description
                )
                messages.success(request, f'เพิ่มเครื่อง {name} เรียบร้อยแล้ว')
            except IntegrityError:
                # ดักจับกรณี name ซ้ำกันใน Database (เนื่องจาก unique=True)
                messages.error(request, f'ไม่สามารถเพิ่มได้! ชื่อเครื่อง "{name}" มีอยู่ในระบบแล้ว')
            
        return redirect('admin_manage_pc')


class AdminManagePcEditView(LoginRequiredMixin, View):
    # ลบ def get() ออก เพราะระบบใช้ Modal หน้าเดิมแล้ว (ลดความซ้ำซ้อนของโค้ด)

    def post(self, request, pc_id):
        # ดึงข้อมูล PC เครื่องที่ต้องการอัปเดต
        pc = get_object_or_404(Computer, id=pc_id)
        
        # รับค่าจาก Form ที่ถูกแก้ไข
        name = request.POST.get('name')
        status = request.POST.get('status')
        software_id = request.POST.get('software_id')
        description = request.POST.get('description')

        # อัปเดตข้อมูล
        if name:
            pc.name = name
        if status:
            pc.status = status
            
        if software_id:
            software_obj = Software.objects.filter(id=software_id).first()
            pc.installed_software = software_obj 
        else:
            pc.installed_software = None 
            
        if description is not None:
            pc.description = description
            
        # บันทึกข้อมูล พร้อมดักจับ Error กรณีเปลี่ยนชื่อไปซ้ำกับเครื่องอื่น
        try:
            pc.save()
            messages.success(request, f'อัปเดตข้อมูลเครื่อง {pc.name} เรียบร้อยแล้ว')
        except IntegrityError:
            messages.error(request, f'ไม่สามารถแก้ไขได้! ชื่อเครื่อง "{name}" ถูกใช้งานแล้ว')
        
        return redirect('admin_manage_pc')


class AdminManagePcDeleteView(LoginRequiredMixin, View):
    def post(self, request, pc_id):
        # ค้นหาและลบ PC ออกจากฐานข้อมูล
        pc = get_object_or_404(Computer, id=pc_id)
        pc_name = pc.name
        pc.delete()
        
        messages.success(request, f'ลบเครื่อง {pc_name} เรียบร้อยแล้ว')
        return redirect('admin_manage_pc')