"""
ACEest Fitness & Gym - Single File Application for PythonAnywhere Deployment
Complete Flask application with embedded HTML template
All dependencies: Flask, Werkzeug (pinned versions for compatibility)

Deployment Instructions for PythonAnywhere:
1. Create account at https://www.pythonanywhere.com
2. Upload this file as 'app.py' in your web directory
3. Create a WSGI config file pointing to this app
4. Set Python version to 3.10+
5. Configure static files and reload
6. Your app will be live at https://yourusername.pythonanywhere.com
"""

from flask import Flask, jsonify, request, render_template_string, Response
import json
from datetime import datetime

# =====================================================================
# PROGRAM DATA - Derived from Aceestver versions 1.0 through 3.2.4
# =====================================================================

PROGRAMS = {
    "Fat Loss (FL)": {
        "code": "FL",
        "calorie_factor": 22,
        "color": "#e74c3c",
        "workout": (
            "Mon: Back Squat 5×5 + AMRAP Core\n"
            "Tue: EMOM 20min Assault Bike\n"
            "Wed: Bench Press + 21-15-9\n"
            "Thu: 10RFT Deadlifts / Box Jumps\n"
            "Fri: Zone 2 Cardio 30min (Active Recovery)"
        ),
        "diet": (
            "Breakfast: 3 Egg Whites + Oats Idli\n"
            "Lunch: Grilled Chicken + Brown Rice\n"
            "Dinner: Fish Curry + Millet Roti\n"
            "Target: ~2,000 kcal/day"
        ),
        "exercises": ["Back Squat", "Assault Bike", "Bench Press", "Deadlift", "Box Jumps"],
    },
    "Muscle Gain (MG)": {
        "code": "MG",
        "calorie_factor": 35,
        "color": "#2ecc71",
        "workout": (
            "Mon: Squat 5×5\n"
            "Tue: Bench Press 5×5\n"
            "Wed: Deadlift 4×6\n"
            "Thu: Front Squat 4×8\n"
            "Fri: Incline Press 4×10\n"
            "Sat: Barbell Rows 4×10"
        ),
        "diet": (
            "Breakfast: 4 Eggs + Peanut Butter Oats\n"
            "Lunch: Chicken Biryani (250g Chicken)\n"
            "Dinner: Mutton Curry + Jeera Rice\n"
            "Target: ~3,200 kcal/day"
        ),
        "exercises": ["Back Squat", "Bench Press", "Deadlift", "Front Squat", "Incline Press", "Barbell Row"],
    },
    "Beginner (BG)": {
        "code": "BG",
        "calorie_factor": 26,
        "color": "#3498db",
        "workout": (
            "Full Body Circuit (3×/week):\n"
            "- Air Squats\n"
            "- Ring Rows\n"
            "- Push-ups\n"
            "Focus: Technique Mastery & Consistency"
        ),
        "diet": (
            "Balanced Tamil Meals:\n"
            "Idli / Dosa / Rice + Dal / Chapati\n"
            "Protein Target: 120g/day"
        ),
        "exercises": ["Air Squats", "Ring Rows", "Push-ups", "Plank", "Dumbbell Row"],
    },
}

GYM_METRICS = {
    "capacity": 150,
    "area_sqft": 10000,
    "breakeven_members": 250,
}

# =====================================================================
# HTML TEMPLATE - Embedded Bootstrap UI
# =====================================================================

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ACEest Fitness & Gym</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {
            --primary: #0d6efd;
            --success: #198754;
            --danger: #dc3545;
            --warning: #ffc107;
            --dark: #212529;
        }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .navbar {
            background: linear-gradient(90deg, #0d6efd, #0056b3) !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .navbar-brand {
            font-weight: 700;
            font-size: 1.5rem;
            color: #ffc107 !important;
        }
        
        .sidebar {
            position: fixed;
            top: 56px;
            left: 0;
            height: calc(100vh - 56px);
            width: 300px;
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            color: white;
            overflow-y: auto;
            padding: 2rem 1rem;
            box-shadow: 2px 0 10px rgba(0,0,0,0.2);
        }
        
        .sidebar-section {
            margin-bottom: 2rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }
        
        .sidebar-section:last-child {
            border-bottom: none;
        }
        
        .sidebar-title {
            font-size: 0.9rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #ffc107;
            margin-bottom: 1rem;
        }
        
        .sidebar-content {
            font-size: 0.9rem;
            line-height: 1.8;
        }
        
        .sidebar-content strong {
            color: #ffffff;
        }
        
        .sidebar-content p {
            margin-bottom: 0.5rem;
        }
        
        .assignment-badge {
            display: inline-block;
            background: #ffc107;
            color: #1e40af;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-weight: 700;
            font-size: 0.75rem;
            margin-bottom: 0.5rem;
        }
        
        .student-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ffc107, #ff6b6b);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .info-item {
            display: flex;
            margin-bottom: 0.7rem;
        }
        
        .info-icon {
            width: 20px;
            margin-right: 0.7rem;
            flex-shrink: 0;
        }
        
        .main-content {
            margin-left: 300px;
            padding: 0;
        }
        
        .container-main {
            margin-top: 2rem;
            margin-bottom: 2rem;
        }
        
        .hero {
            background: linear-gradient(135deg, rgba(13, 110, 253, 0.9), rgba(5, 86, 179, 0.9));
            border-radius: 15px;
            padding: 3rem 2rem;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 2rem;
        }
        
        .hero h1 {
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .hero p {
            font-size: 1.1rem;
            opacity: 0.95;
        }
        
        .card {
            border: none;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }
        
        .card-header {
            background: linear-gradient(90deg, #0d6efd, #0056b3);
            color: white;
            font-weight: 600;
            border-radius: 10px 10px 0 0;
        }
        
        .program-card {
            border-left: 5px solid;
        }
        
        .btn-custom {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .btn-custom:hover {
            transform: scale(1.05);
        }
        
        .form-section {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .badge-custom {
            border-radius: 20px;
            padding: 0.5rem 1rem;
            font-weight: 600;
        }
        
        .list-group-item {
            border: none;
            border-bottom: 1px solid #e9ecef;
            padding: 1rem;
        }
        
        .list-group-item:last-child {
            border-bottom: none;
        }
        
        .metric-box {
            text-align: center;
            padding: 1.5rem;
            background: linear-gradient(135deg, rgba(255,193,7,0.1), rgba(255,193,7,0.2));
            border-radius: 10px;
            border-left: 5px solid #ffc107;
        }
        
        .metric-number {
            font-size: 2rem;
            font-weight: 700;
            color: #ffc107;
        }
        
        .success-message {
            animation: slideIn 0.5s ease;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .version-timeline {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-top: 1rem;
        }
        
        footer {
            background: rgba(0,0,0,0.1);
            color: white;
            text-align: center;
            padding: 1.5rem;
            margin-top: 3rem;
        }
        
        @media (max-width: 768px) {
            .sidebar {
                position: static;
                height: auto;
                width: 100%;
                padding: 1rem;
            }
            
            .main-content {
                margin-left: 0;
            }
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
            <span class="navbar-brand">💪 ACEest Fitness & Gym</span>
            <span class="navbar-text text-light ms-auto">
                <small>API Status: <span class="badge bg-success">Online</span></small>
            </span>
        </div>
    </nav>

    <!-- Sidebar -->
    <div class="sidebar">
        <div class="sidebar-section">
            <div class="assignment-badge">ASSIGNMENT 2</div>
            <div class="student-avatar">KR</div>
            <div class="sidebar-content">
                <p><strong>Kshitiz Ranjan</strong></p>
                <p style="font-size: 0.8rem; color: #ccc;">2024TM93505</p>
            </div>
        </div>

        <div class="sidebar-section">
            <div class="sidebar-title">📚 Course Details</div>
            <div class="sidebar-content">
                <div class="info-item">
                    <span class="info-icon">📖</span>
                    <span><strong>Introduction to DevOps</strong></span>
                </div>
                <div class="info-item">
                    <span class="info-icon">🏫</span>
                    <span>SEZG514</span>
                </div>
               
            </div>
        </div>

        <div class="sidebar-section">
            <div class="sidebar-title">✅ Assignment Goals</div>
            <div class="sidebar-content">
                <ul style="padding-left: 1rem; margin: 0;">
                    <li style="margin-bottom: 0.5rem;">CI/CD Pipeline</li>
                    <li style="margin-bottom: 0.5rem;">Quality Gates</li>
                    <li style="margin-bottom: 0.5rem;">Container Orchestration</li>
                    <li style="margin-bottom: 0.5rem;">Kubernetes Deployment</li>
                </ul>
            </div>
        </div>

        <div class="sidebar-section">
            <div class="sidebar-title">🛠️ Tech Stack</div>
            <div class="sidebar-content">
                <p>✓ <strong>Git</strong> — Version Control</p>
                <p>✓ <strong>Jenkins</strong> — CI/CD</p>
                <p>✓ <strong>SonarQube</strong> — Quality</p>
                <p>✓ <strong>Docker</strong> — Containerization</p>
                <p>✓ <strong>Kubernetes</strong> — Orchestration</p>
            </div>
        </div>

        <div class="sidebar-section">
            <div class="sidebar-title">🔗 Resources</div>
            <div class="sidebar-content">
                <p style="font-size: 0.8rem; word-break: break-word;">
                    <a href="https://github.com/kshitizranjan15/Introduction_to_DEVOPS_-S2-25_SEZG514-_Assignment2" target="_blank" style="color: #ffc107; text-decoration: none;">
                        📦 GitHub Repository
                    </a>
                </p>
            </div>
        </div>

        <div class="sidebar-section">
            <div class="sidebar-title">📊 Submission Status</div>
            <div class="sidebar-content">
                <p><span style="color: #2ecc71;">✓ Code Complete</span></p>
                <p><span style="color: #2ecc71;">✓ Tests Passing</span></p>
                <p><span style="color: #2ecc71;">✓ Quality Gates Met</span></p>
                <p><span style="color: #2ecc71;">✓ Deployed</span></p>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
        <!-- Navbar stays here -->
        <div class="container container-main">
        <!-- Hero Section -->
        <div class="hero">
            <h1>🏋️ ACEest Fitness & Gym Management System</h1>
            <p>Complete CI/CD Automated Platform with DevOps Integration</p>
            <p><small>Version 2.0 - Production Ready</small></p>
        </div>

        <!-- Programs Section -->
        <div class="row mb-4">
            <div class="col-12">
                <h2 class="text-white mb-3">📋 Training Programs</h2>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card program-card" style="border-left-color: #e74c3c;">
                    <div class="card-header" style="background-color: #e74c3c;">🔥 Fat Loss (FL)</div>
                    <div class="card-body">
                        <p class="text-muted"><small><strong>Calorie Factor:</strong> 22 kcal/kg</small></p>
                        <div class="badge-custom" style="background-color: #ffe5e0;">Weight Loss Focus</div>
                        <hr>
                        <p><strong>Top Exercises:</strong></p>
                        <ul class="list-unstyled small">
                            <li>✓ Back Squat</li>
                            <li>✓ Assault Bike</li>
                            <li>✓ Bench Press</li>
                            <li>✓ Deadlift</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card program-card" style="border-left-color: #2ecc71;">
                    <div class="card-header" style="background-color: #2ecc71;">💪 Muscle Gain (MG)</div>
                    <div class="card-body">
                        <p class="text-muted"><small><strong>Calorie Factor:</strong> 35 kcal/kg</small></p>
                        <div class="badge-custom" style="background-color: #e5ffe5;">Hypertrophy Focus</div>
                        <hr>
                        <p><strong>Top Exercises:</strong></p>
                        <ul class="list-unstyled small">
                            <li>✓ Back Squat</li>
                            <li>✓ Bench Press</li>
                            <li>✓ Deadlift</li>
                            <li>✓ Barbell Row</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card program-card" style="border-left-color: #3498db;">
                    <div class="card-header" style="background-color: #3498db;">🌱 Beginner (BG)</div>
                    <div class="card-body">
                        <p class="text-muted"><small><strong>Calorie Factor:</strong> 26 kcal/kg</small></p>
                        <div class="badge-custom" style="background-color: #e5f2ff;">Foundation Building</div>
                        <hr>
                        <p><strong>Top Exercises:</strong></p>
                        <ul class="list-unstyled small">
                            <li>✓ Air Squats</li>
                            <li>✓ Ring Rows</li>
                            <li>✓ Push-ups</li>
                            <li>✓ Plank</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <!-- Calorie Calculator -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="form-section">
                    <h3 class="mb-3">🔢 Calorie Calculator</h3>
                    <form id="calorieForm">
                        <div class="mb-3">
                            <label class="form-label">Body Weight (kg)</label>
                            <input type="number" class="form-control" id="weightInput" placeholder="e.g., 75" min="1" step="0.1">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Training Program</label>
                            <select class="form-select" id="programSelect">
                                <option value="">-- Select Program --</option>
                                <option value="FL">Fat Loss (FL)</option>
                                <option value="MG">Muscle Gain (MG)</option>
                                <option value="BG">Beginner (BG)</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary btn-custom w-100">Calculate Daily Calories</button>
                    </form>
                    <div id="calorieResult" class="mt-3"></div>
                </div>
            </div>

            <!-- Workout Log -->
            <div class="col-md-6">
                <div class="form-section">
                    <h3 class="mb-3">🏃 Log Workout</h3>
                    <form id="workoutForm">
                        <div class="mb-3">
                            <label class="form-label">Workout Name</label>
                            <input type="text" class="form-control" id="workoutName" placeholder="e.g., Morning Run">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Duration (minutes)</label>
                            <input type="number" class="form-control" id="workoutDuration" placeholder="e.g., 30" min="1">
                        </div>
                        <button type="submit" class="btn btn-success btn-custom w-100">Log Workout</button>
                    </form>
                    <div id="workoutList" class="mt-3">
                        <h5>Recent Workouts</h5>
                        <ul id="workoutItems" class="list-group"></ul>
                    </div>
                </div>
            </div>
        </div>

        <!-- Member Registration -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="form-section">
                    <h3 class="mb-3">👤 Register Member</h3>
                    <form id="memberForm">
                        <div class="mb-3">
                            <label class="form-label">Full Name</label>
                            <input type="text" class="form-control" id="memberName" placeholder="e.g., John Doe">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Email</label>
                            <input type="email" class="form-control" id="memberEmail" placeholder="e.g., john@example.com">
                        </div>
                        <button type="submit" class="btn btn-warning btn-custom w-100">Register Member</button>
                    </form>
                </div>
            </div>

            <!-- Members List -->
            <div class="col-md-6">
                <div class="form-section">
                    <h3 class="mb-3">👥 Active Members</h3>
                    <ul id="membersList" class="list-group"></ul>
                </div>
            </div>
        </div>

        <!-- Gym Metrics -->
        <div class="row mb-4">
            <div class="col-12">
                <h3 class="text-white mb-3">📊 Gym Metrics & Capacity</h3>
            </div>
            <div class="col-md-4">
                <div class="metric-box">
                    <div class="metric-number">150</div>
                    <p><strong>Max Capacity</strong></p>
                    <small class="text-muted">Members at Full Capacity</small>
                </div>
            </div>
            <div class="col-md-4">
                <div class="metric-box">
                    <div class="metric-number">10,000</div>
                    <p><strong>Gym Area</strong></p>
                    <small class="text-muted">Square Feet</small>
                </div>
            </div>
            <div class="col-md-4">
                <div class="metric-box">
                    <div class="metric-number">250</div>
                    <p><strong>Break-Even</strong></p>
                    <small class="text-muted">Required Members</small>
                </div>
            </div>
        </div>

        <!-- Health Status -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="form-section" style="background: linear-gradient(135deg, #e5ffe5, #f0fff0);">
                    <h3 class="mb-3">✅ System Health</h3>
                    <p><strong>Status:</strong> <span class="badge bg-success">HEALTHY</span></p>
                    <p><strong>Last Updated:</strong> <span id="healthTime"></span></p>
                    <p><strong>API Endpoints Available:</strong> <span class="badge bg-info">6</span></p>
                </div>
            </div>
        </div>
        </div>
        <!-- End main content div -->
    </div>

    <!-- Footer -->
    <footer>
        <p>&copy; 2025 ACEest Fitness & Gym | DevOps Assignment 2 | Kshitiz Ranjan (2024TM93505)</p>
        <p><small>Repository: https://github.com/kshitizranjan15/Introduction_to_DEVOPS_-S2-25_SEZG514-_Assignment2</small></p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const API_BASE = window.location.origin;

        // Update health time
        document.getElementById('healthTime').textContent = new Date().toLocaleString();

        // Calorie Calculator
        document.getElementById('calorieForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const weight = document.getElementById('weightInput').value;
            const program = document.getElementById('programSelect').value;
            
            if (!weight || !program) {
                alert('Please fill in all fields');
                return;
            }

            try {
                const res = await fetch(API_BASE + '/calories', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ weight_kg: parseFloat(weight), program_code: program })
                });
                const data = await res.json();
                if (res.ok) {
                    document.getElementById('calorieResult').innerHTML = `
                        <div class="alert alert-success success-message">
                            <strong>Daily Calorie Target:</strong> <span style="font-size: 1.5rem; color: #198754;">${data.estimated_daily_kcal} kcal</span><br>
                            <small>Program: ${data.program} | Weight: ${data.weight_kg}kg | Factor: ${data.calorie_factor}</small>
                        </div>
                    `;
                } else {
                    alert('Error: ' + data.error);
                }
            } catch (err) {
                alert('Error calculating calories: ' + err);
            }
        });

        // Workout Logger
        document.getElementById('workoutForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('workoutName').value;
            const duration = document.getElementById('workoutDuration').value;
            
            if (!name || !duration) {
                alert('Please fill in all fields');
                return;
            }

            try {
                const res = await fetch(API_BASE + '/workouts', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, duration_minutes: parseInt(duration) })
                });
                const data = await res.json();
                if (res.ok) {
                    document.getElementById('workoutName').value = '';
                    document.getElementById('workoutDuration').value = '';
                    loadWorkouts();
                } else {
                    alert('Error: ' + data.error);
                }
            } catch (err) {
                alert('Error logging workout: ' + err);
            }
        });

        // Load Workouts
        async function loadWorkouts() {
            try {
                const res = await fetch(API_BASE + '/workouts');
                const workouts = await res.json();
                const html = workouts.map(w => `
                    <li class="list-group-item">
                        <strong>${w.name}</strong> - <span class="badge bg-primary">${w.duration_minutes} min</span>
                    </li>
                `).join('');
                document.getElementById('workoutItems').innerHTML = html || '<li class="list-group-item text-muted">No workouts logged yet</li>';
            } catch (err) {
                console.error('Error loading workouts:', err);
            }
        }

        // Member Registration
        document.getElementById('memberForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('memberName').value;
            const email = document.getElementById('memberEmail').value;
            
            if (!name || !email) {
                alert('Please fill in all fields');
                return;
            }

            try {
                const res = await fetch(API_BASE + '/members', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email })
                });
                const data = await res.json();
                if (res.ok) {
                    document.getElementById('memberName').value = '';
                    document.getElementById('memberEmail').value = '';
                    loadMembers();
                } else {
                    alert('Error: ' + data.error);
                }
            } catch (err) {
                alert('Error registering member: ' + err);
            }
        });

        // Load Members
        async function loadMembers() {
            try {
                const res = await fetch(API_BASE + '/members');
                const members = await res.json();
                const html = members.map(m => `
                    <li class="list-group-item">
                        <strong>${m.name}</strong><br>
                        <small class="text-muted">📧 ${m.email}</small>
                    </li>
                `).join('');
                document.getElementById('membersList').innerHTML = html || '<li class="list-group-item text-muted">No members registered yet</li>';
            } catch (err) {
                console.error('Error loading members:', err);
            }
        }

        // Load data on page load
        document.addEventListener('DOMContentLoaded', () => {
            loadWorkouts();
            loadMembers();
        });
    </script>
</body>
</html>
'''

# =====================================================================
# FLASK APP CREATION AND ROUTES
# =====================================================================

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # In-memory stores
    app.config.setdefault("WORKOUTS", [])
    app.config.setdefault("MEMBERS", [])

    @app.route("/favicon.ico")
    def favicon():
        """Return SVG favicon to avoid 404 errors."""
        svg = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            '<rect width="100%" height="100%" fill="#0d6efd"/>'
            '<text x="50%" y="50%" font-size="32" fill="white" dy=".35em" text-anchor="middle">A</text>'
            '</svg>'
        )
        return Response(svg, mimetype='image/svg+xml')

    @app.route("/", methods=["GET"])
    def index():
        """Serve the main HTML interface."""
        return render_template_string(HTML_TEMPLATE)

    @app.route("/health", methods=["GET"])
    def health():
        """Health check endpoint."""
        return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()}), 200

    @app.route("/api/info", methods=["GET"])
    def info():
        """API information endpoint."""
        return jsonify({
            "service": "ACEest Fitness & Gym API",
            "version": "2.0",
            "status": "operational",
            "timestamp": datetime.now().isoformat()
        }), 200

    @app.route("/workouts", methods=["GET", "POST"])
    def workouts():
        """Get all workouts or create a new one."""
        if request.method == "GET":
            return jsonify(app.config["WORKOUTS"]), 200

        payload = request.get_json() or {}
        name = payload.get("name")
        duration = payload.get("duration_minutes")

        # Validation
        if not name or not isinstance(name, str) or not name.strip():
            return jsonify({"error": "name is required and must be a non-empty string"}), 400
        if duration is None or not isinstance(duration, (int, float)) or duration <= 0:
            return jsonify({"error": "duration_minutes must be a positive number"}), 400

        workout = {
            "id": len(app.config["WORKOUTS"]) + 1,
            "name": name.strip(),
            "duration_minutes": duration,
            "created_at": datetime.now().isoformat()
        }
        app.config["WORKOUTS"].append(workout)
        return jsonify(workout), 201

    @app.route("/members", methods=["GET", "POST"])
    def members():
        """Get all members or register a new member."""
        if request.method == "GET":
            return jsonify(app.config["MEMBERS"]), 200

        payload = request.get_json() or {}
        name = payload.get("name")
        email = payload.get("email")

        # Validation
        if not name or not isinstance(name, str) or not name.strip():
            return jsonify({"error": "name is required and must be a non-empty string"}), 400
        if not email or not isinstance(email, str) or "@" not in email:
            return jsonify({"error": "email is required and must be valid"}), 400

        member = {
            "id": len(app.config["MEMBERS"]) + 1,
            "name": name.strip(),
            "email": email.lower(),
            "created_at": datetime.now().isoformat()
        }
        app.config["MEMBERS"].append(member)
        return jsonify(member), 201

    @app.route("/programs", methods=["GET"])
    def programs():
        """Get all training programs."""
        return jsonify(PROGRAMS), 200

    @app.route("/programs/<program_code>", methods=["GET"])
    def program_detail(program_code):
        """Get details for a specific program."""
        for name, data in PROGRAMS.items():
            if data["code"].upper() == program_code.upper():
                return jsonify({"program": name, **data}), 200
        return jsonify({"error": f"Program '{program_code}' not found. Valid codes: FL, MG, BG"}), 404

    @app.route("/calories", methods=["POST"])
    def calories():
        """Calculate daily calorie requirements."""
        payload = request.get_json() or {}
        weight = payload.get("weight_kg")
        program_code = payload.get("program_code", "").upper()

        # Validation
        if weight is None or not isinstance(weight, (int, float)) or weight <= 0:
            return jsonify({"error": "weight_kg must be a positive number"}), 400

        # Find matching program
        matched = None
        for name, data in PROGRAMS.items():
            if data["code"].upper() == program_code:
                matched = (name, data)
                break

        if not matched:
            valid_codes = ', '.join(d['code'] for d in PROGRAMS.values())
            return jsonify({"error": f"program_code must be one of: {valid_codes}"}), 400

        program_name, program_data = matched
        estimated = round(weight * program_data["calorie_factor"])
        
        return jsonify({
            "weight_kg": weight,
            "program": program_name,
            "calorie_factor": program_data["calorie_factor"],
            "estimated_daily_kcal": estimated,
            "timestamp": datetime.now().isoformat()
        }), 200

    @app.route("/gym-info", methods=["GET"])
    def gym_info():
        """Get gym capacity and metrics."""
        return jsonify(GYM_METRICS), 200

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({"error": "Endpoint not found", "message": str(error)}), 404

    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors."""
        return jsonify({"error": "Internal server error", "message": str(error)}), 500

    return app


# =====================================================================
# DEPLOYMENT CONFIGURATION
# =====================================================================

# For PythonAnywhere WSGI
app = create_app()

# For local testing
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
