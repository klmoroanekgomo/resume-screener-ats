"""
Streamlit Web Interface for Resume Screening System
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import time

# Page configuration
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions

def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def upload_resume(file):
    """Upload resume to API"""
    try:
        files = {'file': (file.name, file, file.type)}
        response = requests.post(f"{API_BASE_URL}/resume/upload", files=files)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error uploading resume: {str(e)}")
        return None

def get_profile(filename):
    """Get candidate profile from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/resume/profile/{filename}")
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error getting profile: {str(e)}")
        return None

def match_single(filename, job_data):
    """Match single resume to job"""
    try:
        params = {"filename": filename}
        response = requests.post(
            f"{API_BASE_URL}/match/single",
            params=params,
            json=job_data
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error matching resume: {str(e)}")
        return None

def match_batch(job_data, resume_filenames=None):
    """Match multiple resumes to job"""
    try:
        request_data = {
            "job_description": job_data,
            "resume_filenames": resume_filenames
        }
        response = requests.post(f"{API_BASE_URL}/match/batch", json=request_data)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error batch matching: {str(e)}")
        return None

def list_resumes():
    """Get list of uploaded resumes"""
    try:
        response = requests.get(f"{API_BASE_URL}/resumes/list")
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error listing resumes: {str(e)}")
        return None

# Main App

def main():
    # Header
    st.markdown('<p class="main-header">🎯 AI-Powered Resume Screening System</p>', unsafe_allow_html=True)
    
    # Check API health
    if not check_api_health():
        st.markdown("""
        <div class="error-box">
            <h3>⚠️ API Not Running</h3>
            <p>Please start the API server before using this app:</p>
            <code>python src/api/main.py</code>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/resume.png", width=80)
        st.title("Navigation")
        
        page = st.radio(
            "Select Page",
            ["🏠 Home", "📤 Upload Resumes", "👤 View Profiles", "🎯 Match Candidates", "📊 Analytics"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # API Status
        st.markdown("### API Status")
        st.success("✅ Connected")
        
        # Quick Stats
        resumes_data = list_resumes()
        if resumes_data:
            st.metric("Total Resumes", resumes_data.get('total', 0))
        
        st.markdown("---")
        st.markdown("### About")
        st.info("""
        AI-powered system for screening resumes and matching candidates to jobs.
        
        **Features:**
        - Resume parsing
        - Skill extraction
        - Candidate matching
        - Batch processing
        """)
    
    # Main Content
    if page == "🏠 Home":
        show_home()
    elif page == "📤 Upload Resumes":
        show_upload()
    elif page == "👤 View Profiles":
        show_profiles()
    elif page == "🎯 Match Candidates":
        show_matching()
    elif page == "📊 Analytics":
        show_analytics()

def show_home():
    """Home page"""
    
    st.markdown("## Welcome to the AI Resume Screener! 👋")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚀 Quick Start
        
        1. **Upload Resumes** - Add candidate resumes (PDF, DOCX, or TXT)
        2. **View Profiles** - Extract skills, experience, and education
        3. **Match Candidates** - Compare resumes to job descriptions
        4. **Analyze Results** - View insights and rankings
        
        ### ✨ Key Features
        
        - 🤖 **AI-Powered** - Advanced NLP and machine learning
        - 📊 **Smart Matching** - Multi-factor candidate scoring
        - ⚡ **Fast Processing** - Batch process multiple resumes
        - 📈 **Analytics** - Insights and visualizations
        """)
    
    with col2:
        st.markdown("### 📊 System Overview")
        
        # Get statistics
        resumes_data = list_resumes()
        
        if resumes_data and resumes_data.get('total', 0) > 0:
            # Create metrics
            total_resumes = resumes_data['total']
            
            metric_col1, metric_col2 = st.columns(2)
            metric_col1.metric("Total Resumes", total_resumes)
            metric_col2.metric("Status", "Ready", delta="Active")
            
            # Recent uploads
            st.markdown("#### Recent Uploads")
            recent = resumes_data['resumes'][:5]
            for resume in recent:
                st.text(f"📄 {resume['filename']} ({resume['size_kb']} KB)")
        else:
            st.info("No resumes uploaded yet. Start by uploading some resumes!")
            
            if st.button("📤 Go to Upload Page"):
                st.session_state.page = "📤 Upload Resumes"
                st.rerun()
    
    # Demo Section
    st.markdown("---")
    st.markdown("## 🎬 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>1️⃣ Upload</h3>
            <p>Upload candidate resumes in PDF, DOCX, or TXT format</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>2️⃣ Extract</h3>
            <p>AI extracts skills, experience, education, and more</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>3️⃣ Match</h3>
            <p>Smart matching ranks candidates by fit score</p>
        </div>
        """, unsafe_allow_html=True)

def show_upload():
    """Upload resumes page"""
    
    st.markdown("## 📤 Upload Resumes")
    
    st.markdown("""
    Upload candidate resumes to start the screening process. 
    Supported formats: **PDF**, **DOCX**, **TXT**
    """)
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose resume files",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help="You can upload multiple files at once"
    )
    
    if uploaded_files:
        st.markdown(f"### Selected Files: {len(uploaded_files)}")
        
        # Show file details
        for file in uploaded_files:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.text(f"📄 {file.name}")
            col2.text(f"{file.size / 1024:.1f} KB")
            col3.text(file.type.split('/')[-1].upper())
        
        # Upload button
        if st.button("🚀 Upload All", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            
            for i, file in enumerate(uploaded_files):
                status_text.text(f"Uploading {file.name}...")
                result = upload_resume(file)
                
                if result:
                    results.append({
                        'filename': result['filename'],
                        'status': result['processing_status'],
                        'size': result['file_size'],
                        'text_length': result['extracted_text_length']
                    })
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.empty()
            progress_bar.empty()
            
            # Show results
            st.success(f"✅ Successfully uploaded {len(results)} resume(s)!")
            
            # Results table
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)
                
                st.balloons()

def show_profiles():
    """View candidate profiles page"""
    
    st.markdown("## 👤 Candidate Profiles")
    
    # Get list of resumes
    resumes_data = list_resumes()
    
    if not resumes_data or resumes_data.get('total', 0) == 0:
        st.warning("No resumes uploaded yet. Please upload some resumes first.")
        return
    
    # Select resume
    resume_files = [r['filename'] for r in resumes_data['resumes']]
    selected_file = st.selectbox("Select a resume to view", resume_files)
    
    if selected_file:
        if st.button("📊 Extract Profile", type="primary"):
            with st.spinner("Extracting profile..."):
                profile = get_profile(selected_file)
            
            if profile:
                # Header
                st.markdown("---")
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"### {profile.get('name', 'Unknown Candidate')}")
                    st.markdown(f"**File:** {profile['filename']}")
                
                with col2:
                    st.metric("Experience Level", profile['experience_level'].upper())
                    st.metric("Years of Experience", profile['years_experience'])
                
                # Contact Information
                st.markdown("#### 📧 Contact Information")
                contact_col1, contact_col2, contact_col3 = st.columns(3)
                
                contact_col1.text_input("Email", profile.get('email', 'N/A'), disabled=True)
                contact_col2.text_input("Phone", profile.get('phone', 'N/A'), disabled=True)
                contact_col3.text_input("LinkedIn", profile.get('linkedin', 'N/A'), disabled=True)
                
                # Skills
                st.markdown("#### 🔧 Skills")
                
                skills_data = profile['skills']
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Skills", skills_data['total_skills'])
                col2.metric("Categories", len(skills_data['categories']))
                col3.metric("Top Skill Mentions", max(skills_data['skill_count'].values()) if skills_data['skill_count'] else 0)
                
                # Skills by category
                if skills_data['categories']:
                    st.markdown("##### Skills by Category")
                    
                    for category, skills in skills_data['categories'].items():
                        with st.expander(f"{category.replace('_', ' ').title()} ({len(skills)} skills)"):
                            st.write(", ".join(skills))
                
                # Top skills chart
                if skills_data['skill_count']:
                    st.markdown("##### Most Mentioned Skills")
                    
                    # Get top 10 skills
                    top_skills = sorted(
                        skills_data['skill_count'].items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:10]
                    
                    skills, counts = zip(*top_skills)
                    
                    fig = px.bar(
                        x=list(counts),
                        y=list(skills),
                        orientation='h',
                        labels={'x': 'Mentions', 'y': 'Skill'},
                        title="Top 10 Skills"
                    )
                    fig.update_layout(showlegend=False, height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Education
                st.markdown("#### 🎓 Education")
                
                edu_data = profile['education']
                
                if edu_data['has_degree']:
                    st.success(f"**Highest Level:** {edu_data['highest_level'].replace('_', ' ').title()}")
                    
                    if edu_data['found_degrees']:
                        st.markdown("**Degrees Found:**")
                        for degree in edu_data['found_degrees']:
                            st.text(f"• {degree['keyword']} ({degree['level']})")
                else:
                    st.info("No degree information found")
                
                # Certifications
                st.markdown("#### 📜 Certifications")
                
                if profile['certifications']:
                    for cert in profile['certifications']:
                        st.text(f"✓ {cert}")
                else:
                    st.info("No certifications found")

def show_matching():
    """Match candidates to jobs page"""
    
    st.markdown("## 🎯 Match Candidates to Job")
    
    # Get list of resumes
    resumes_data = list_resumes()
    
    if not resumes_data or resumes_data.get('total', 0) == 0:
        st.warning("No resumes uploaded yet. Please upload some resumes first.")
        return
    
    # Tabs for single vs batch matching
    tab1, tab2 = st.tabs(["Single Match", "Batch Match"])
    
    with tab1:
        show_single_match(resumes_data)
    
    with tab2:
        show_batch_match(resumes_data)

def show_single_match(resumes_data):
    """Single resume matching"""
    
    st.markdown("### Match a Single Resume")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Select Resume")
        resume_files = [r['filename'] for r in resumes_data['resumes']]
        selected_file = st.selectbox("Resume", resume_files, key="single_resume")
    
    with col2:
        st.markdown("#### Job Details")
        job_title = st.text_input("Job Title", "Senior Python Developer")
        company = st.text_input("Company", "TechCorp")
    
    st.markdown("#### Job Description")
    job_description = st.text_area(
        "Description",
        """We are seeking a Senior Python Developer with 5+ years of experience.

Required Skills:
- Python, Django, FastAPI
- PostgreSQL, MongoDB
- AWS, Docker, Kubernetes
- RESTful APIs, Microservices
- Git, CI/CD

Education: Bachelor's degree in Computer Science
Experience: 5+ years""",
        height=200
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        required_skills = st.text_input(
            "Required Skills (comma-separated)",
            "Python, Django, FastAPI, AWS, Docker, PostgreSQL"
        )
    
    with col2:
        required_years = st.number_input("Required Years of Experience", min_value=0, value=5)
    
    if st.button("🎯 Calculate Match", type="primary"):
        with st.spinner("Calculating match score..."):
            # Prepare job data
            job_data = {
                "title": job_title,
                "company": company,
                "description": job_description,
                "required_skills": [s.strip() for s in required_skills.split(',')] if required_skills else [],
                "required_years": required_years
            }
            
            result = match_single(selected_file, job_data)
        
        if result:
            display_match_result(result)

def show_batch_match(resumes_data):
    """Batch resume matching"""
    
    st.markdown("### Match Multiple Resumes")
    
    st.markdown("#### Job Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        job_title = st.text_input("Job Title", "Data Scientist", key="batch_title")
        company = st.text_input("Company", "DataMinds AI", key="batch_company")
    
    with col2:
        required_years = st.number_input("Required Years", min_value=0, value=3, key="batch_years")
        required_education = st.selectbox(
            "Required Education",
            ["Any", "bachelors", "masters", "phd"],
            key="batch_edu"
        )
    
    job_description = st.text_area(
        "Description",
        """Looking for a Data Scientist with ML expertise.

Required Skills:
- Python, R
- Machine Learning, TensorFlow, PyTorch
- SQL, NoSQL
- Data visualization
- NLP, Computer Vision

Education: Master's degree preferred
Experience: 3+ years""",
        height=150,
        key="batch_desc"
    )
    
    required_skills = st.text_input(
        "Required Skills (comma-separated)",
        "Python, Machine Learning, TensorFlow, PyTorch, NLP",
        key="batch_skills"
    )
    
    # Select resumes
    st.markdown("#### Select Resumes to Match")
    all_resumes = [r['filename'] for r in resumes_data['resumes']]
    
    match_all = st.checkbox("Match all resumes", value=True)
    
    if not match_all:
        selected_resumes = st.multiselect("Select specific resumes", all_resumes)
    else:
        selected_resumes = None
    
    if st.button("🚀 Match All Candidates", type="primary"):
        with st.spinner("Processing batch match..."):
            # Prepare job data
            job_data = {
                "title": job_title,
                "company": company,
                "description": job_description,
                "required_skills": [s.strip() for s in required_skills.split(',')] if required_skills else [],
                "required_years": required_years,
                "required_education": required_education if required_education != "Any" else None
            }
            
            result = match_batch(job_data, selected_resumes)
        
        if result:
            display_batch_results(result)

def display_match_result(result):
    """Display single match result"""
    
    st.markdown("---")
    st.markdown("## 📊 Match Results")
    
    # Overall score
    score = result['overall_score']
    fit_level = result['fit_level']
    
    # Color based on score
    if score >= 80:
        color = "success"
    elif score >= 60:
        color = "warning"
    else:
        color = "error"
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Overall Score", f"{score:.1f}%", fit_level)
    col2.metric("Skill Match", f"{result['skill_match']['match_percentage']:.1f}%")
    col3.metric("Text Similarity", f"{result['text_similarity']:.1f}%")
    col4.metric("Semantic Similarity", f"{result['semantic_similarity']:.1f}%")
    
    # Detailed breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Matched Skills")
        skill_match = result['skill_match']
        
        st.info(f"**{skill_match['total_matched']} / {skill_match['total_required']}** required skills matched")
        
        if skill_match['matched_skills']:
            for skill in skill_match['matched_skills']:
                st.text(f"✓ {skill}")
    
    with col2:
        st.markdown("### ❌ Missing Skills")
        
        if skill_match['missing_skills']:
            st.warning(f"**{len(skill_match['missing_skills'])}** skills needed")
            for skill in skill_match['missing_skills']:
                st.text(f"✗ {skill}")
        else:
            st.success("No missing skills!")
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    
    for rec in result['recommendations']:
        st.info(f"• {rec}")
    
    # Gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        title={'text': "Overall Fit Score"},
        delta={'reference': 70},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "lightgray"},
                {'range': [40, 60], 'color': "lightyellow"},
                {'range': [60, 80], 'color': "lightgreen"},
                {'range': [80, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def display_batch_results(result):
    """Display batch match results"""
    
    st.markdown("---")
    st.markdown("## 📊 Batch Match Results")
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Job", result['job_title'])
    col2.metric("Total Candidates", result['total_candidates'])
    col3.metric("Processing Time", f"{result['processing_time']:.2f}s")
    
    # Rankings
    st.markdown("### 🏆 Candidate Rankings")
    
    matches = result['matches']
    
    # Create DataFrame
    df_data = []
    for i, match in enumerate(matches, 1):
        df_data.append({
            'Rank': i,
            'Candidate': match['candidate_name'] or 'Unknown',
            'Score': f"{match['overall_score']:.1f}%",
            'Fit Level': match['fit_level'],
            'Skills Match': f"{match['skill_match']['match_percentage']:.1f}%",
            'Missing Skills': len(match['skill_match']['missing_skills'])
        })
    
    df = pd.DataFrame(df_data)
    
    # Style the dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Top 3 detailed view
    st.markdown("### 🥇 Top 3 Candidates")
    
    for i, match in enumerate(matches[:3], 1):
        with st.expander(f"#{i} - {match['candidate_name']} ({match['overall_score']:.1f}%)"):
            display_match_result(match)
    
    # Score distribution
    st.markdown("### 📈 Score Distribution")
    
    scores = [m['overall_score'] for m in matches]
    
    fig = px.histogram(
        scores,
        nbins=10,
        title="Candidate Score Distribution",
        labels={'value': 'Score', 'count': 'Number of Candidates'}
    )
    st.plotly_chart(fig, use_container_width=True)

def show_analytics():
    """Analytics and insights page"""
    
    st.markdown("## 📊 Analytics & Insights")
    
    st.info("Analytics dashboard coming soon! This will include:")
    st.markdown("""
    - 📈 Skill demand trends
    - 🎯 Average match scores
    - 📊 Candidate quality distribution
    - 🔍 Most common skills
    - 📅 Hiring timeline metrics
    """)

if __name__ == "__main__":
    main()

    