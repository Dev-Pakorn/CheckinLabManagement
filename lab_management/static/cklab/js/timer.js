let timerInterval = null;
let syncInterval = null;

document.addEventListener('DOMContentLoaded', () => {
    const session = window.djangoData;
    if (!session) return;

    // Start Timer
    const startTime = new Date(session.startTime).getTime();
    
    function updateTimer() {
        const now = new Date().getTime();
        let diff = now - startTime;
        if (diff < 0) diff = 0;
        
        const hours = Math.floor(diff / 3600000);
        const minutes = Math.floor((diff % 3600000) / 60000);
        const seconds = Math.floor((diff % 60000) / 1000);
        
        const display = document.getElementById('timerDisplay');
        if (display) display.innerText = `${hours.toString().padStart(2,'0')}:${minutes.toString().padStart(2,'0')}:${seconds.toString().padStart(2,'0')}`;
    }
    
    timerInterval = setInterval(updateTimer, 1000);
    updateTimer();

    // Sync with Admin
    syncInterval = setInterval(() => {
        fetch(session.monitorUrl).then(res => res.json()).then(data => {
            const myPC = data.data.find(pc => String(pc.pc_id) === String(session.pcId));
            if (myPC && myPC.status === 'available') {
                window.location.href = session.indexUrl;
            }
        });
    }, 5000);
});

window.doCheckout = function() {
    if (confirm('ยืนยันการเลิกใช้งาน?')) {
        window.location.href = window.djangoData.feedbackUrl;
    }
};