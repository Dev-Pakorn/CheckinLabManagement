/* timer.js - Django Integrated Version (Force Bright Text) */

let timerInterval; 
let startTime; // เก็บเวลาเริ่มใช้งานที่ได้มาจาก Backend หรือตอนโหลดหน้า
let forceEndTime = null; // สำหรับกรณีจองเวลา (ถ้ามีในอนาคต)

document.addEventListener('DOMContentLoaded', () => {
    // 1. กำหนดเวลาเริ่มต้นจากการโหลดหน้า
    // (หากต้องการให้ตรงเป๊ะ 100% ควรรับค่า startTime จาก Django Context มาใส่ตัวแปร)
    startTime = Date.now(); 

    // หากมีการดึงข้อมูลผู้ใช้จาก Session Storage (ที่เซฟไว้ตอน Check-in) ก็ยังคงทำได้เพื่อแสดงชื่อ
    const savedUser = sessionStorage.getItem('cklab_user_name');
    const userName = savedUser ? savedUser : 'กำลังใช้งาน...';
    const userNameDisplay = document.getElementById('userNameDisplay');
    if(userNameDisplay) userNameDisplay.innerText = userName;
    
    // -------------------------------------------------------------
    // ✅ อัปเดตการแสดงผลชื่อเครื่องและ Software (ถ้ามี API ดึงมาได้)
    // -------------------------------------------------------------
    // ในที่นี้สมมติให้ใช้ค่า PC_ID ที่ได้มาจาก Django Context (ที่อยู่ใน tag <script> ของ timer.html)
    const pcIdDisplay = typeof PC_ID !== 'undefined' ? PC_ID : '??';
    
    // ค่าเริ่มต้น: General Use (สีขาวปกติ text-white)
    let labelText = "General Use";
    let labelClass = "text-white fw-normal"; 

    // อัปเดต HTML: ตัวคั่นใช้สีจางได้ แต่ตัวหนังสือต้องชัด
    const pcNameEl = document.getElementById('pcNameDisplay');
    if (pcNameEl) {
        pcNameEl.innerHTML = `Station: ${pcIdDisplay} <span class="text-white-50 fw-normal mx-1">|</span> <span class="${labelClass}" style="letter-spacing: 0.5px;">${labelText}</span>`;
    }
    // -------------------------------------------------------------
    
    // เริ่มจับเวลา
    setupUnlimitedMode();
});

function setupUnlimitedMode() {
    console.log("Mode: Normal Timer (Elapsed)");
    const label = document.getElementById('timerLabel');
    if(label) label.innerText = "เวลาที่ใช้งานไปแล้ว (Elapsed Time)";
    
    updateTimer(); 
    if(timerInterval) clearInterval(timerInterval);
    timerInterval = setInterval(updateTimer, 1000); 
    
    // เช็คสถานะกับ Backend เผื่อ Admin สั่งเตะออก (Checkout จากระยะไกล)
    setInterval(syncWithAdminUpdates, 5000);
}

function updateTimer() {
    const now = Date.now();
    let diff = now - startTime;
    if (diff < 0) diff = 0;
    
    const timerDisplay = document.getElementById('timerDisplay');
    if(timerDisplay) {
        timerDisplay.innerText = formatTime(diff);
        timerDisplay.classList.remove('text-danger', 'fw-bold'); 
        timerDisplay.classList.add('text-white'); 
    }
}

async function syncWithAdminUpdates() {
    if (typeof PC_ID === 'undefined' || !PC_ID) return;

    try {
        // ใช้ API ที่เราเขียนไว้ใน views.py
        const response = await fetch(`/kiosk/api/status/${PC_ID}/`);
        if (!response.ok) return;

        const data = await response.json();

        // หากสถานะเครื่องกลายเป็น AVAILABLE หรือ MAINTENANCE แปลว่าแอดมินสั่งเคลียร์เครื่องแล้ว
        if (data.status === 'AVAILABLE' || data.status === 'MAINTENANCE') {
            alert("⚠️ Admin ได้ทำการรีเซ็ตเครื่องหรือเช็คเอาท์ให้คุณแล้ว");
            window.location.href = `/kiosk/?pc=${PC_ID}`; // กลับหน้าแรกทันที (ไม่ผ่าน feedback)
            return;
        }

    } catch (error) {
        console.error("Sync error:", error);
    }
}

function formatTime(ms) {
    const h = Math.floor(ms / 3600000).toString().padStart(2, '0');
    const m = Math.floor((ms % 3600000) / 60000).toString().padStart(2, '0');
    const s = Math.floor((ms % 60000) / 1000).toString().padStart(2, '0');
    return `${h}:${m}:${s}`;
}

function showAlert(msg) {
    const box = document.getElementById('alertBox');
    const txt = document.getElementById('alertMsg');
    if(box && txt) {
        box.classList.remove('d-none');
        txt.innerText = msg;
    }
}

function hideAlert() {
    const box = document.getElementById('alertBox');
    if(box) box.classList.add('d-none');
}

function doCheckout(isAuto = false) {
    if (!isAuto && !confirm('คุณต้องการเลิกใช้งานและออกจากระบบใช่หรือไม่?')) return;
    if (timerInterval) clearInterval(timerInterval);

    // ป้องกันการกดปุ่มซ้ำ
    const btn = document.querySelector('.btn-danger');
    if(btn) btn.disabled = true;

    // แทนที่จะใช้ DB.updatePCStatus() และ window.location.href
    // เราจะสั่งให้ Form ที่ครอบปุ่ม Checkout ไว้ ทำการ Submit ตัวเองไปยัง Django Backend (CheckoutView)
    const form = document.getElementById('checkoutForm');
    if (form) {
        form.submit();
    } else {
        alert("ไม่พบฟอร์มสำหรับ Checkout กรุณาติดต่อผู้ดูแลระบบ");
    }
}

// แนะนำเพิ่มเติม: ตอน Check-in ที่ไฟล์ auth.js ก่อนที่จะ submit form 
// ให้เพิ่ม sessionStorage.setItem('cklab_user_name', verifiedUserData.name); 
// เพื่อให้หน้า Timer ดึงชื่อมาโชว์ได้ครับ