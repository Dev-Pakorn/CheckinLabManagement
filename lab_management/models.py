from django.db import models
from django.utils import timezone

# ภานุวัฒน์ - สร้าง Model สำหรับการตั้งค่าระบบ (Config) เพื่อเก็บข้อมูลการตั้งค่าต่าง ๆ ของระบบ
class SiteConfig(models.Model):
    lab_name = models.CharField(max_length=255, default="CKLab", help_text="ชื่อห้องปฏิบัติการที่จะแสดงบนเว็บไซต์")
    booking_enabled = models.BooleanField(default=True, help_text="เปิด/ปิด การใช้งานระบบจอง")
    announcement = models.TextField(blank=True, null=True, help_text="ข้อความประกาศ (แสดงบนหน้า Kiosk)")
    location = models.CharField(max_length=255, blank=True, null=True, help_text="สถานที่ตั้ง (เช่น อาคาร 4 ชั้น 2)")
    admin_on_duty = models.ForeignKey('AdminonDuty', on_delete=models.SET_NULL, blank=True, null=True, help_text="เจ้าหน้าที่ดูแลระบบประจำวัน")
    is_open = models.BooleanField(default=True, help_text="สถานะการให้บริการห้องแล็บ (เปิด/ปิด)")

class AdminonDuty(models.Model):
    contact_email = models.EmailField(blank=True, null=True, help_text="อีเมลติดต่อ (เช่น admin@example.com)")
    admin_on_duty = models.CharField(max_length=100, blank=True, null=True, help_text="เจ้าหน้าที่ดูแลระบบประจำวัน")
    contact_phone = models.CharField(max_length=50, blank=True, null=True, help_text="เบอร์โทรศัพท์ติดต่อ")

# ลลิดา - สร้าง Model สำหรับ Software เพื่อเก็บข้อมูลซอฟต์แวร์ที่ติดตั้งในห้องปฏิบัติการ
class Software(models.Model):
    TYPE_CHOICES = [
        ('Software', 'Software (ทั่วไป)'),
        ('AI', 'AI Tool (ปัญญาประดิษฐ์)'),
    ]

    name = models.CharField(max_length=100, verbose_name="ชื่อรายการ")
    version = models.CharField(max_length=50, verbose_name="แพ็กเกจ (Package)")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Software', verbose_name="ประเภท")
    expire_date = models.DateField(null=True, blank=True, verbose_name="วันหมดอายุ License")

    def __str__(self):
        return f"{self.name} ({self.version})"

# อัษฎาวุธ - สร้าง Model สำหรับการจองคอมพิวเตอร์ (Booking)
class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'รออนุมัติ'),
        ('APPROVED', 'อนุมัติแล้ว'),
        ('REJECTED', 'ไม่อนุมัติ/ยกเลิก'),
    ]

    student_id = models.CharField(max_length=20, verbose_name="รหัสนักศึกษา")
    computer = models.ForeignKey('Computer', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="เครื่องคอมพิวเตอร์")
    start_time = models.DateTimeField(verbose_name="เวลาเริ่มใช้งาน")
    end_time = models.DateTimeField(verbose_name="เวลาสิ้นสุดการใช้งาน")
    booking_date = models.DateTimeField(default=timezone.now, verbose_name="วันที่ทำการจอง")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="สถานะการจอง")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="เวลาที่ทำรายการ")

# ณัฐกรณ์ + ธนสิทธิ์ - ย้าย status เข้า Computer โดยตรง ไม่ต้องมี model Status แยก
class Computer(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'ว่าง (AVAILABLE)'),
        ('IN_USE', 'ใช้งาน (IN USE)'),
        ('RESERVED', 'จองแล้ว (RESERVED)'),
        ('MAINTENANCE', 'แจ้งซ่อม (MAINT.)'),
    ]

    name = models.CharField(max_length=20, unique=True, verbose_name="ชื่อเครื่อง")
    Software = models.ForeignKey(Software, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ซอฟต์แวร์ที่ติดตั้ง")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE', verbose_name="สถานะปัจจุบัน")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="อัปเดตสถานะล่าสุด")
    description = models.TextField(blank=True, null=True, verbose_name="รายละเอียดเพิ่มเติม")

# เขมมิกา - สร้าง Model สำหรับบันทึกการใช้งานคอมพิวเตอร์ (UsageLog)
class UsageLog(models.Model):
    user_id = models.CharField(max_length=50)
    user_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20, choices=[('student', 'Student'), ('staff', 'Staff'), ('guest', 'Guest')], null=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    user_year = models.CharField(max_length=10, null=True, blank=True)

    computer = models.CharField(max_length=20, null=True, blank=True)
    Software = models.CharField(max_length=100, null=True, blank=True)

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    satisfaction_score = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
