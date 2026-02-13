from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Computer, UsageLog

# --- User / Kiosk Side ---
def index(request):
    pc_id = request.GET.get('pc', '1')
    computer, created = Computer.objects.get_or_create(pc_id=pc_id, defaults={'name': f'PC-{pc_id}', 'status': 'available'})
    
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        computer.status = 'in_use'
        computer.current_user = user_name
        computer.session_start = timezone.now()
        computer.save()
        
        request.session['session_pc_id'] = computer.id
        request.session['session_user_name'] = user_name
        request.session['session_start_time'] = computer.session_start.isoformat()
        return redirect('timer')

    return render(request, 'cklab/kiosk/index.html', {'computer': computer})

def confirm(request):
    return render(request, 'cklab/kiosk/confirm.html')

def timer(request):
    if 'session_pc_id' not in request.session:
        return redirect('index')
    context = {
        'user_name': request.session.get('session_user_name'),
        'start_time': request.session.get('session_start_time'),
        'computer': Computer.objects.get(id=request.session.get('session_pc_id'))
    }
    return render(request, 'cklab/kiosk/timer.html', context)

def feedback(request):
    if request.method == 'POST':
        pc_id = request.session.get('session_pc_id')
        if pc_id:
            try:
                computer = Computer.objects.get(id=pc_id)
                UsageLog.objects.create(
                    user_id="Unknown", 
                    user_name=request.session.get('session_user_name', 'Unknown'),
                    computer=computer,
                    start_time=computer.session_start or timezone.now(),
                    satisfaction_score=request.POST.get('rating', 0)
                )
                computer.status = 'available'
                computer.current_user = None
                computer.session_start = None
                computer.save()
            except Computer.DoesNotExist: pass
        request.session.flush()
        return redirect('index')
    return render(request, 'cklab/kiosk/feedback.html')

# --- Admin Portal Side ---
def admin_login(request): return render(request, 'cklab/admin/admin-login.html')

@login_required
def admin_monitor(request):
    computers = Computer.objects.all().order_by('pc_id')
    return render(request, 'cklab/admin/admin-monitor.html', {'computers': computers})

@login_required
def admin_booking(request): return HttpResponse("<h1>Admin Booking</h1>")
@login_required
def admin_manage_pc(request): return HttpResponse("<h1>Admin Manage PC</h1>")
@login_required
def admin_software(request): return HttpResponse("<h1>Admin Software</h1>")
@login_required
def admin_report(request): return HttpResponse("<h1>Admin Report</h1>")
@login_required
def admin_config(request): return HttpResponse("<h1>Admin Config</h1>")

# --- API ---
def api_monitor_data(request):
    computers = Computer.objects.all().order_by('pc_id')
    data = [{'pc_id': pc.pc_id, 'name': pc.name, 'status': pc.status, 'current_user': pc.current_user} for pc in computers]
    return JsonResponse({'status': 'ok', 'data': data})