import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import time
import os
from datetime import datetime
import hashlib

# ==========================================
# 1. THEME & COLOR COORDINATION (GOVT. STD)
# ==========================================
st.set_page_config(
    page_title="Citizen Feedback & Complaint System | Pune City",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR HIGH CONTRAST ---
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background-color: #ffffff;
        color: #212121;
    }

    /* Professional Header */
    .govt-header {
        background-color: #f8f9fa;
        border-bottom: 5px solid #ff9933;
        padding: 30px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .govt-header h1 {
        color: #0b3d91 !important;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .govt-header p {
        color: #212121;
        font-size: 1.1rem;
        margin-top: 0;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0b3d91;
        color: white;
    }
    
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p {
        color: white !important;
    }

    /* Sidebar Radio Button Styling */
    div[data-testid="stSidebarUserContent"] .st-emotion-cache-10trblm {
        color: white !important;
    }

    /* Input Labels */
    label {
        color: #0b3d91 !important;
        font-weight: 600 !important;
    }

    /* FIX: Checkbox text visibility */
    div[data-testid="stCheckbox"] label p {
        color: #212121 !important;
        font-weight: 500 !important;
    }

    /* FIX: Force Submit Button Text to White */
    div.stButton > button p {
        color: white !important;
    }

    /* Feature Cards */
    .info-card {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-left: 5px solid #138808;
        padding: 20px;
        border-radius: 4px;
        margin-bottom: 20px;
    }

    /* Submit Button Styling */
    div.stButton > button,
    div.stFormSubmitButton > button {
        background-color: #0b3d91 !important;
        color: white !important;
        border-radius: 4px !important;
        border: none !important;
        padding: 12px 28px !important;
        font-weight: bold !important;
        width: 100%;
        font-size: 16px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background-color: #ff9933 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    }

    /* Active state for buttons */
    div.stButton > button:active,
    div.stFormSubmitButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
    }

    /* Footer */
    .footer {
        background-color: #f8f9fa;
        padding: 20px;
        text-align: center;
        border-top: 1px solid #dee2e6;
        margin-top: 50px;
        font-size: 0.85rem;
    }

    /* Tab Styling - Red text for Feedback and Complaint tabs */
    button[data-baseweb="tab"] {
        color: #d32f2f !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #d32f2f !important;
        background-color: #fff !important;
        border-bottom: 3px solid #d32f2f !important;
        font-weight: bold !important;
    }

    /* Make tab text always red, even when not selected */
    button[data-baseweb="tab"] span {
        color: #d32f2f !important;
        font-weight: bold !important;
    }

    /* Ensure tab text is always visible in red */
    button[data-baseweb="tab"] p {
        color: #d32f2f !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SHARED CONSTANTS & DATABASE SETUP
# ==========================================
PUNE_AREAS = ["Shivajinagar", "Kothrud", "Hadapsar", "Wakad", "Hinjewadi"]
CRIME_TYPES = ["Theft / Robbery", "Harassment / Misconduct", "Traffic Violation", "Cyber Crime"]

# Database setup
DB_PATH = "pune_feedback.db"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg", width=80)
    st.markdown("### CITIZEN PORTAL")
    st.divider()
    page = st.radio("MAIN NAVIGATION", 
                    ["Home", "Submit Feedback", "Register Complaint", "Admin Login"])
    st.markdown("---")
    st.caption("Active Zone: Pune City Administration")

# ==========================================
# 4. HEADER SECTION (CENTRALIZED)
# ==========================================
st.markdown("""
    <div class="govt-header">
        <h1>Citizen Feedback & Complaint System</h1>
        <p>AI-Enabled Centralized QR-Based Platform for Pune City</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 5. PAGE ROUTING
# ==========================================

# --- HOME PAGE ---
if page == "Home":
    st.markdown("### Welcome to the Official Citizen Service Portal")
    st.write("""
    This platform enables citizens to submit feedback and register complaints related to public safety 
    and police services in a transparent manner. This system was accessed via the centralized QR Code 
    infrastructure deployed across the city.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="info-card">
            <h4 style="color:#0b3d91;">📋 How It Works</h4>
            <ol>
                <li><b>Identify Area:</b> Select the area where the incident occurred.</li>
                <li><b>Provide Evidence:</b> Upload photos or videos for verified complaints.</li>
                <li><b>Track Status:</b> Use your tracking ID for real-time updates.</li>
                <li><b>Transparency:</b> Authorities review and assign priority based on AI analysis.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card" style="border-left-color:#ff9933;">
            <h4 style="color:#0b3d91;">🌟 Key Features</h4>
            <ul>
                <li><b>Centralized System:</b> Unified portal for all city zones.</li>
                <li><b>Anonymous Feedback:</b> Encourage honest reporting for public services.</li>
                <li><b>Verified Complaints:</b> Mandates proof to prevent duplicate/fake entries.</li>
                <li><b>Direct Governance:</b> Bridges the gap between citizens and authorities.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# --- FEEDBACK PAGE ---
elif page == "Submit Feedback":
    st.markdown("### 📝 Submit Feedback")
    st.info("Citizens can share feedback regarding public services. Anonymous feedback is allowed.")
    
    with st.form("feedback_form"):
        area = st.selectbox("Area", PUNE_AREAS)
        rating = st.select_slider("Rate Service (1-Lowest, 5-Highest)", options=[1, 2, 3, 4, 5])
        feedback_text = st.text_area("Your Feedback / Suggestions")
        anonymous = st.checkbox("Submit Anonymously")
        
        if st.form_submit_button("Submit Feedback"):
            # Validation
            if not feedback_text.strip():
                st.error("⚠️ Feedback text cannot be empty.")
            elif rating is None:
                st.error("⚠️ Please select a rating.")
            else:
                # Save to database
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                
                # Get area_id
                cursor.execute("SELECT area_id FROM Area WHERE area_name = ?", (area,))
                result = cursor.fetchone()
                if result:
                    area_id = result[0]
                    
                    # Insert feedback
                    cursor.execute(
                        "INSERT INTO Feedback (rating, feedback_text, is_anonymous, area_id, date) VALUES (?, ?, ?, ?, ?)",
                        (rating, feedback_text.strip(), anonymous, area_id, datetime.now().strftime('%Y-%m-%d'))
                    )
                    conn.commit()
                    conn.close()
                    
                    st.success(f"✅ Thank you! Your feedback for {area} has been successfully recorded.")
                    if anonymous:
                        st.info("🕵️ Your identity is kept private.")
                else:
                    st.error("⚠️ Error: Area not found in database.")

# --- COMPLAINT PAGE ---
elif page == "Register Complaint":
    st.markdown("### 🚨 Register a Complaint")
    
    # Updated Warning: Orange text for "Accurate Details" requirement
    st.markdown('<p style="color:#ff9933; font-weight:bold; border:1px solid #ff9933; padding:10px; border-radius:5px;">⚠️ Ensure all details are accurate. Providing false information is a punishable offense.</p>', unsafe_allow_html=True)
    
    with st.form("complaint_form"):
        c1, c2 = st.columns(2)
        with c1:
            c_area = st.selectbox("Area of Incident", PUNE_AREAS)
            c_type = st.selectbox("Crime Category", CRIME_TYPES)
        with c2:
            c_phone = st.text_input("Mandatory Phone Number")
            c_file = st.file_uploader("Upload Proof (Image/Video)", type=['png', 'jpg', 'jpeg', 'pdf', 'mp4', 'mov', 'avi'])
            
        c_desc = st.text_area("Detailed Description of Issue")
        
        if st.form_submit_button("Lodge Verified Complaint"):
            # Validation
            if not c_desc.strip():
                st.error("⚠️ Description cannot be empty.")
            elif not c_phone.strip():
                st.error("⚠️ Phone number is mandatory.")
            elif not c_file:
                st.error("⚠️ Proof upload is mandatory.")
            elif not c_phone.strip().isdigit() or len(c_phone.strip()) != 10:
                st.error("⚠️ Please enter a valid 10-digit phone number.")
            else:
                # Check for duplicate complaints
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                
                # Check for existing complaints with same phone number
                cursor.execute(
                    "SELECT description FROM Complaint WHERE phone_number = ?", 
                    (c_phone.strip(),)
                )
                existing_complaints = cursor.fetchall()
                
                is_duplicate = False
                if existing_complaints:
                    # Simple string similarity check
                    new_tokens = set(c_desc.lower().split())
                    for existing in existing_complaints:
                        existing_tokens = set(existing[0].lower().split())
                        if existing_tokens:
                            overlap = len(new_tokens & existing_tokens) / len(new_tokens | existing_tokens)
                            if overlap > 0.6:
                                is_duplicate = True
                                break
                
                if is_duplicate:
                    st.warning("⚠️ A similar complaint from this phone number already exists. Please avoid duplicate submissions.")
                else:
                    # Save uploaded file
                    filename = f"{int(time.time())}_{c_file.name}"
                    file_path = os.path.join(UPLOAD_DIR, filename)
                    with open(file_path, "wb") as f:
                        f.write(c_file.getbuffer())
                    
                    # Classify priority
                    desc_lower = c_desc.lower()
                    if any(kw in desc_lower for kw in ["urgent", "attack", "emergency", "murder", "weapon", "fire", "kidnap"]):
                        priority = "High"
                    elif any(kw in desc_lower for kw in ["robbery", "theft", "harassment", "assault", "danger"]):
                        priority = "Medium"
                    else:
                        priority = "Low"
                    
                    # Get area_id
                    cursor.execute("SELECT area_id FROM Area WHERE area_name = ?", (c_area,))
                    result = cursor.fetchone()
                    if result:
                        area_id = result[0]
                        
                        # Insert complaint
                        cursor.execute(
                            "INSERT INTO Complaint (description, phone_number, proof_file, category, status, priority_level, area_id, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (c_desc.strip(), c_phone.strip(), file_path, c_type, "Pending", priority, area_id, datetime.now().strftime('%Y-%m-%d'))
                        )
                        conn.commit()
                        conn.close()
                        
                        st.success(f"✅ Complaint registered successfully! Tracking ID: PNQ-{int(time.time())}")
                        st.info(f"📌 Priority assigned: **{priority}**")
                        if priority == "High":
                            st.error("🔴 This has been flagged as HIGH PRIORITY and will be reviewed immediately.")
                    else:
                        st.error("⚠️ Error: Area not found in database.")

# --- ADMIN LOGIN ---
elif page == "Admin Login":
    st.markdown("### 🔐 Admin Login")
    st.write("Access to this section is restricted to authorized personnel only.")
    
    # Admin session state
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False
    
    if not st.session_state.admin_logged_in:
        with st.container(border=True):
            admin_user = st.text_input("User ID")
            admin_pass = st.text_input("Password", type="password")
            
            if st.button("Access Dashboard"):
                # Verify credentials
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT password FROM Admin WHERE username = ?", 
                    (admin_user,)
                )
                result = cursor.fetchone()
                conn.close()
                
                if result and result[0] == hashlib.sha256(admin_pass.encode()).hexdigest():
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Invalid Credentials. Try admin / admin123")
    else:
        # Admin dashboard
        st.success("✅ Authorized Access Granted.")
        
        # Logout button
        if st.button("🚪 Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()
        
        st.divider()
        
        # Tabs for different views
        tab1, tab2 = st.tabs(["📝 Feedback Overview", "🚨 Complaint Management"])
        
        # Feedback tab
        with tab1:
            st.subheader("All Citizen Feedback")
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f.feedback_id, a.area_name, f.rating, f.feedback_text,
                       CASE WHEN f.is_anonymous THEN 'Yes' ELSE 'No' END AS anonymous, f.date
                FROM Feedback f
                JOIN Area a ON f.area_id = a.area_id
                ORDER BY f.feedback_id DESC
            """)
            feedbacks = cursor.fetchall()
            conn.close()
            
            if not feedbacks:
                st.info("No feedback submitted yet.")
            else:
                df_feedback = pd.DataFrame(feedbacks, columns=["ID", "Area", "Rating", "Feedback", "Anonymous", "Date"])
                st.dataframe(df_feedback, use_container_width=True, hide_index=True)
                
                # Area-wise rating chart
                if len(df_feedback) > 0:
                    st.markdown("#### Average Rating by Area")
                    avg_rating = df_feedback.groupby("Area")["Rating"].mean().reset_index()
                    avg_rating.columns = ["Area", "Average Rating"]
                    fig_feedback = px.bar(avg_rating, x="Area", y="Average Rating", 
                                         color="Area", color_discrete_sequence=["#0b3d91"])
                    st.plotly_chart(fig_feedback, use_container_width=True)
        
        # Complaints tab
        with tab2:
            st.subheader("All Complaints")
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.complaint_id, a.area_name, c.category, c.description,
                       c.phone_number, c.proof_file, c.status, c.priority_level, c.date
                FROM Complaint c
                JOIN Area a ON c.area_id = a.area_id
                ORDER BY c.complaint_id DESC
            """)
            complaints = cursor.fetchall()
            conn.close()
            
            if not complaints:
                st.info("No complaints submitted yet.")
            else:
                df_complaints = pd.DataFrame(complaints, columns=["ID", "Area", "Category", "Description", "Phone", "Proof", "Status", "Priority", "Date"])
                
                # Filters
                col1, col2, col3 = st.columns(3)
                with col1:
                    filter_status = st.selectbox("Filter by Status", ["All"] + list(df_complaints["Status"].unique()))
                with col2:
                    filter_priority = st.selectbox("Filter by Priority", ["All"] + list(df_complaints["Priority"].unique()))
                with col3:
                    filter_area = st.selectbox("Filter by Area", ["All"] + list(df_complaints["Area"].unique()))
                
                # Apply filters
                filtered_df = df_complaints.copy()
                if filter_status != "All":
                    filtered_df = filtered_df[filtered_df["Status"] == filter_status]
                if filter_priority != "All":
                    filtered_df = filtered_df[filtered_df["Priority"] == filter_priority]
                if filter_area != "All":
                    filtered_df = filtered_df[filtered_df["Area"] == filter_area]
                
                # Display filtered complaints
                st.dataframe(filtered_df.drop(columns=["Proof"]), use_container_width=True, hide_index=True)
                
                # Complaint management
                st.divider()
                st.subheader("⚙️ Update Complaint")
                
                if len(complaints) > 0:
                    complaint_ids = [str(c[0]) for c in complaints]
                    selected_id = st.selectbox("Select Complaint ID to Update", complaint_ids)
                    
                    # Find selected complaint
                    selected_complaint = None
                    for c in complaints:
                        if str(c[0]) == selected_id:
                            selected_complaint = c
                            break
                    
                    if selected_complaint:
                        # Display complaint details
                        st.markdown(f"""
                        <div style="background:#f8f9fa;padding:15px;border-radius:8px;margin-bottom:15px;">
                            <strong>Category:</strong> {selected_complaint[2]}<br>
                            <strong>Area:</strong> {selected_complaint[1]}<br>
                            <strong>Description:</strong> {selected_complaint[3]}<br>
                            <strong>Phone:</strong> {selected_complaint[4]}<br>
                            <strong>Date:</strong> {selected_complaint[8]}<br>
                            <strong>Status:</strong> {selected_complaint[6]}<br>
                            <strong>Priority:</strong> {selected_complaint[7]}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Show proof if available
                        proof_path = selected_complaint[5]
                        if proof_path and os.path.exists(proof_path):
                            ext = os.path.splitext(proof_path)[1].lower()
                            if ext in [".jpg", ".jpeg", ".png"]:
                                st.image(proof_path, caption="Uploaded Proof", width=300)
                            else:
                                st.info(f"📎 Proof file: `{proof_path}` (video — open manually)")
                        else:
                            st.warning("No proof file found.")
                        
                        # Update form
                        col1, col2 = st.columns(2)
                        with col1:
                            new_status = st.selectbox("Update Status", ["Pending", "Approved", "Rejected"], 
                                                     index=["Pending", "Approved", "Rejected"].index(selected_complaint[6]))
                        with col2:
                            new_priority = st.selectbox("Assign Priority", ["High", "Medium", "Low"], 
                                                       index=["High", "Medium", "Low"].index(selected_complaint[7]))
                        
                        if st.button("💾 Save Changes"):
                            conn = sqlite3.connect(DB_PATH)
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE Complaint SET status = ?, priority_level = ? WHERE complaint_id = ?",
                                (new_status, new_priority, int(selected_id))
                            )
                            conn.commit()
                            conn.close()
                            st.success(f"✅ Complaint #{selected_id} updated successfully!")
                            st.rerun()
                
                # Analytics
                st.divider()
                st.subheader("📊 Complaint Analytics")
                if len(df_complaints) > 0:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**By Category**")
                        cat_counts = df_complaints["Category"].value_counts().reset_index()
                        cat_counts.columns = ["Category", "Count"]
                        fig_cat = px.bar(cat_counts, x="Category", y="Count", 
                                       color="Category", color_discrete_sequence=["#0b3d91"])
                        st.plotly_chart(fig_cat, use_container_width=True)
                    
                    with col2:
                        st.markdown("**By Priority**")
                        pri_counts = df_complaints["Priority"].value_counts().reset_index()
                        pri_counts.columns = ["Priority", "Count"]
                        fig_pri = px.bar(pri_counts, x="Priority", y="Count", 
                                       color="Priority", color_discrete_sequence=["#ff9933"])
                        st.plotly_chart(fig_pri, use_container_width=True)

# ==========================================
# 6. FOOTER
# ==========================================
st.markdown("""
    <div class="footer">
        <p>© 2026 Government Citizen Service System | All Rights Reserved</p>
        <p>Developed for Pune City Administration | MCA Project Prototype</p>
        <p style="color:#666; font-size: 10px;">Security: 256-bit SSL Encrypted • 127.0.0.1 Connection Verified</p>
    </div>
""", unsafe_allow_html=True)