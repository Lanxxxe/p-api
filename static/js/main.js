// Mobile sidebar toggle
const mobileBtn = document.getElementById('mobile-menu-btn');
const sidebar   = document.getElementById('sidebar');
if (mobileBtn) {
    mobileBtn.addEventListener('click', () => sidebar.classList.toggle('-translate-x-full'));
}

// Mark active nav link based on current URL
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
        link.classList.add('active', 'text-blue-500', 'bg-[#e8edf2]');
    }
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