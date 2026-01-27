// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const sidebar = document.getElementById('sidebar');

mobileMenuBtn.addEventListener('click', () => {
    sidebar.classList.toggle('-translate-x-full');
});

// Close sidebar when clicking outside on mobile
document.addEventListener('click', (e) => {
    if (window.innerWidth < 1024 && 
        !sidebar.contains(e.target) && 
        !mobileMenuBtn.contains(e.target) &&
        !sidebar.classList.contains('-translate-x-full')) {
        sidebar.classList.add('-translate-x-full');
    }
});

// Update time every second
setInterval(() => {
    const now = new Date();
    const timeStr = now.toISOString().slice(0, 19).replace('T', ' ');
}, 1000);