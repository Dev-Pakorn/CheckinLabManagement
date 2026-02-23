# lab_management/views/manage_pc.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404

# นำเข้า Models ที่ต้องใช้
from ..models import Computer, Software

class AdminManagePcView(LoginRequiredMixin, View):
    def get(self, request):
        # ดึงข้อมูล Computer ทั้งหมด (อาจจะเรียงตามชื่อเครื่อง)
        pcs = Computer.objects.all().order_by('name')
        # ดึงข้อมูล Software ทั้งหมดเพื่อเตรียมไว้แสดงใน Dropdown/Modal
        softwares = Software.objects.all()
        
        context = {
            'pcs': pcs,
            'softwares': softwares,
        }
        return render(request, 'cklab/admin/admin-manage-pc.html', context)


class AdminAddPcView(LoginRequiredMixin, View):
    def get(self, request):
        # กรณีมีการเข้าผ่าน GET สามารถ redirect กลับไปหน้าหลัก Manage PC ได้เลย
        # สมมติว่าตั้งชื่อ url path ไว้ว่า 'manage_pc_list'
        return redirect('manage_pc_list') 

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

        # สร้างข้อมูล PC ใหม่
        if name:
            Computer.objects.create(
                name=name,
                status=status,
                Software=software_obj, # ใช้ 'S' ตัวใหญ่ตามที่กำหนดใน Model
                description=description
            )
            
        return redirect('manage_pc_list')


class AdminManagePcEditView(LoginRequiredMixin, View):
    def get(self, request, pc_id):
        # ดึงข้อมูล PC เครื่องที่ต้องการแก้ไข (ถ้าส่งมาผิดให้ขึ้น 404)
        pc = get_object_or_404(Computer, id=pc_id)
        softwares = Software.objects.all()
        
        context = {
            'pc': pc,
            'softwares': softwares,
        }
        # หากใช้หน้าแยกสำหรับแก้ไข สามารถ render ไปหน้าที่ต้องการได้
        # แต่ถ้าใช้ Modal ในหน้าเดียวกันอาจไม่ค่อยได้ใช้ get() ตรงนี้
        return render(request, 'cklab/admin/admin-manage-pc-edit.html', context)

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
            pc.Software = software_obj
        else:
            pc.Software = None # เคลียร์ค่าหากไม่มีการเลือกซอฟต์แวร์
            
        if description is not None:
            pc.description = description
            
        pc.save()
        
        return redirect('manage_pc_list')


class AdminManagePcDeleteView(LoginRequiredMixin, View):
    def post(self, request, pc_id):
        # ค้นหาและลบ PC ออกจากฐานข้อมูล
        pc = get_object_or_404(Computer, id=pc_id)
        pc.delete()
        
        return redirect('manage_pc_list')