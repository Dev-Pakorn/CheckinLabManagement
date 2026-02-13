const RATING_TEXTS = { 1: "แย่", 2: "พอใช้", 3: "ปานกลาง", 4: "ดี", 5: "ยอดเยี่ยม" };
document.addEventListener('DOMContentLoaded', () => {
    const stars = document.querySelectorAll('.star-rating span');
    const input = document.getElementById('ratingInput');
    const text = document.getElementById('rateText');

    stars.forEach((star, index) => {
        star.addEventListener('click', () => {
            const val = index + 1;
            input.value = val;
            text.innerText = `${RATING_TEXTS[val]} (${val}/5)`;
            stars.forEach((s, i) => {
                if (i < val) s.classList.add('active');
                else s.classList.remove('active');
            });
        });
    });
});