# Citizen Feedback & Complaint System

AI-Enabled Centralized QR-Based Citizen Feedback and Verified Complaint System for Pune City

## Features

- ✅ Feedback Submission (with rating, text, anonymous option)
- ✅ Complaint Registration (with proof upload, priority classification)
- ✅ Admin Dashboard (login, data viewing, complaint management)
- ✅ Duplicate Complaint Detection
- ✅ Priority Auto-Classification
- ✅ Government-themed UI (Deep Blue #0b3d91 and Saffron #ff9933)

## Deployment to Streamlit Cloud

1. **Create a GitHub Repository**
   - Create a new GitHub repository
   - Push all files from this directory to the repository

2. **Streamlit Cloud Setup**
   - Go to https://streamlit.io/cloud
   - Sign in with your GitHub account
   - Click "New App"
   - Select your repository
   - Set the app name (e.g., "pune-citizen-feedback")
   - Set the main file as `app.py`
   - Click "Deploy"

3. **Environment Variables** (if needed)
   - Streamlit Cloud will automatically detect and install dependencies from `requirements.txt`

## Database Initialization

The application includes automatic database initialization. The `setup.py` file creates the required tables and seed data.

## Credentials

- Admin username: `admin`
- Admin password: `admin123`

## License

This project is licensed under the MIT License.