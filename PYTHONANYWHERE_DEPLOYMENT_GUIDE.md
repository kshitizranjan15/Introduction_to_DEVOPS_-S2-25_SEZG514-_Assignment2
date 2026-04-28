# PythonAnywhere Deployment Guide

## ACEest Fitness & Gym - Single File Deployment

This guide walks you through deploying the complete application on PythonAnywhere with zero additional configuration needed.

---

## Step 1: Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com
2. Click "Pricing" and select the **Free Tier** (Beginner account)
3. Sign up with email and confirm
4. Your free account includes:
   - 100MB disk space
   - 1 web app with your own domain
   - 3-month data retention

---

## Step 2: Upload the Single-File Application

1. **Login to PythonAnywhere**
   - Go to https://www.pythonanywhere.com/user/login
   - Enter your credentials

2. **Open the Web Tab**
   - Click "Web" in the left sidebar
   - Click "Add a new web app"

3. **Choose Python Version**
   - Select "Python 3.10" or later
   - Click "Next"

4. **Choose Framework**
   - Select "Flask"
   - Click "Next"

5. **Choose Project Path**
   - Use: `/home/yourusername/mysite`
   - Click "Next"

---

## Step 3: Upload Application File

### Option A: Direct Upload

1. Go to "Files" tab in PythonAnywhere
2. Navigate to `/home/yourusername/mysite`
3. Delete the existing `flask_app.py`
4. Upload `pythonanywhere_app.py`
5. Rename it to `flask_app.py` (PythonAnywhere looks for this filename)

### Option B: Use Web Editor

1. In "Files" tab, create a new file `flask_app.py`
2. Copy-paste the entire content from `pythonanywhere_app.py`
3. Save the file

---

## Step 4: Configure WSGI File

1. Go to "Web" tab
2. Find "WSGI configuration file" section
3. Click the link to edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`
4. Replace the entire content with:

```python
# ============================================================
# PythonAnywhere WSGI configuration for ACEest Fitness App
# ============================================================

import sys
import os

# Add the path to your Flask app
path = '/home/yourusername/mysite'
if path not in sys.path:
    sys.path.append(path)

# Import the Flask app
from flask_app import app as application
```

5. **Save the file** (Ctrl+S or CMD+S)

---

## Step 5: Configure Static Files

1. Go to "Web" tab
2. Look for "Static files and directories" section
3. Add a mapping:
   - URL: `/static`
   - Directory: `/home/yourusername/mysite/static`
4. Click "Reload Web App" button

---

## Step 6: Set Python Version

1. In "Web" tab, find "Python version"
2. Click the version link
3. Select **Python 3.10** or **Python 3.11**
4. Click "Save"

---

## Step 7: Reload and Test

1. Click the **"Reload Web App"** button (green button at the top)
2. Wait 10-15 seconds for the app to restart
3. Your app is now live at: `https://yourusername.pythonanywhere.com`

---

## Step 8: Access Your Application

### From Browser:
- **Main App:** https://yourusername.pythonanywhere.com/
- **Health Check:** https://yourusername.pythonanywhere.com/health
- **API Info:** https://yourusername.pythonanywhere.com/api/info
- **Programs:** https://yourusername.pythonanywhere.com/programs
- **Gym Info:** https://yourusername.pythonanywhere.com/gym-info

### From Command Line (testing):
```bash
# Health check
curl https://yourusername.pythonanywhere.com/health

# List members
curl https://yourusername.pythonanywhere.com/members

# Create a workout
curl -X POST https://yourusername.pythonanywhere.com/workouts \
  -H "Content-Type: application/json" \
  -d '{"name":"Morning Run","duration_minutes":30}'
```

---

## Available API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Main web interface (HTML) |
| GET | `/health` | Health check endpoint |
| GET | `/api/info` | API information |
| GET | `/workouts` | List all workouts |
| POST | `/workouts` | Create new workout |
| GET | `/members` | List all members |
| POST | `/members` | Register new member |
| GET | `/programs` | List all training programs |
| GET | `/programs/<code>` | Get program details (FL, MG, BG) |
| POST | `/calories` | Calculate daily calorie requirements |
| GET | `/gym-info` | Get gym metrics and capacity |

---

## Troubleshooting

### 1. Error: "No module named 'flask_app'"

**Solution:**
- Ensure the file is named exactly `flask_app.py`
- Check the file is in the correct directory (`/home/yourusername/mysite`)
- Click "Reload Web App" after uploading

### 2. Error: 500 Internal Server Error

**Solution:**
- Go to "Web" tab → "Log files" → "Error log"
- Read the error message
- Common issues:
  - WSGI configuration points to wrong path
  - File permissions are incorrect
  - Python version mismatch

### 3. Workouts/Members not persisting after page reload

**Note:** This is expected behavior - the application uses in-memory storage (Python lists). Data is cleared when the app restarts.

**For persistent storage, you would need:**
- PostgreSQL database
- SQLAlchemy ORM
- Data persistence layer

(This is beyond the scope of free PythonAnywhere, which focuses on learning)

### 4. Static files not loading

**Solution:**
- Configure static file mapping in "Web" tab
- Ensure the path is correct
- Click "Reload Web App"

---

## Monitoring and Logs

1. **Access Logs:**
   - Web tab → "Log files" → "Access log"
   - Shows all HTTP requests

2. **Error Logs:**
   - Web tab → "Log files" → "Error log"
   - Shows application errors and exceptions

3. **Server Logs:**
   - Web tab → "Server log"
   - Shows startup and reload messages

---

## Limitations of Free Tier

✅ **Included:**
- 100MB disk space
- 1 web app
- Python 3.10+
- HTTPS (free SSL)
- Your own domain name

❌ **Not Included:**
- Database (PostgreSQL)
- Background tasks (Celery)
- Email sending
- Persistent file storage
- Custom domain (requires paid upgrade)

---

## Upgrading to Paid Tier

If you need persistent storage or database:

1. Go to "Account" → "Upgrade"
2. Select "Hacker (paid)" plan ($5/month)
3. Includes:
   - 512MB disk space
   - PostgreSQL database
   - Email configuration
   - Background tasks support
   - Custom domain

---

## Custom Domain (Paid Only)

1. Upgrade to paid account
2. Go to "Web" tab
3. Add custom domain in "Domain names" section
4. Point domain DNS to PythonAnywhere
5. Full setup instructions provided during configuration

---

## Performance Tips

1. **Keep the app simple** - Avoid heavy computations on free tier
2. **Optimize database queries** - Index frequently searched columns
3. **Cache responses** - Use Flask caching for repeated requests
4. **Monitor logs** - Check for slow requests and errors
5. **Reload during low traffic** - Don't reload during peak hours

---

## Backup Your Code

Since PythonAnywhere is cloud-based, always maintain a backup:

```bash
# Download your app
scp yourusername@ssh.pythonanywhere.com:/home/yourusername/mysite/flask_app.py ./

# Or use Git for version control
git clone https://github.com/yourusername/your-repo.git
```

---

## Next Steps

1. **Deploy immediately:** Follow steps 1-8 above
2. **Share your link:** Send `https://yourusername.pythonanywhere.com` to others
3. **Add features:** Enhance the app with:
   - Member authentication (Flask-Login)
   - Payment processing (Stripe)
   - Email notifications (Flask-Mail)
   - Admin dashboard (Flask-Admin)

---

## Support & Resources

- **PythonAnywhere Help:** https://help.pythonanywhere.com/
- **Flask Documentation:** https://flask.palletsprojects.com/
- **Python Docs:** https://docs.python.org/3/
- **Community Forum:** https://www.pythonanywhere.com/forums/

---

## Your Application is Ready! 🚀

**URL:** `https://yourusername.pythonanywhere.com`

Start by visiting the main page and testing the:
- ✅ Training programs selector
- ✅ Calorie calculator
- ✅ Workout logger
- ✅ Member registration
- ✅ Gym metrics dashboard

---

**Created:** April 28, 2026  
**For:** ACEest Fitness & Gym Assignment 2  
**Student:** Kshitiz Ranjan (2024TM93505)  
**Repository:** https://github.com/kshitizranjan15/Introduction_to_DEVOPS_-S2-25_SEZG514-_Assignment2
