# Dev Guide — CKLab Management System

คู่มือสำหรับนักพัฒนาในทีม อธิบายโครงสร้างโปรเจกต์ สถาปัตยกรรม และแนวทางการเขียนโค้ด

---

## 1. Project Structure

```
CheckinLabManagement/
├── cklab_project/                # Django project config
│   ├── settings.py               # Database, apps, middleware, auth redirects
│   ├── urls.py                   # Root URL → include('lab_management.urls')
│   ├── wsgi.py
│   └── asgi.py
│
├── lab_management/               # Main application
│   ├── models.py                 # SiteConfig, Software, Booking, Status, Computer, UsageLog
│   ├── views/                    # Class-Based Views (CBV) — แยกไฟล์ตามผู้รับผิดชอบ
│   │   ├── __init__.py           # Re-export ทุก class (urls.py ใช้งานได้เหมือนเดิม)
│   │   ├── auth.py               # สถาพร: LoginView, LogoutView
│   │   ├── kiosk.py              # ปภังกร: IndexView, CheckinView, CheckoutView, StatusView, FeedbackView
│   │   ├── monitor.py            # ธนสิทธิ์: AdminMonitorView, AdminCheckinView, AdminCheckoutView
│   │   ├── booking.py            # อัษฎาวุธ: AdminBookingView, AdminBookingDetailView, AdminImportBookingView
│   │   ├── manage_pc.py          # ณัฐกรณ์: AdminManagePcView, AdminAddPcView, AdminManagePcEditView, AdminManagePcDeleteView
│   │   ├── software.py           # ลลิดา: AdminSoftwareView, AdminSoftwareEditView, AdminSoftwareDeleteView
│   │   ├── report.py             # เขมมิกา: AdminReportView, AdminReportExportView
│   │   └── config.py             # ภานุวัฒน์: AdminConfigView, AdminUserView, AdminUserEditView, AdminUserDeleteView
│   ├── forms/                    # Django Forms — แยกไฟล์ตามผู้รับผิดชอบ
│   │   ├── __init__.py           # Re-export ทุก form class
│   │   ├── kiosk.py              # ปภังกร: CheckinForm, FeedbackForm
│   │   ├── booking.py            # อัษฎาวุธ: BookingForm, ImportBookingForm
│   │   ├── manage_pc.py          # ณัฐกรณ์: PcForm
│   │   ├── software.py           # ลลิดา: SoftwareForm
│   │   ├── report.py             # เขมมิกา: ReportFilterForm
│   │   └── config.py             # ภานุวัฒน์: SiteConfigForm, AdminUserForm, AdminUserEditForm
│   ├── urls.py                   # URL patterns ทั้งหมด
│   ├── admin.py                  # Django admin registration
│   ├── apps.py
│   ├── tests.py
│   ├── migrations/
│   ├── templates/cklab/
│   │   ├── base.html             # Base template (Bootstrap 5 + Kanit font)
│   │   ├── kiosk/                # User-facing templates
│   │   │   ├── index.html        # Check-in form
│   │   │   ├── checkin.html      # Checkin page
│   │   │   ├── checkout.html     # Checkout page
│   │   │   ├── status.html       # Session status
│   │   │   └── feedback.html     # Rating & feedback
│   │   └── admin/                # Admin-facing templates
│   │       ├── admin-login.html
│   │       ├── admin-monitor.html
│   │       ├── admin-booking.html
│   │       ├── admin-booking-import.html
│   │       ├── admin-manage-pc.html
│   │       ├── admin-software.html
│   │       ├── admin-software-edit.html
│   │       ├── admin-report.html
│   │       ├── admin-users.html
│   │       ├── admin-users-edit.html
│   │       └── admin-config.html
│   └── static/cklab/
│       ├── css/
│       │   ├── main.css          # Global styles
│       │   └── admin.css         # Admin sidebar
│       ├── js/
│       │   ├── auth.js
│       │   ├── admin-login.js
│       │   ├── timer.js          # Timer + API sync ทุก 5 วินาที
│       │   └── feedback.js       # Star rating interaction
│       └── img/
│           └── ubulogo.png
│
├── .env                          # Environment variables (ไม่เข้า git)
├── .env.example                  # Template สำหรับ .env
├── .gitignore
├── docker-compose.yml            # PostgreSQL 15 (อ่านค่าจาก .env)
├── manage.py
└── README.md
```

---

## 2. Tech Stack

| Layer | Technology |
|:---|:---|
| Backend | Python 3.10+ / Django 5.0 |
| Database | PostgreSQL 15 (Docker) |
| Frontend | Django Templates + Bootstrap 5.3 + Vanilla JS |
| Font | Google Fonts — Kanit (ภาษาไทย) |
| Package Manager | uv (Astral) |

---

## 3. Environment Variables

โปรเจกต์ใช้ไฟล์ `.env` เก็บค่า config ทั้งหมด (ไม่ hardcode ใน source code)

### ไฟล์ที่เกี่ยวข้อง

| ไฟล์ | หน้าที่ | เข้า Git? |
|:---|:---|:---|
| `.env` | ค่าจริงที่ใช้รัน (มี password/secret) | ไม่ (อยู่ใน `.gitignore`) |
| `.env.example` | Template ให้คนในทีม copy ไปสร้าง `.env` | ใช่ |

### ตัวแปรทั้งหมด

| Variable | ใช้ใน | ตัวอย่าง |
|:---|:---|:---|
| `SECRET_KEY` | `settings.py` | `django-insecure-setup-key` |
| `DEBUG` | `settings.py` | `True` / `False` |
| `ALLOWED_HOSTS` | `settings.py` | `localhost,127.0.0.1` |
| `POSTGRES_DB` | `settings.py`, `docker-compose.yml` | `cklab_db` |
| `POSTGRES_USER` | `settings.py`, `docker-compose.yml` | `cklab_admin` |
| `POSTGRES_PASSWORD` | `settings.py`, `docker-compose.yml` | `secretpassword` |
| `POSTGRES_HOST` | `settings.py` | `localhost` |
| `POSTGRES_PORT` | `settings.py` | `5432` |

### วิธีตั้งค่า (สำหรับสมาชิกใหม่)

```powershell
# copy template แล้วแก้ค่าตามต้องการ
cp .env.example .env
```

---

## 4. Quick Start

```powershell
# 1. ติดตั้ง dependencies
uv venv
.\.venv\Scripts\activate
uv pip install django psycopg2-binary python-dotenv

# 2. ตั้งค่า environment
cp .env.example .env          # แก้ค่าใน .env ตามต้องการ

# 3. รัน database
docker compose up -d

# 4. migrate & สร้าง superuser
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 5. รัน server
python manage.py runserver
```

เปิดเบราว์เซอร์:
- **Kiosk (User):** `http://localhost:8000/`
- **Admin Login:** `http://localhost:8000/admin-portal/login/`
- **Django Admin:** `http://localhost:8000/django-admin/`

---

## 5. Database Models

| Model | ผู้รับผิดชอบ | หน้าที่ |
|:---|:---|:---|
| `SiteConfig` | ภานุวัฒน์ | เก็บค่า config ของระบบ |
| `Software` | ลลิดา | ข้อมูล Software ที่ติดตั้งในห้อง |
| `Booking` | อัษฎาวุธ | ข้อมูลการจองเครื่องคอมพิวเตอร์ |
| `Status` | ณัฐกรณ์ | สถานะของเครื่องคอมพิวเตอร์ |
| `Computer` | ธนสิทธิ์ | ข้อมูลเครื่องคอมพิวเตอร์แต่ละเครื่อง |
| `UsageLog` | เขมมิกา | บันทึกการใช้งานคอมพิวเตอร์ |

### SiteConfig (ผู้รับผิดชอบ: ภานุวัฒน์)

| Field | Type | Note |
|:---|:---|:---|
| — | — | รอกำหนด field โดยผู้รับผิดชอบ |

### Software (ผู้รับผิดชอบ: ลลิดา)

| Field | Type | Note |
|:---|:---|:---|
| — | — | รอกำหนด field โดยผู้รับผิดชอบ |

### Booking (ผู้รับผิดชอบ: อัษฎาวุธ)

| Field | Type | Note |
|:---|:---|:---|
| — | — | รอกำหนด field โดยผู้รับผิดชอบ |

### Status (ผู้รับผิดชอบ: ณัฐกรณ์)

| Field | Type | Note |
|:---|:---|:---|
| — | — | รอกำหนด field โดยผู้รับผิดชอบ |

### Computer (ผู้รับผิดชอบ: ธนสิทธิ์)

| Field | Type | Note |
|:---|:---|:---|
| — | — | รอกำหนด field โดยผู้รับผิดชอบ |

### UsageLog (ผู้รับผิดชอบ: เขมมิกา)

| Field | Type | Note |
|:---|:---|:---|
| — | — | รอกำหนด field โดยผู้รับผิดชอบ |

---

## 6. Views — Class-Based Views (CBV)

โปรเจกต์ใช้ CBV ทั้งหมด แยกไฟล์ตามผู้รับผิดชอบใน `lab_management/views/`

### 6.1 Kiosk Views (ไม่ต้อง Login) — ผู้รับผิดชอบ: ปภังกร

| Class | Base | HTTP Methods | URL Parameter | หน้าที่ |
|:---|:---|:---|:---|:---|
| `IndexView` | `View` | GET, POST | — | หน้าหลัก Kiosk |
| `CheckinView` | `View` | GET, POST | `pc_id` | Check-in เข้าใช้เครื่อง |
| `CheckoutView` | `View` | GET, POST | `pc_id` | Check-out ออกจากเครื่อง |
| `StatusView` | `View` | GET | `pc_id` | ตรวจสอบ session ปัจจุบัน |
| `FeedbackView` | `View` | GET, POST | `pc_id`, `software_id` | ให้คะแนน Software หลัง Check-out |

### 6.2 Admin Views (ต้อง Login — `LoginRequiredMixin`)

| Class | Base | HTTP Methods | URL Parameter | หน้าที่ | ผู้รับผิดชอบ |
|:---|:---|:---|:---|:---|:---|
| `AdminUserView` | `LoginRequiredMixin, View` | GET, POST | — | ดูรายการ / เพิ่ม Admin User | สถาพร |
| `AdminUserEditView` | `LoginRequiredMixin, View` | GET, POST | `pk` | แก้ไข Admin User | สถาพร |
| `AdminUserDeleteView` | `LoginRequiredMixin, View` | POST | `pk` | ลบ Admin User | สถาพร |
| `AdminMonitorView` | `LoginRequiredMixin, View` | GET, POST | — | Dashboard แสดง Computer ทั้งหมด | ธนสิทธิ์ |
| `AdminCheckinView` | `LoginRequiredMixin, View` | POST | `pc_id` | Admin Check-in แทน User | ธนสิทธิ์ |
| `AdminCheckoutView` | `LoginRequiredMixin, View` | POST | `pc_id` | Admin Check-out แทน User | ธนสิทธิ์ |
| `AdminBookingView` | `LoginRequiredMixin, View` | GET, POST | — | ดูรายการ / เพิ่ม Booking | อัษฎาวุธ |
| `AdminBookingDetailView` | `LoginRequiredMixin, View` | GET, POST | `pk` | ดู / แก้ไข Booking รายการ | อัษฎาวุธ |
| `AdminImportBookingView` | `LoginRequiredMixin, View` | POST | — | Import ข้อมูล Booking จาก CSV | อัษฎาวุธ |
| `AdminManagePcView` | `LoginRequiredMixin, View` | GET | — | ดูรายการ PC ทั้งหมด | ณัฐกรณ์ |
| `AdminAddPcView` | `LoginRequiredMixin, View` | GET, POST | — | เพิ่ม PC ใหม่ | ณัฐกรณ์ |
| `AdminManagePcEditView` | `LoginRequiredMixin, View` | GET, POST | `pc_id` | แก้ไขข้อมูล PC | ณัฐกรณ์ |
| `AdminManagePcDeleteView` | `LoginRequiredMixin, View` | POST | `pc_id` | ลบ PC | ณัฐกรณ์ |
| `AdminSoftwareView` | `LoginRequiredMixin, View` | GET, POST | — | ดูรายการ / เพิ่ม Software | ลลิดา |
| `AdminSoftwareEditView` | `LoginRequiredMixin, View` | GET, POST | `pk` | แก้ไข Software | ลลิดา |
| `AdminSoftwareDeleteView` | `LoginRequiredMixin, View` | POST | `pk` | ลบ Software | ลลิดา |
| `AdminReportView` | `LoginRequiredMixin, View` | GET, POST | — | รายงานการใช้งาน | เขมมิกา |
| `AdminReportExportView` | `LoginRequiredMixin, View` | GET | — | Export UsageLog เป็น CSV | เขมมิกา |
| `AdminConfigView` | `LoginRequiredMixin, View` | GET, POST | — | ดู/แก้ไข SiteConfig | ภานุวัฒน์ |

---

## 7. URL Routing

Root: `cklab_project/urls.py` → `include('lab_management.urls')`

```
# Kiosk (ไม่ต้อง Login)
/                                          → IndexView
/checkin/<pc_id>/                          → CheckinView
/checkout/<pc_id>/                         → CheckoutView
/status/<pc_id>/                           → StatusView
/feedback/<pc_id>/<software_id>/           → FeedbackView

# Auth
/admin-portal/login/                       → Django LoginView
/admin-portal/logout/                      → Django LogoutView

# Admin User Management
/admin-portal/users/                       → AdminUserView
/admin-portal/users/<pk>/edit/             → AdminUserEditView
/admin-portal/users/<pk>/delete/           → AdminUserDeleteView

# Admin Monitor
/admin-portal/monitor/                     → AdminMonitorView
/admin-portal/checkin/<pc_id>/             → AdminCheckinView   (Admin checkin แทน user)
/admin-portal/checkout/<pc_id>/            → AdminCheckoutView  (Admin checkout แทน user)

# Booking
/admin-portal/booking/                     → AdminBookingView
/admin-portal/booking/<pk>/                → AdminBookingDetailView
/admin-portal/booking/import/              → AdminImportBookingView

# Manage PC
/admin-portal/manage-pc/                   → AdminManagePcView
/admin-portal/manage-pc/add/               → AdminAddPcView
/admin-portal/manage-pc/<pc_id>/edit/      → AdminManagePcEditView
/admin-portal/manage-pc/<pc_id>/delete/    → AdminManagePcDeleteView

# Software
/admin-portal/software/                    → AdminSoftwareView
/admin-portal/software/<pk>/edit/          → AdminSoftwareEditView
/admin-portal/software/<pk>/delete/        → AdminSoftwareDeleteView

# Report
/admin-portal/report/                      → AdminReportView
/admin-portal/report/export/               → AdminReportExportView

# Config
/admin-portal/config/                      → AdminConfigView

/django-admin/                             → Django Admin Site
```

---

## 8. Authentication Flow

```
settings.py:
  LOGIN_URL           = '/admin-portal/login/'
  LOGIN_REDIRECT_URL  = '/admin-portal/monitor/'
  LOGOUT_REDIRECT_URL = '/admin-portal/login/'
```

- Admin views ใช้ `LoginRequiredMixin` — ถ้ายังไม่ login จะ redirect ไป `LOGIN_URL`
- Login/Logout ใช้ custom `LoginView` / `LogoutView` ใน `views/auth.py` (extends Django built-in)
- Kiosk views ไม่ต้อง login (เปิดใช้งานได้เลย)

---

## 9. Session Flow (Kiosk)

```
IndexView (GET)
  → แสดงหน้าหลัก Kiosk

CheckinView (POST) — /checkin/<pc_id>/
  → รับ student_id / ชื่อผู้ใช้
  → บันทึก Computer.status = 'in_use'
  → เก็บ session: session_pc_id, session_user_name, session_start_time
  → redirect → StatusView/<pc_id>/

StatusView (GET) — /status/<pc_id>/
  → อ่าน session → แสดงสถานะการใช้งานปัจจุบัน

CheckoutView (POST) — /checkout/<pc_id>/
  → ยืนยัน Check-out
  → redirect → FeedbackView/<pc_id>/<software_id>/

FeedbackView (POST) — /feedback/<pc_id>/<software_id>/
  → สร้าง UsageLog
  → reset Computer (status='available', current_user=None)
  → session.flush()
  → redirect → IndexView
```

---

## 10. Forms

โปรเจกต์ใช้ Django Forms แยกไฟล์ตามผู้รับผิดชอบใน `lab_management/forms/`

### Form Classes

| Form Class | ไฟล์ | ผู้รับผิดชอบ | ใช้กับ View |
|:---|:---|:---|:---|
| `CheckinForm` | `forms/kiosk.py` | ปภังกร | `CheckinView` |
| `FeedbackForm` | `forms/kiosk.py` | ปภังกร | `FeedbackView` |
| `BookingForm` | `forms/booking.py` | อัษฎาวุธ | `AdminBookingView`, `AdminBookingDetailView` |
| `ImportBookingForm` | `forms/booking.py` | อัษฎาวุธ | `AdminImportBookingView` |
| `PcForm` | `forms/manage_pc.py` | ณัฐกรณ์ | `AdminAddPcView`, `AdminManagePcEditView` |
| `SoftwareForm` | `forms/software.py` | ลลิดา | `AdminSoftwareView`, `AdminSoftwareEditView` |
| `ReportFilterForm` | `forms/report.py` | เขมมิกา | `AdminReportView` |
| `SiteConfigForm` | `forms/config.py` | ภานุวัฒน์ | `AdminConfigView` |
| `AdminUserForm` | `forms/config.py` | ภานุวัฒน์ | `AdminUserView` |
| `AdminUserEditForm` | `forms/config.py` | ภานุวัฒน์ | `AdminUserEditView` |

### วิธีใช้ Form ใน View

```python
# views/booking.py
from ..forms import BookingForm

class AdminBookingView(LoginRequiredMixin, View):
    def get(self, request):
        form = BookingForm()
        return render(request, 'cklab/admin/admin-booking.html', {'form': form})

    def post(self, request):
        form = BookingForm(request.POST)
        if form.is_valid():
            # บันทึกข้อมูล...
            return redirect('admin_booking')
        return render(request, 'cklab/admin/admin-booking.html', {'form': form})
```

### วิธีแสดง Form ใน Template

```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">บันทึก</button>
</form>
```

---

## 11. แนวทางการพัฒนา (สำหรับสมาชิกในทีม)

> แต่ละคนแก้ไขเฉพาะไฟล์ `views/` ของตัวเองเท่านั้น

### ขั้นตอน

**1) เขียน logic** ในไฟล์ `views/` ของตัวเอง เช่น `views/booking.py`:

```python
# views/booking.py
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..models import Booking

class AdminBookingView(LoginRequiredMixin, View):
    def get(self, request):
        bookings = Booking.objects.all()
        return render(request, 'cklab/admin/admin-booking.html', {'bookings': bookings})

    def post(self, request):
        # บันทึกข้อมูล...
        return redirect('admin_booking')
```

**2) Export class** ใน `views/__init__.py` (ถ้าเพิ่ม class ใหม่):

```python
# views/__init__.py
from .booking import AdminBookingView, AdminImportBookingView  # เพิ่ม class ใหม่ตรงนี้
```

**3) เพิ่ม URL** ใน `lab_management/urls.py` (ถ้ามี route ใหม่):

```python
path('admin-portal/booking/', views.AdminBookingView.as_view(), name='admin_booking'),
```

**4) สร้าง Template** ใน `templates/cklab/admin/`:

```html
{% extends "cklab/base.html" %}
{% block title %}Booking{% endblock %}
{% block content %}
  <!-- เนื้อหา -->
{% endblock %}
```

**5) อัปเดต Model (ถ้าจำเป็น)** ใน `lab_management/models.py` แล้วรัน:

```powershell
python manage.py makemigrations
python manage.py migrate
```

---

## 12. CBV Cheat Sheet

| ต้องการ | ใช้ Base Class | ตัวอย่าง |
|:---|:---|:---|
| render template เปล่า | `TemplateView` | — |
| render + ส่ง context | `View` + `render()` | `AdminMonitorView` |
| GET + POST custom logic | `View` + define `get()` / `post()` | `CheckinView`, `FeedbackView` |
| CRUD model | `ListView`, `CreateView`, `UpdateView`, `DeleteView` | (ยังไม่ได้ใช้) |
| ต้อง Login | เพิ่ม `LoginRequiredMixin` เป็น class แรก | `AdminMonitorView` |
| Return JSON | `View` + `JsonResponse` | — |

---

## 13. Database (Docker)

```yaml
# docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:15
    container_name: cklab_postgres
    restart: always
    env_file:
      - .env          # ใช้ POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

คำสั่งที่ใช้บ่อย:

```powershell
docker compose up -d          # เปิด database
docker compose down            # ปิด database
docker compose down -v         # ปิด + ลบข้อมูลทั้งหมด
docker ps                      # เช็คสถานะ container
```

---

## 14. Git Workflow

```powershell
# ดึงโค้ดล่าสุด
git pull origin main

# สร้าง branch ใหม่สำหรับ feature
git checkout -b feature/your-feature-name

# commit & push
git add .
git commit -m "Add your feature description"
git push origin feature/your-feature-name

# สร้าง Pull Request บน GitHub → merge เข้า main
```

### Merge branch เข้า main (local)

```powershell
# สลับไป main
git checkout main

# ดึงโค้ดล่าสุดจาก remote ก่อนเสมอ
git pull origin main

# merge branch ของตัวเองเข้า main
git merge feature/your-feature-name

# push ขึ้น remote
git push origin main
```

### แก้ Merge Conflict

```powershell
# หลังจาก merge แล้วมี conflict — เปิดไฟล์ที่ conflict แก้ไขด้วยมือ จากนั้น:
git add .
git commit -m "Resolve merge conflict"

# ถ้าต้องการยกเลิก merge (กลับสู่สถานะก่อน merge)
git merge --abort
```

### ลบ branch หลัง merge เสร็จ

```powershell
# ลบ branch local
git branch -d feature/your-feature-name

# ลบ branch remote
git push origin --delete feature/your-feature-name
```
