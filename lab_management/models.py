from django.db import models

# ภานุวัฒน์ - สร้าง Model สำหรับการตั้งค่าระบบ (Config) เพื่อเก็บข้อมูลการตั้งค่าต่าง ๆ ของระบบ
class SiteConfig(models.Model):
    lab_name = models.CharField(max_length=255)
    
# ลลิดา - สร้าง Model สำหรับ Software เพื่อเก็บข้อมูลซอฟต์แวร์ที่ติดตั้งในห้องปฏิบัติการ
class Software(models.Model):
    pass
# อัษฎาวุธ - สร้าง Model สำหรับการจองคอมพิวเตอร์ (Booking) เพื่อเก็บข้อมูลการจองของผู้ใช้
class Booking(models.Model):
    pass
# ณัฐกรณ์ - สร้าง Model สำหรับสถานะเครื่องคอมพิวเตอร์ (Status) เพื่อระบุว่าเครื่องนั้นอยู่ในสถานะอะไร
class Status(models.Model):
    pass

# ธนสิทธิ์ - สร้าง Model สำหรับคอมพิวเตอร์ (Computer) เพื่อเก็บข้อมูลสถานะและการใช้งานของคอมพิวเตอร์แต่ละเครื่องในห้องปฏิบัติการ
class Computer(models.Model):
    pass

# เขมมิกา - สร้าง Model สำหรับบันทึกการใช้งานคอมพิวเตอร์ (UsageLog)
class UsageLog(models.Model):
    # 1. ข้อมูลผู้ใช้
    user_id = models.CharField(max_length=50)        # รหัสนักศึกษา
    user_name = models.CharField(max_length=100)      # ชื่อ-นามสกุล
    department = models.CharField(max_length=100, null=True, blank=True) # คณะ/หน่วยงาน (เพิ่มเติมเพื่อให้รายงานสมบูรณ์)
    user_year = models.CharField(max_length=10, null=True, blank=True)   # ชั้นปี (เพิ่มเติมตามความต้องการของคุณ)

    # 2. ข้อมูลอุปกรณ์และซอฟต์แวร์
    computer = models.ForeignKey('Computer', on_delete=models.SET_NULL, null=True) # เชื่อมโยงกับเครื่องที่ใช้
    # หมายเหตุ: Software สามารถดึงข้อมูลได้จากความสัมพันธ์ ManyToMany ใน Computer หรือจะเก็บชื่อ Software ที่ใช้หลักๆ ลงในฟิลด์นี้ก็ได้
    software_used = models.CharField(max_length=100, null=True, blank=True) 

    # 3. วันที่และเวลา
    start_time = models.DateTimeField()               # วันที่และเวลาเริ่มใช้งาน
    end_time = models.DateTimeField(auto_now_add=True) # วันที่และเวลาสิ้นสุด

    # 4. การประเมินและสถานะ
    pc_status_at_end = models.CharField(max_length=20, null=True, blank=True) # สถานะ PC ตอนคืนเครื่อง (เช่น ปกติ/แจ้งซ่อม)
    satisfaction_score = models.IntegerField(null=True, blank=True)           # คะแนนความพึงพอใจ 1-5
    comment = models.TextField(null=True, blank=True)                         # ข้อเสนอแนะเพิ่มเติม

    class Meta:
        ordering = ['-end_time'] # เรียงลำดับจากใหม่ไปเก่าเพื่อให้ดูรายงานง่ายขึ้น

    def __str__(self):
        return f"{self.user_name} - {self.computer.name if self.computer else 'N/A'}"