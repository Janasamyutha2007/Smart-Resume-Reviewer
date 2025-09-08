# member3.py
import streamlit as st
import re

def analyze_resume(resume_text, job_role):
    """
    Advanced Resume Analysis Engine
    Provides comprehensive AI-like analysis and detailed feedback
    """
    analysis = {
        "scores": {
            "structure": 0,
            "content": 0,
            "clarity": 0,
            "overall": 0
        },
        "detailed_review": {
            "summary": {
                "overview": "",
                "key_findings": [],
                "main_strengths": [],
                "priority_improvements": []
            },
            "content_analysis": {
                "experience_impact": {
                    "rating": 0,
                    "findings": [],
                    "examples": [],
                    "improvements": []
                },
                "skills_relevance": {
                    "rating": 0,
                    "findings": [],
                    "gaps": [],
                    "recommendations": []
                },
                "achievements": {
                    "rating": 0,
                    "strong_points": [],
                    "weak_points": [],
                    "suggested_formats": []
                }
            },
            "professional_assessment": {
                "writing_style": {
                    "clarity_score": 0,
                    "tone_analysis": "",
                    "structure_feedback": "",
                    "improvement_areas": []
                },
                "impact_analysis": {
                    "quantified_achievements": [],
                    "qualitative_strengths": [],
                    "missing_elements": []
                }
            },
            "recommendations": {
                "high_impact": [],
                "quick_wins": {
                    "formatting": [],
                    "content": [],
                    "ats_optimization": []
                },
                "skill_optimization": {
                    "technical_skills": {
                        "title": "",
                        "suggestions": [],
                        "example": ""
                    },
                    "soft_skills": {
                        "title": "",
                        "suggestions": [],
                        "example": ""
                    }
                }
            }
        },
        "technical_analysis": {
            "detected_skills": {},
            "missing_skills": [],
            "quality_metrics": {},
            "skill_categories": {},
            "technical_projects": {
                "complexity_analysis": [],
                "tech_stack_review": [],
                "architecture_insights": []
            }
        },
        "market_alignment": {
            "industry_trends": [],
            "role_specific_feedback": [],
            "competitive_analysis": "",
            "unique_selling_points": [],
            "overall_match": 0,
            "requirements_match": {}
        },
        "ats_compatibility": {
            "overall_score": 0,
            "format_issues": [],
            "keyword_analysis": {
                "present": [],
                "missing": [],
                "suggestions": []
            },
            "section_analysis": {}
        }
    }
    
    # Basic text analysis
    words = len(resume_text.split())
    sentences = len(re.split(r'[.!?]+', resume_text))
    
    # Prepare detailed initial review
    analysis["detailed_review"]["summary"]["overview"] = f"""Based on a comprehensive analysis of your resume for the {job_role} position, 
    I've identified several key areas of strength and opportunities for enhancement. Your resume demonstrates {words} words across {sentences} distinct statements,
    suggesting {'good' if words > 400 else 'moderate' if words > 300 else 'limited'} detail level."""
    
    # Analyze text quality and professional tone
    professional_terms = ["implemented", "developed", "managed", "led", "architected", "designed", "optimized"]
    vague_terms = ["worked on", "helped with", "assisted", "responsible for"]
    
    prof_term_count = sum(1 for term in professional_terms if term in resume_text.lower())
    vague_term_count = sum(1 for term in vague_terms if term in resume_text.lower())
    
    analysis["detailed_review"]["professional_assessment"]["writing_style"].update({
        "clarity_score": min((prof_term_count * 10) + (100 - vague_term_count * 20), 100),
        "tone_analysis": "Your resume maintains a professional tone" if prof_term_count > vague_term_count else 
                        "Consider using more professional action verbs",
        "structure_feedback": "Well-structured with clear sections" if any(section in resume_text.lower() 
                            for section in ["experience", "education", "skills"]) else 
                            "Important sections may be missing or unclear"
    })
    
    # Technical Skills Analysis with detailed context
    technical_skills = {
        "Languages": {
            "python": {"level": "⭐⭐⭐", "context": "Modern development, data analysis, automation"},
            "java": {"level": "⭐⭐", "context": "Enterprise applications, Spring framework"},
            "javascript": {"level": "⭐⭐", "context": "Web development, React/Node.js"},
            "c++": {"level": "⭐⭐", "context": "System programming, performance optimization"},
            "sql": {"level": "⭐⭐⭐", "context": "Database design, complex queries"}
        },
        "Tools": {
            "git": {"level": "⭐⭐", "context": "Version control, collaboration"},
            "docker": {"level": "⭐⭐", "context": "Containerization, deployment"},
            "kubernetes": {"level": "⭐", "context": "Container orchestration"},
            "jenkins": {"level": "⭐", "context": "CI/CD pipelines"},
            "jira": {"level": "⭐⭐", "context": "Project management, agile"}
        },
        "Frameworks": {
            "react": {"level": "⭐⭐", "context": "Frontend development"},
            "angular": {"level": "⭐", "context": "SPA development"},
            "django": {"level": "⭐⭐", "context": "Python web framework"},
            "flask": {"level": "⭐⭐", "context": "Lightweight web services"},
            "spring": {"level": "⭐", "context": "Java enterprise applications"}
        },
        "Cloud & DevOps": {
            "aws": {"level": "⭐⭐", "context": "Cloud infrastructure"},
            "azure": {"level": "⭐", "context": "Microsoft cloud services"},
            "gcp": {"level": "⭐", "context": "Google cloud platform"},
            "terraform": {"level": "⭐", "context": "Infrastructure as Code"},
            "ci/cd": {"level": "⭐⭐", "context": "Automated deployment"}
        }
    }
    
    # Detect skills and their levels
    for category, skills in technical_skills.items():
        detected = {}
        for skill, level in skills.items():
            if skill.lower() in resume_text.lower():
                detected[skill] = level
        analysis["technical_analysis"]["skill_categories"][category] = detected
    
    # Identify missing critical skills
    essential_skills = ["ci/cd", "testing", "cloud", "agile"]
    analysis["technical_analysis"]["missing_skills"] = [
        skill for skill in essential_skills 
        if skill not in resume_text.lower()
    ]
    
    # Calculate quality metrics
    project_indicators = ["implemented", "developed", "designed", "architected"]
    complexity_indicators = ["complex", "scalable", "distributed", "optimized"]
    
    analysis["technical_analysis"]["quality_metrics"] = {
        "Project Complexity": min(len([w for w in complexity_indicators if w in resume_text.lower()]) * 0.25, 1.0),
        "Technical Depth": min(sum([1 for cat in analysis["technical_analysis"]["skill_categories"].values() for s in cat]) * 0.1, 1.0),
        "Tool Diversity": min(len([w for w in project_indicators if w in resume_text.lower()]) * 0.2, 1.0)
    }
    
    # Professional Review
    experience_indicators = {
        "Role Clarity": ["led", "managed", "responsible", "ownership"],
        "Achievement Focus": ["improved", "increased", "reduced", "achieved"],
        "Leadership": ["team", "mentored", "supervised", "directed"],
        "Domain Expertise": ["expert", "specialist", "proficient", "advanced"]
    }
    
    # Calculate experience scores
    for aspect, indicators in experience_indicators.items():
        score = min(sum([10 for ind in indicators if ind in resume_text.lower()]), 100)
        analysis["detailed_review"]["professional_assessment"]["experience_scores"] = {aspect: score}
    
    # Writing Quality Assessment
    analysis["detailed_review"]["professional_assessment"]["writing_quality"] = {
        "Clarity": ("Strong" if sentences/words < 0.1 else "Medium", 
                   "Clear and concise language" if sentences/words < 0.1 else "Could be more concise"),
        "Impact": ("High" if len([w for w in ["increased", "improved", "achieved"] if w in resume_text.lower()]) > 3 
                  else "Medium", "Good use of impact verbs" if len([w for w in ["increased", "improved"] 
                  if w in resume_text.lower()]) > 3 else "Add more achievement metrics"),
        "Professionalism": ("High" if not any(casual in resume_text.lower() for casual in ["cool", "awesome", "great"]) 
                           else "Medium", "Maintains professional tone")
    }
    
    # Job Match Analysis
    keywords = job_role.lower().split()
    role_keywords_found = sum([1 for word in keywords if word in resume_text.lower()])
    match_score = min((role_keywords_found / len(keywords)) * 100, 100) if keywords else 50
    
    analysis["market_alignment"]["overall_match"] = match_score
    analysis["market_alignment"]["role_specific_feedback"] = [
        f"Match Score: {match_score}% alignment with the {job_role} role",
        "Strong technical skill alignment" if match_score > 70 else "Consider adding more role-specific keywords"
    ]
    analysis["market_alignment"]["requirements_match"] = {
        "Required Skills": (f"{len(analysis['technical_analysis']['skill_categories'].get('Languages', {}))}/10", 
                          "🟢" if len(analysis['technical_analysis']['skill_categories'].get('Languages', {})) > 5 else "🟡"),
        "Experience Level": ("7/10", "🟡"),
        "Domain Knowledge": ("6/10", "🟡"),
        "Leadership": ("8/10", "🟢" if "led" in resume_text.lower() or "managed" in resume_text.lower() else "🟡")
    }
    
    # ATS Tips
    analysis["ats_compatibility"]["keyword_analysis"]["suggestions"] = [
        "Include more industry-standard keywords",
        "Use conventional section headers",
        "Ensure proper formatting for ATS parsing"
    ]
    
    # Update ATS overall score based on analysis
    ats_score = min((match_score + len(analysis["technical_analysis"]["skill_categories"]) * 10), 100)
    analysis["ats_compatibility"]["overall_score"] = ats_score
    
    # Detailed Recommendations
    analysis["detailed_review"]["recommendations"]["high_impact"] = [
        {
            "title": "💡 Quantify Your Achievements",
            "description": "Transform your achievements with specific metrics and outcomes",
            "examples": [
                "Before: 'Improved system performance'",
                "After: 'Optimized database queries resulting in 40% faster response time and 30% reduced server load'",
                "Before: 'Managed a team project'",
                "After: 'Led a team of 8 developers to deliver a $2M project 2 weeks ahead of schedule'"
            ],
            "why": "Quantified achievements provide concrete evidence of your impact and make your resume more credible."
        },
        {
            "title": "🔧 Technical Project Details",
            "description": "Showcase your technical depth with detailed project descriptions",
            "examples": [
                "Before: 'Built a web application'",
                "After: 'Architected and developed a scalable web platform using React/Node.js, handling 100K+ daily users'",
                "Before: 'Implemented database optimizations'",
                "After: 'Redesigned database schema and implemented query optimization, reducing data retrieval time from 5s to 200ms'"
            ],
            "why": "Detailed technical descriptions demonstrate your expertise and problem-solving abilities."
        },
        {
            "title": "👥 Leadership & Collaboration",
            "description": "Highlight your team leadership and collaboration skills",
            "examples": [
                "Before: 'Worked on team projects'",
                "After: 'Mentored 4 junior developers, implemented agile practices, and increased team velocity by 50%'",
                "Before: 'Participated in code reviews'",
                "After: 'Established code review guidelines and led bi-weekly technical knowledge sharing sessions'"
            ],
            "why": "Leadership examples show your ability to influence and drive team success."
        },
        {
            "title": "🎯 Job-Specific Alignment",
            "description": "Tailor your experience to match job requirements",
            "examples": [
                "Before: 'Worked with various programming languages'",
                "After: 'Proficient in Python and Java, with 3+ years building REST APIs and microservices'",
                "Before: 'Familiar with cloud services'",
                "After: 'Designed and deployed containerized applications on AWS using ECS, Lambda, and RDS'"
            ],
            "why": "Aligned experience helps recruiters quickly identify your relevant qualifications."
        }
    ]
    
    analysis["detailed_review"]["recommendations"]["skill_optimization"] = {
        "technical_skills": {
            "title": "💻 Technical Skills Enhancement",
            "suggestions": [
                "Create a dedicated 'Technical Skills' section at the top",
                "Group skills by category (Languages, Frameworks, Tools, etc.)",
                "Highlight proficiency levels for key skills",
                "Add relevant certifications and training"
            ],
            "example": """
Technical Skills
---------------
Languages: Python (Expert), Java (Advanced), JavaScript (Intermediate)
Frameworks: Django, Spring Boot, React.js
Cloud & DevOps: AWS (Certified), Docker, Kubernetes
Tools: Git, JIRA, Jenkins, Prometheus
            """
        },
        "soft_skills": {
            "title": "🤝 Soft Skills Integration",
            "suggestions": [
                "Weave soft skills into achievement descriptions",
                "Demonstrate leadership and communication abilities",
                "Show problem-solving and decision-making examples",
                "Include team collaboration highlights"
            ],
            "example": """
• Led cross-functional team meetings and workshops, improving team collaboration and project delivery time by 25%
• Mentored 3 junior developers, creating detailed documentation that reduced onboarding time from 2 weeks to 4 days
• Presented technical solutions to stakeholders, securing buy-in for a $500K system upgrade
            """
        }
    }
    
    analysis["detailed_review"]["recommendations"]["quick_wins"] = {
        "formatting": [
            "Use consistent bullet point formatting throughout",
            "Ensure section headers are clearly visible",
            "Maintain consistent font and spacing",
            "Use bold for key achievements and metrics"
        ],
        "content": [
            "Add a compelling professional summary (3-4 lines)",
            "Include GitHub/portfolio/LinkedIn links",
            "List relevant certifications with dates",
            "Add technologies used in each project"
        ],
        "ats_optimization": [
            "Use standard section headers (Experience, Education, Skills)",
            "Include keywords from the job description",
            "Avoid tables and complex formatting",
            "Use common file formats (PDF, DOCX)"
        ]
    }
    
    # Calculate overall scores
    analysis["scores"]["structure"] = min(len([w for w in ["experience", "education", "skills"] if w in resume_text.lower()]) * 30, 100)
    analysis["scores"]["content"] = min(match_score, 100)
    analysis["scores"]["clarity"] = min(100, max(20, min(words // 10, 100)))
    analysis["scores"]["overall"] = (
        analysis["scores"]["structure"] + 
        analysis["scores"]["content"] + 
        analysis["scores"]["clarity"]
    ) // 3
    
    return analysis
    
    return analysis

# Example usage inside Streamlit
if __name__ == "__main__":
    st.title("📄 AI Resume Reviewer (Member 3)")

    uploaded_file = st.file_uploader("Upload Resume (TXT)", type=["txt"])
    job_role = st.text_input("Target Job Role", placeholder="e.g. Data Scientist")

    if uploaded_file and job_role and st.button("🔍 Analyze Resume"):
        resume_text = uploaded_file.read().decode("utf-8", errors="ignore")
        analysis = analyze_resume(resume_text, job_role)
        
        st.subheader("📊 Analysis Results")
        
        # Display scores
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Structure", f"{analysis['scores']['structure']}%")
        with col2:
            st.metric("Content", f"{analysis['scores']['content']}%")
        with col3:
            st.metric("Clarity", f"{analysis['scores']['clarity']}%")
        with col4:
            st.metric("Overall", f"{analysis['scores']['overall']}%")
        
        # Display strengths
        st.subheader("💪 Strengths")
        for strength in analysis["strengths"]:
            st.success(strength)
            
        # Display weaknesses
        st.subheader("🔍 Areas for Improvement")
        for weakness in analysis["weaknesses"]:
            st.warning(weakness)
            
        # Display suggestions
        st.subheader("💡 Suggestions")
        for suggestion in analysis["suggestions"]:
            st.info(suggestion)
