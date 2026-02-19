# ลลิดา — Software
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Software
from ..forms.software import SoftwareForm

# หน้าหลัก: แสดงตาราง Software ทั้งหมด และมีฟอร์มสำหรับเพิ่มข้อมูลใหม่
class AdminSoftwareView(LoginRequiredMixin, View):
    def get(self, request):
        softwares = Software.objects.all() # ดึงข้อมูล Software ทั้งหมดจากฐานข้อมูล
        form = SoftwareForm() # สร้างฟอร์มเปล่า
        return render(request, 'cklab/admin/admin-software.html', {
            'softwares': softwares,
            'form': form
        })

    def post(self, request):
        form = SoftwareForm(request.POST)
        if form.is_valid():
            form.save() # บันทึกลงฐานข้อมูล
            return redirect('admin_software') # กลับไปหน้าเดิม (ชื่อ url ต้องตรงกับใน urls.py)
        
        softwares = Software.objects.all()
        return render(request, 'cklab/admin/admin-software.html', {
            'softwares': softwares,
            'form': form
        })

# หน้าแก้ไข: ดึงข้อมูลเดิมมาแสดงในฟอร์มเพื่อแก้ไข
class AdminSoftwareEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        software = get_object_or_404(Software, pk=pk)
        form = SoftwareForm(instance=software)
        return render(request, 'cklab/admin/admin-software-edit.html', {
            'form': form,
            'software': software
        })

    def post(self, request, pk):
        software = get_object_or_404(Software, pk=pk)
        form = SoftwareForm(request.POST, instance=software)
        if form.is_valid():
            form.save()
            return redirect('admin_software')
        return render(request, 'cklab/admin/admin-software-edit.html', {
            'form': form,
            'software': software
        })

# ระบบลบข้อมูล: (ไม่มีหน้าเว็บแยก ทำงานเบื้องหลังแล้วเด้งกลับหน้าหลัก)
class AdminSoftwareDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        software = get_object_or_404(Software, pk=pk)
        software.delete()
        return redirect('admin_software')