# ลลิดา — Software Forms
from django import forms
from ..models import Software

class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ['name', 'version', 'type', 'expire_date'] # เอาแค่ฟิลด์ที่มีในโปรเจกต์
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'editName', 'placeholder': 'เช่น ChatGPT, Microsoft Office'}),
            'version': forms.TextInput(attrs={'class': 'form-control', 'id': 'editVersion', 'placeholder': 'เช่น Plus, Pro, 2024'}),
            'type': forms.Select(attrs={'class': 'form-select', 'id': 'editType'}),
            'expire_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'editExpire', 'type': 'date'}),
        }