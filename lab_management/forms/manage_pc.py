# ณัฐกรณ์ — Manage PC Forms
from django import forms
from lab_management.models import Computer

class PcForm(forms.ModelForm):
    class Meta:
        # ระบุว่าฟอร์มนี้เชื่อมกับ Model ไหน
        model = Computer 
        
        # เลือกฟิลด์ที่จะให้แสดงในหน้าเว็บ (last_updated ไม่ต้องใส่เพราะมันอัปเดตอัตโนมัติ)
        fields = ['name', 'status', 'installed_software', 'description']
        
        # ปรับแต่งหน้าตาของช่องกรอกข้อมูล (ใส่ class ของ Bootstrap เพื่อให้สวยงาม)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'เช่น PC-01, LAB4-01'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'installed_software': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'ระบุรายละเอียดเพิ่มเติม (ถ้ามี)...'
            }),
        }
        
        # เปลี่ยนชื่อ Label ที่จะแสดงบนหน้าเว็บให้เข้าใจง่ายขึ้น
        labels = {
            'name': 'ชื่อเครื่องคอมพิวเตอร์',
            'status': 'สถานะการใช้งานปัจจุบัน',
            'installed_software': 'ซอฟต์แวร์หลักที่ติดตั้ง',
            'description': 'รายละเอียด / หมายเหตุ',
        }