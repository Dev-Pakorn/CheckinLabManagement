# 🖥️ CKLab Management System

ระบบบริหารจัดการห้องปฏิบัติการคอมพิวเตอร์ พัฒนาด้วย **Django Framework**

---

## 👥 ตารางแบ่งหน้าที่ (Route Responsibility)

| ผู้รับผิดชอบ (Member) | หน้าที่หลัก (Role) | Routes ที่ดูแล |
| :--- | :--- | :--- |
| **1. ปภังกร** | **User / Kiosk System** | `path('', views.index)`<br>`path('confirm/', ...)`<br>`path('timer/', ...)`<br>`path('feedback/', ...)` |
| **2. สถาพร** | **Admin Auth** | `path('admin-portal/login/', ...)` |
| **3. ธนสิทธิ์** | **Admin Monitor** | `path('admin-portal/monitor/', ...)` |
| **4. อัษฎาวุธ** | **Booking** | `path('admin-portal/booking/', ...)` |
| **5. ณัฐกรณ์** | **PC Manage** | `path('admin-portal/manage-pc/', ...)` |
| **6. ลลิดา** | **Software** | `path('admin-portal/software/', ...)` |
| **7. เขมมิกา** | **Report** | `path('admin-portal/report/', ...)` |
| **8. ภานุวัฒน์** | **Config** | `path('admin-portal/config/', ...)` |

---

## ⚙️ วิธีรัน (Quick Start)
1. `docker compose up -d`
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. `python manage.py createsuperuser`
5. `python manage.py runserver`