# main.py
import streamlit as st
from member1 import extract_resume_text
from member2 import get_job_input
from member3 import analyze_resume

# Page Configuration
st.set_page_config(
    page_title="Smart Resume Reviewer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px;
    }
    .success-box {
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #4CAF50;
        background-color: #f0f8f0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #ff9800;
        background-color: #fff8e1;
    }
    .main {
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📚 Guide & AI Tools")
    
    # How to Use Guide
    with st.expander("📖 How to Use", expanded=True):
        st.markdown("""
        ### Step-by-Step Guide
        
        1. **Upload Resume**
           - Upload PDF or TXT format
           - Or paste resume text directly
        
        2. **Enter Job Details**
           - Specify target job role
           - Add job description (optional)
        
        3. **Choose AI Tools**
           - Select preferred AI model
           - Each tool has different strengths
        
        4. **Review Analysis**
           - Check overall score
           - Review specific feedback
           - Get improvement suggestions
        """)
    
    # AI Tools Section
    st.subheader("🤖 AI Tools Access")
    st.markdown("""
        Access these AI tools directly to enhance your analysis:
        
        #### ChatGPT
        [![ChatGPT](https://img.shields.io/badge/ChatGPT-Access-green)](https://chat.openai.com)
        - Free & paid versions
        - Strong general analysis
        
        #### Claude
        [![Claude](https://img.shields.io/badge/Claude-Access-blue)](https://claude.ai)
        - Free trial available
        - Detailed technical review
        
        #### Google Gemini
        [![Gemini](https://img.shields.io/badge/Gemini-Access-red)](https://gemini.google.com)
        - Free access
        - Good for technical roles
        
        *Note: Login required for each platform*
    """)
    
    # Additional Resources
    with st.expander("📚 Additional Resources"):
        st.markdown("""
        - [Resume Writing Tips](https://www.indeed.com/career-advice/resumes-cover-letters)
        - [ATS-Friendly Templates](https://www.jobscan.co/resume-templates)
        - [Industry Keywords Guide](https://www.linkedin.com/pulse/top-skills-2025)
        """)

# Main title
st.title("📝 Smart Resume Reviewer")
st.markdown("<div class='success-box'>Upload your resume and enter job details to get instant feedback and analysis.</div>", unsafe_allow_html=True)
st.markdown("---")

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["📤 Upload & Input", "🤖 AI Analysis", "📊 Results"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Step 1: Upload Resume")
        upload_option = st.radio("Choose input method:", ["Upload File", "Paste Text"])
        
        if upload_option == "Upload File":
            uploaded_file = st.file_uploader(
                "Upload your resume",
                type=["pdf", "txt"],
                help="Supported formats: PDF, TXT"
            )
        else:
            resume_text = st.text_area("Paste your resume text here:", height=300)
    
    if uploaded_file:
        # Extract text using Member 1's function
        resume_text = extract_resume_text(uploaded_file)
        if resume_text:
            st.success("✅ Resume text extracted successfully!")
            with st.expander("Preview Extracted Text"):
                st.text_area("Content", resume_text, height=200)

    with col2:
        st.subheader("Step 2: Job Details")
        # Get job details using Member 2's function
        job_role, job_description = get_job_input()

with tab2:
    st.subheader("🤖 AI Analysis Configuration")
    
    # AI Model Selection
    ai_col1, ai_col2 = st.columns(2)
    
    with ai_col1:
        selected_model = st.selectbox(
            "Select AI Model for Analysis:",
            ["GPT-4", "Claude", "Basic Analysis"],
            index=0,
            help="Choose an AI model for resume analysis"
        )
        
        # Model specific settings
        if selected_model in ["GPT-4", "Claude"]:
            temperature = st.slider(
                "Response Creativity",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Lower values for more focused analysis, higher for creative suggestions"
            )
            
            system_prompt = st.text_area(
                "Custom Instructions (Optional)",
                value="You are an expert resume reviewer. Analyze the resume for relevance, clarity, and impact.",
                help="Customize how the AI model should approach the analysis"
            )
    
    with ai_col2:
        analysis_aspects = st.multiselect(
            "Select Analysis Aspects:",
            ["Technical Skills", "Soft Skills", "Experience", "Education", 
             "Format & Structure", "Job Match", "Keywords Analysis"],
            default=["Technical Skills", "Experience", "Job Match"]
        )
        
        depth = st.select_slider(
            "Analysis Depth",
            options=["Basic", "Standard", "Detailed"],
            value="Standard"
        )

with tab3:
    st.subheader("Step 3: AI-Powered Analysis Results")
    if st.button("🔍 Analyze Resume", disabled=not ((uploaded_file or 'resume_text' in locals()) and job_role)):
        if resume_text:
            with st.spinner("AI is analyzing your resume..."):
                # Get analysis using Member 3's function
                analysis = analyze_resume(resume_text, job_role)
                
                # AI Summary and Initial Feedback
                st.markdown("### 🤖 AI Analysis Summary")
                st.info(analysis["detailed_review"]["summary"]["overview"])
                
                # Score Summary with Improvement Focus
                st.markdown("### 📊 Performance Analysis")
                score_cols = st.columns(4)
                
                with score_cols[0]:
                    structure_score = analysis['scores']['structure']
                    st.metric("Structure", f"{structure_score}%", 
                             delta="Needs Work" if structure_score < 70 else "Good")
                with score_cols[1]:
                    content_score = analysis['scores']['content']
                    st.metric("Content", f"{content_score}%",
                             delta="Needs Work" if content_score < 70 else "Good")
                with score_cols[2]:
                    clarity_score = analysis['scores']['clarity']
                    st.metric("Clarity", f"{clarity_score}%",
                             delta="Needs Work" if clarity_score < 70 else "Good")
                with score_cols[3]:
                    overall_score = analysis['scores']['overall']
                    st.metric("Overall", f"{overall_score}%",
                             delta="Needs Work" if overall_score < 70 else "Good")
                
                # Immediate Action Items
                st.markdown("### 🎯 Priority Improvements")
                priority_cols = st.columns([2, 1])
                with priority_cols[0]:
                    if structure_score < 70:
                        st.error("📄 **Structure Needs Work:**")
                        st.markdown("""
                        - Add clear section headers
                        - Ensure logical flow of information
                        - Include all essential sections
                        """)
                    if content_score < 70:
                        st.error("📝 **Content Enhancement Needed:**")
                        st.markdown("""
                        - Add more quantifiable achievements
                        - Include specific technical skills
                        - Highlight relevant experience
                        """)
                    if clarity_score < 70:
                        st.error("🔍 **Improve Clarity:**")
                        st.markdown("""
                        - Use more concise language
                        - Remove redundant information
                        - Strengthen action verbs
                        """)
                
                with priority_cols[1]:
                    st.info("💡 **Quick Wins**")
                    quick_improvements = analysis["detailed_review"]["recommendations"]["quick_wins"]
                    for tip in quick_improvements.get("formatting", [])[:3]:
                        st.success(f"✓ {tip}")
                
                # Detailed Analysis Tabs
                st.markdown("### 🔎 Detailed Analysis")
                
                # Enhanced Analysis Sections
                analysis_tabs = st.tabs([
                    "📈 Resume Impact",
                    "💻 Technical Skills",
                    "🎯 Job Alignment",
                    "📝 Writing & Style",
                    "🤖 AI Suggestions"
                ])
                
                with analysis_tabs[0]:
                    st.markdown("### 📈 Resume Impact Analysis")
                    impact_analysis = analysis["detailed_review"]["content_analysis"]["experience_impact"]
                    
                    # Quantified Achievements
                    st.subheader("💫 Achievement Analysis")
                    for finding in impact_analysis["findings"]:
                        if "quantified" in finding.lower():
                            st.warning(f"⚠️ {finding}")
                        else:
                            st.success(f"✅ {finding}")
                    
                    # Improvement Examples
                    st.subheader("🔄 Enhancement Examples")
                    for improvement in analysis["detailed_review"]["recommendations"]["high_impact"]:
                        with st.expander(f"📌 {improvement['title']}", expanded=True):
                            st.write(f"**Current:** {improvement['examples'][0]}")
                            st.write(f"**Better:** {improvement['examples'][1]}")
                            st.info(f"**Why:** {improvement['why']}")
                
                with analysis_tabs[1]:
                    st.markdown("### 💻 Technical Skills Assessment")
                    
                    # Skills Matrix
                    st.subheader("🔍 Skills Analysis")
                    for category, skills in analysis["technical_analysis"]["skill_categories"].items():
                        with st.expander(f"{category} Skills", expanded=True):
                            for skill, details in skills.items():
                                col1, col2 = st.columns([1, 3])
                                with col1:
                                    st.write(f"**{skill}**")
                                with col2:
                                    st.write(f"{details['level']} - _{details['context']}_")
                    
                    # Missing Skills
                    st.subheader("📋 Skill Gaps")
                    for skill in analysis["technical_analysis"]["missing_skills"]:
                        st.warning(f"🔍 Consider adding: **{skill}**")
                
                with analysis_tabs[2]:
                    st.markdown("### 🎯 Job Role Alignment")
                    
                    # Overall Match
                    match_score = analysis["market_alignment"]["overall_match"]
                    st.progress(match_score / 100)
                    st.metric("Job Match Score", f"{match_score}%")
                    
                    # ATS Analysis
                    st.subheader("🤖 ATS Optimization")
                    ats_score = analysis["ats_compatibility"]["overall_score"]
                    st.progress(ats_score / 100)
                    
                    # Keyword Analysis
                    with st.expander("📊 Keyword Analysis", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**✅ Found Keywords**")
                            for keyword in analysis["ats_compatibility"]["keyword_analysis"]["present"]:
                                st.success(keyword)
                        with col2:
                            st.markdown("**⚠️ Missing Keywords**")
                            for keyword in analysis["ats_compatibility"]["keyword_analysis"]["missing"]:
                                st.warning(keyword)
                
                with analysis_tabs[3]:
                    st.markdown("### 📝 Writing & Style Analysis")
                    
                    # Writing Quality
                    style = analysis["detailed_review"]["professional_assessment"]["writing_style"]
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Clarity Score", f"{style['clarity_score']}%")
                    with col2:
                        st.write(style["tone_analysis"])
                    
                    # Structure Analysis
                    st.subheader("📄 Document Structure")
                    st.info(style["structure_feedback"])
                
                with analysis_tabs[4]:
                    st.markdown("### 💡 AI-Powered Suggestions")
                    
                    # Priority Improvements
                    st.subheader("🎯 High-Priority Improvements")
                    for improvement in analysis["detailed_review"]["recommendations"]["high_impact"]:
                        with st.expander(improvement["title"], expanded=True):
                            st.write(f"**What to Improve:** {improvement['description']}")
                            st.markdown("**Example Change:**")
                            st.error(f"Current: {improvement['examples'][0]}")
                            st.success(f"Better: {improvement['examples'][1]}")
                            st.info(f"**Impact:** {improvement['why']}")
                    
                    # Quick Wins
                    st.subheader("⚡ Quick Improvements")
                    quick_wins = analysis["detailed_review"]["recommendations"]["quick_wins"]
                    cols = st.columns(3)
                    
                    with cols[0]:
                        st.markdown("**📝 Format**")
                        for tip in quick_wins["formatting"]:
                            st.success(tip)
                    
                    with cols[1]:
                        st.markdown("**📄 Content**")
                        for tip in quick_wins["content"]:
                            st.success(tip)
                    
                    with cols[2]:
                        st.markdown("**🎯 ATS**")
                        for tip in quick_wins["ats_optimization"]:
                            st.success(tip)                # Display detailed analysis
                analysis_tabs = st.tabs([
                    "� Technical Analysis", 
                    "💼 Professional Review",
                    "🎯 Job Match", 
                    "� Recommendations"
                ])
                
                with analysis_tabs[0]:
                    st.subheader("Technical Skills Analysis")
                    
                    # Technical Skills Breakdown
                    tech_col1, tech_col2 = st.columns(2)
                    with tech_col1:
                        st.markdown("#### 🔍 Skills Detection")
                        detected_skills = [
                            ("Python", "⭐⭐⭐"),
                            ("SQL", "⭐⭐"),
                            ("Git", "⭐⭐"),
                            ("Docker", "⭐"),
                        ]
                        for skill, level in detected_skills:
                            st.write(f"**{skill}**: {level}")
                    
                    with tech_col2:
                        st.markdown("#### � Skills Gap Analysis")
                        missing_skills = ["CI/CD", "Cloud Platforms", "Testing Frameworks"]
                        for skill in missing_skills:
                            st.warning(f"Consider adding experience with {skill}")
                    
                    # Code Quality Indicators
                    st.markdown("#### 💻 Technical Project Indicators")
                    quality_metrics = {
                        "Project Complexity": 0.75,
                        "Technical Depth": 0.65,
                        "Tool Diversity": 0.80
                    }
                    for metric, value in quality_metrics.items():
                        st.progress(value)
                        st.caption(f"{metric}: {int(value * 100)}%")
                
                with analysis_tabs[1]:
                    st.subheader("Professional Assessment")
                    
                    # Experience Analysis
                    st.markdown("#### 📈 Experience Analysis")
                    exp_quality = {
                        "Role Clarity": 85,
                        "Achievement Focus": 70,
                        "Leadership Indicators": 65,
                        "Domain Expertise": 80
                    }
                    
                    for aspect, score in exp_quality.items():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.progress(score/100)
                        with col2:
                            st.write(f"{score}%")
                    
                    # Writing Quality
                    st.markdown("#### ✍️ Writing Quality")
                    writing_metrics = {
                        "Clarity": ("Strong", "Clear and concise language"),
                        "Impact": ("Medium", "Could use more quantifiable achievements"),
                        "Professionalism": ("High", "Maintains professional tone")
                    }
                    
                    for metric, (level, desc) in writing_metrics.items():
                        st.write(f"**{metric}**: {level}")
                        st.caption(desc)
                
                with analysis_tabs[2]:
                    st.subheader("Job Role Alignment")
                    
                    # Job Match Score
                    match_score = 75
                    st.markdown(f"#### 🎯 Overall Match Score: {match_score}%")
                    st.progress(match_score/100)
                    
                    # Keyword Analysis
                    st.markdown("#### 🔑 Key Requirements Match")
                    requirements = {
                        "Required Skills": ("8/10", "🟢"),
                        "Experience Level": ("7/10", "🟡"),
                        "Domain Knowledge": ("6/10", "🟡"),
                        "Leadership": ("8/10", "🟢")
                    }
                    
                    for req, (score, indicator) in requirements.items():
                        st.write(f"{indicator} **{req}**: {score}")
                    
                    # ATS Optimization
                    st.markdown("#### 🤖 ATS Optimization Tips")
                    ats_tips = [
                        "Include more industry-standard keywords",
                        "Use conventional section headers",
                        "Ensure proper formatting for ATS parsing"
                    ]
                    for tip in ats_tips:
                        st.info(tip)
                
                with analysis_tabs[3]:
                    st.markdown("### 🤖 AI-Powered Resume Analysis")
                    
                    # Overall Summary
                    st.markdown("#### 📋 Executive Summary")
                    st.info(analysis["detailed_review"]["summary"]["overview"])
                    
                    # Detailed Content Analysis
                    st.markdown("#### 📊 Detailed Content Analysis")
                    
                    # Experience Impact
                    with st.expander("💼 Experience & Impact Analysis", expanded=True):
                        exp_impact = analysis["detailed_review"]["content_analysis"]["experience_impact"]
                        st.markdown(f"**Impact Score**: {exp_impact['rating']}/100")
                        
                        st.markdown("**📈 Key Findings:**")
                        for finding in exp_impact["findings"]:
                            if "No quantified" in finding:
                                st.warning(finding)
                            else:
                                st.success(finding)
                                
                        st.markdown("**🎯 Suggested Improvements:**")
                        for improvement in exp_impact["improvements"]:
                            st.info(f"• {improvement}")
                    
                    # Technical Analysis
                    with st.expander("💻 Technical Expertise Assessment", expanded=True):
                        tech_analysis = analysis["technical_analysis"]["technical_projects"]
                        
                        st.markdown("**🔍 Project Complexity Analysis:**")
                        for complexity in tech_analysis["complexity_analysis"]:
                            st.write(f"• {complexity}")
                        
                        st.markdown("**🛠️ Technical Stack Review:**")
                        for review in tech_analysis["tech_stack_review"]:
                            st.write(f"• {review}")
                        
                        st.markdown("**📐 Architecture & System Design:**")
                        for insight in tech_analysis["architecture_insights"]:
                            st.write(f"• {insight}")
                    
                    # Writing Style Analysis
                    with st.expander("✍️ Professional Writing Assessment", expanded=True):
                        writing_style = analysis["detailed_review"]["professional_assessment"]["writing_style"]
                        
                        # Experience Scores
                        if "experience_scores" in analysis["detailed_review"]["professional_assessment"]:
                            exp_scores = analysis["detailed_review"]["professional_assessment"]["experience_scores"]
                            for aspect, score in exp_scores.items():
                                st.metric(aspect, f"{score}%")
                        
                        # Writing Quality
                        writing_quality = analysis["detailed_review"]["professional_assessment"]["writing_quality"]
                        if writing_quality:
                            for metric, (level, desc) in writing_quality.items():
                                st.markdown(f"**{metric}**: {level}")
                                st.caption(desc)
                        
                        st.markdown("**📝 Structure Feedback:**")
                        st.info(writing_style["structure_feedback"])
                        
                    # Market Alignment
                    if "market_alignment" in analysis:
                        with st.expander("🎯 Market & Role Alignment", expanded=True):
                            st.markdown("**Industry Alignment:**")
                            for trend in analysis["market_alignment"]["industry_trends"]:
                                st.write(f"• {trend}")
                            
                            st.markdown("**Role-Specific Feedback:**")
                            for feedback in analysis["market_alignment"]["role_specific_feedback"]:
                                st.write(f"• {feedback}")
                    
                    st.markdown("---")
                    st.markdown("### 💡 Comprehensive Improvement Suggestions")
                    
                    # High Impact Improvements
                    st.subheader("🚀 High-Impact Improvements")
                    for improvement in analysis["detailed_review"]["recommendations"]["high_impact"]:
                        with st.expander(improvement["title"], expanded=True):
                            st.markdown(f"**{improvement['description']}**")
                            st.markdown("#### Examples:")
                            for i in range(0, len(improvement["examples"]), 2):
                                st.error(improvement["examples"][i])  # Before
                                st.success(improvement["examples"][i+1])  # After
                            st.info(f"**Why This Matters**: {improvement['why']}")
                    
                    # Skills Optimization
                    st.subheader("💪 Skills Optimization")
                    
                    # Technical Skills
                    tech_skills = analysis["detailed_review"]["recommendations"]["skill_optimization"]["technical_skills"]
                    with st.expander(tech_skills["title"], expanded=True):
                        for suggestion in tech_skills["suggestions"]:
                            st.markdown(f"• {suggestion}")
                        st.code(tech_skills["example"], language="markdown")
                        
                    # Soft Skills
                    soft_skills = analysis["detailed_review"]["recommendations"]["skill_optimization"]["soft_skills"]
                    with st.expander(soft_skills["title"], expanded=True):
                        for suggestion in soft_skills["suggestions"]:
                            st.markdown(f"• {suggestion}")
                        st.code(soft_skills["example"], language="markdown")
                    
                    # Quick Wins
                    st.subheader("⚡ Quick Improvements")
                    quick_wins = analysis["detailed_review"]["recommendations"]["quick_wins"]
                    
                    quick_wins_tabs = st.tabs(["📝 Formatting", "📄 Content", "🎯 ATS Optimization"])
                    
                    with quick_wins_tabs[0]:
                        for tip in quick_wins["formatting"]:
                            st.success(tip)
                    
                    with quick_wins_tabs[1]:
                        for tip in quick_wins["content"]:
                            st.success(tip)
                    
                    with quick_wins_tabs[2]:
                        for tip in quick_wins["ats_optimization"]:
                            st.success(tip)
                    
                    # ATS Compatibility Section
                    st.subheader("🤖 ATS Compatibility Analysis")
                    
                    ats_col1, ats_col2 = st.columns([2, 1])
                    with ats_col1:
                        ats_score = analysis["ats_compatibility"]["overall_score"]
                        st.progress(ats_score / 100)
                        st.caption(f"ATS Compatibility Score: {ats_score}%")
                    
                    with ats_col2:
                        if ats_score >= 80:
                            st.success("✅ ATS Friendly")
                        elif ats_score >= 60:
                            st.warning("⚠️ Some Improvements Needed")
                        else:
                            st.error("❌ Major Revisions Needed")
                    
                    # Keyword Analysis
                    with st.expander("🔍 ATS Keyword Analysis", expanded=True):
                        for suggestion in analysis["ats_compatibility"]["keyword_analysis"]["suggestions"]:
                            st.info(suggestion)
                    
                    # Download Options
                    st.markdown("---")
                    st.subheader("📥 Download Analysis")
                    
                    # Generate detailed report text
                    report_text = f"""
Resume Analysis Report for {job_role} Position
============================================

Overall Scores
-------------
Structure: {analysis['scores']['structure']}%
Content: {analysis['scores']['content']}%
Clarity: {analysis['scores']['clarity']}%
Overall: {analysis['scores']['overall']}%

High-Impact Recommendations
-------------------------
"""
                    # Add high-impact recommendations
                    for imp in analysis["detailed_review"]["recommendations"]["high_impact"]:
                        report_text += f"\n{imp['title']}\n"
                        report_text += f"{'-' * len(imp['title'])}\n"
                        report_text += f"{imp['description']}\n\n"
                        report_text += "Examples:\n"
                        for i in range(0, len(imp["examples"]), 2):
                            report_text += f"Before: {imp['examples'][i]}\n"
                            report_text += f"After:  {imp['examples'][i+1]}\n\n"
                    
                    # Add skills optimization
                    report_text += "\nSkills Optimization\n==================\n"
                    report_text += "\nTechnical Skills Suggestions:\n"
                    for sugg in analysis["detailed_review"]["recommendations"]["skill_optimization"]["technical_skills"]["suggestions"]:
                        report_text += f"• {sugg}\n"
                    
                    report_text += "\nExample Technical Skills Format:\n"
                    report_text += analysis["detailed_review"]["recommendations"]["skill_optimization"]["technical_skills"]["example"]
                    
                    # Add quick wins
                    report_text += "\n\nQuick Improvements\n=================\n"
                    for category, tips in analysis["detailed_review"]["recommendations"]["quick_wins"].items():
                        report_text += f"\n{category.title()}:\n"
                        for tip in tips:
                            report_text += f"• {tip}\n"
                    
                    # Download options
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="📄 Download as Text",
                            data=report_text,
                            file_name="resume_analysis_report.txt",
                            mime="text/plain"
                        )
                    
                    with col2:
                        st.markdown("""
                        <style>
                        .copy-box {
                            background-color: #f0f2f6;
                            border-radius: 5px;
                            padding: 10px;
                            margin: 10px 0;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("📋 Copy Report Text", expanded=False):
                            st.markdown('<div class="copy-box">', unsafe_allow_html=True)
                            st.code(report_text, language="markdown")
                            st.markdown('</div>', unsafe_allow_html=True)
                
                with analysis_tabs[3]:
                    st.markdown("### 🤖 AI Analysis Feedback")
                    
                    if selected_model != "Basic Analysis":
                        with st.spinner(f"Generating {selected_model} analysis..."):
                            # Here you would integrate with the actual AI model APIs
                            # For now, showing a placeholder for the integrated AI analysis
                            st.write(f"💫 **{selected_model} Analysis**")
                            
                            analysis_sections = {
                                "Skills Analysis": "Detailed review of technical and soft skills based on job requirements",
                                "Experience Match": "Assessment of experience relevance and achievements",
                                "Format & Structure": "Evaluation of resume organization and clarity",
                                "Improvement Suggestions": "Specific recommendations for enhancement"
                            }
                            
                            for section, content in analysis_sections.items():
                                with st.expander(section, expanded=True):
                                    st.write(content)
                                    if section == "Improvement Suggestions":
                                        st.warning("● Add more quantifiable achievements")
                                        st.warning("● Enhance technical skills section")
                                        st.warning("● Improve role descriptions")
                            
                            # Custom feedback based on model
                            if selected_model == "GPT-4":
                                st.info("🔍 Advanced language model providing comprehensive analysis")
                            elif selected_model == "Claude":
                                st.info("� Anthropic's AI offering detailed technical insights")
                            
                # Download Report Option
                st.download_button(
                    label="📥 Download Full Analysis Report",
                    data=f"Resume Analysis Report\n\nJob Role: {job_role}\n\nScores:\n- Structure: {analysis['scores']['structure']}%\n- Content: {analysis['scores']['content']}%\n- Overall: {analysis['scores']['overall']}%",
                    file_name="resume_analysis_report.txt",
                    mime="text/plain"
                )
        else:
            st.error("Please upload a valid resume first")
