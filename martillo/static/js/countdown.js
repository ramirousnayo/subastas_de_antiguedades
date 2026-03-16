function updateCountdowns() {
    const timers = document.querySelectorAll('.countdown-timer');
    
    timers.forEach(timer => {
        const targetDate = new Date(timer.dataset.date);
        const now = new Date();
        const diff = targetDate - now;
        
        if (diff <= 0) {
            timer.innerText = "CERRADA";
            timer.style.color = "var(--borgoña)";
            return;
        }
        
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);
        
        let display = "";
        if (days > 0) display += `${days}d `;
        display += `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        timer.innerText = display;
    });
}

// Update every second
setInterval(updateCountdowns, 1000);
updateCountdowns();
