# member2.py
import streamlit as st
import textwrap

def get_job_input():
    """
    Captures target job role and optional job description from the user via Streamlit UI.
    Returns:
        tuple (job_role, job_description)
    """

    st.subheader("🎯 Enter Job Role & Description")

    job_role = st.text_input("Target Job Role", placeholder="e.g. Data Analyst, Software Engineer")

    job_desc = st.text_area("Paste Job Description (optional)", placeholder="Paste the full job listing here...")

    if not job_desc.strip():
        job_desc = textwrap.dedent("""
            [No description provided]
            You can paste a full job listing here to improve feedback.
        """).strip()

    return job_role, job_desc


# Example usage inside Streamlit
if __name__ == "__main__":
    st.title("🚀 Resume Reviewer Setup")
    role, desc = get_job_input()
    if st.button("✅ Confirm Input"):
        st.write("🔹 Role:", role)
        st.write("🔹 Description:", desc)
