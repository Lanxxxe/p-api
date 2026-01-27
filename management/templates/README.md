# Portfolio Admin Dashboard Template Structure

## Overview
The admin dashboard uses a base template system with Django's template inheritance for consistent styling across all pages.

## File Structure
```
management/templates/
├── base.html           # Base template with sidebar, navbar, footer, styles
├── dashboard.html      # Dashboard page (extends base.html)
└── projects.html       # Projects page example (extends base.html)
```

## Base Template Features (base.html)

### Included Components:
- **Sidebar**: Left navigation with links (Dashboard, Projects, Blog, Settings, Logout)
- **Top Navbar**: Search bar, notifications, profile section
- **Footer**: Copyright and system version
- **Background Effects**: Matrix rain animation, scan line effect
- **Styles**: Complete Tailwind CSS + custom styles for hacker theme

### Template Blocks:
- `{% block title %}` - Page title
- `{% block extra_styles %}` - Additional CSS for specific pages
- `{% block nav_dashboard %}` - Active state for Dashboard nav item
- `{% block nav_projects %}` - Active state for Projects nav item
- `{% block nav_blog %}` - Active state for Blog nav item
- `{% block nav_settings %}` - Active state for Settings nav item
- `{% block content %}` - Main page content
- `{% block extra_scripts %}` - Additional JavaScript for specific pages

## Creating New Pages

### Basic Template:
```django
{% extends 'base.html' %}

{% block title %}Portfolio Admin | Your Page Name{% endblock %}

{% block nav_yourpage %}bg-blue-950 border-l-4 border-blue-500{% endblock %}

{% block content %}
<!-- Your page content here -->
<div class="flex items-center justify-between">
    <div>
        <h2 class="text-3xl font-bold text-blue-300 glow-text">&gt; YOUR_PAGE</h2>
        <p class="text-blue-600 terminal-text mt-1">Your page description.</p>
    </div>
</div>

<!-- Your components -->
{% endblock %}
```

### Example Usage:

#### 1. Dashboard Page (dashboard.html)
```django
{% extends 'base.html' %}
{% block title %}Portfolio Admin | Dashboard{% endblock %}
{% block nav_dashboard %}bg-blue-950 border-l-4 border-blue-500{% endblock %}
{% block content %}
    <!-- Dashboard-specific content -->
{% endblock %}
```

#### 2. Projects Page (projects.html)
```django
{% extends 'base.html' %}
{% block title %}Portfolio Admin | Projects{% endblock %}
{% block nav_projects %}bg-blue-950 border-l-4 border-blue-500{% endblock %}
{% block content %}
    <!-- Projects-specific content -->
{% endblock %}
```

## Reusable Components

### Card Component:
```html
<div class="bg-blue-950 bg-opacity-20 border border-blue-800 rounded-lg p-6 glow-border hover-glow transition-all">
    <!-- Card content -->
</div>
```

### Button Styles:
```html
<!-- Primary Button -->
<button class="bg-blue-900 hover:bg-blue-800 text-blue-300 px-4 py-2 rounded border border-blue-700 hover-glow transition-all">
    Button Text
</button>

<!-- Secondary Button -->
<button class="bg-blue-950 hover:bg-blue-900 text-blue-400 px-4 py-2 rounded border border-blue-800 hover-glow transition-all">
    Button Text
</button>
```

### Status Badges:
```html
<!-- Active -->
<span class="px-3 py-1 bg-green-900 bg-opacity-30 text-green-400 rounded-full text-xs border border-green-700">ACTIVE</span>

<!-- In Progress -->
<span class="px-3 py-1 bg-yellow-900 bg-opacity-30 text-yellow-400 rounded-full text-xs border border-yellow-700">IN PROGRESS</span>

<!-- Maintenance -->
<span class="px-3 py-1 bg-red-900 bg-opacity-30 text-red-400 rounded-full text-xs border border-red-700">MAINTENANCE</span>
```

### Section Header:
```html
<div class="flex items-center justify-between">
    <div>
        <h2 class="text-3xl font-bold text-blue-300 glow-text">&gt; SECTION_NAME</h2>
        <p class="text-blue-600 terminal-text mt-1">Section description.</p>
    </div>
</div>
```

## Style Classes Reference

### Hacker Theme Classes:
- `glow-border` - Blue glowing border
- `glow-text` - Blue glowing text shadow
- `hover-glow` - Glow effect on hover
- `pulse-glow` - Pulsing glow animation
- `terminal-text` - Monospace terminal font
- `gradient-line` - Blue horizontal gradient line

### Color Palette:
- **Background**: `bg-black`, `bg-blue-950`
- **Text**: `text-blue-300`, `text-blue-400`, `text-blue-500`, `text-blue-600`
- **Borders**: `border-blue-700`, `border-blue-800`, `border-blue-900`
- **Accents**: `text-green-400` (success), `text-yellow-400` (warning), `text-red-400` (error)

## Responsive Design
- Desktop: Full sidebar visible
- Tablet/Mobile: Collapsible sidebar with hamburger menu
- Navbar adapts to screen size (profile text hidden on mobile)

## Adding Custom JavaScript
```django
{% block extra_scripts %}
<script>
    // Your custom JavaScript here
</script>
{% endblock %}
```

## Adding Custom Styles
```django
{% block extra_styles %}
<style>
    /* Your custom CSS here */
</style>
{% endblock %}
```

## URL Configuration
Update `management/urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('projects/', views.projects, name='projects'),
    # Add more pages...
]
```

Update `management/views.py`:
```python
def dashboard(request):
    return render(request, 'dashboard.html')

def projects(request):
    return render(request, 'projects.html')
```

## Navigation Active States
To highlight the active page in the sidebar, use the appropriate block:
- Dashboard: `{% block nav_dashboard %}bg-blue-950 border-l-4 border-blue-500{% endblock %}`
- Projects: `{% block nav_projects %}bg-blue-950 border-l-4 border-blue-500{% endblock %}`
- Blog: `{% block nav_blog %}bg-blue-950 border-l-4 border-blue-500{% endblock %}`
- Settings: `{% block nav_settings %}bg-blue-950 border-l-4 border-blue-500{% endblock %}`

## Features Included
✅ Responsive sidebar with mobile menu
✅ Top navbar with search, notifications, profile
✅ Matrix rain background animation
✅ Scan line CRT effect
✅ System status indicators
✅ Custom scrollbar styling
✅ Glowing effects and animations
✅ Consistent hacker-style theme
✅ Footer with system info
