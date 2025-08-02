import streamlit as st
import pandas as pd
import io

# --- Load data functions ---
@st.cache_data
def load_job_data():
    df = pd.read_csv("jobs.csv")
    df.columns = df.columns.str.strip()
    return df

@st.cache_data
def load_program_skills():
    df = pd.read_csv("program_skills.csv")
    df.columns = df.columns.str.strip()
    return df

# Load both datasets
job_df = load_job_data()
program_df = load_program_skills()

st.title("🔍 Job Skills Finder + Program Comparison")

# Step 1: Select field
fields = job_df['Field'].dropna().unique().tolist()
fields.sort()
selected_field = st.selectbox("Select a field:", ["--Select field--"] + fields)

if selected_field != "--Select field--":
    # Step 2: Select job title within the selected field
    jobs = job_df[job_df['Field'] == selected_field]['Job Title'].dropna().unique().tolist()
    jobs.sort()
    selected_job = st.selectbox("Select a job title:", ["--Select job--"] + jobs)

    if selected_job != "--Select job--":
        # Step 3: Select program unit (optional)
        program_units = program_df['Program Unit'].dropna().unique().tolist()
        program_units.sort()
        selected_program = st.selectbox("Select a program unit (optional):", ["--None--"] + program_units)

        # Step 4: Get job-related skills
        matching_jobs = job_df[(job_df['Field'] == selected_field) & (job_df['Job Title'] == selected_job)]

        if not matching_jobs.empty:
            for _, row in matching_jobs.iterrows():
                st.subheader(f"🔧 Skills for: {row['Job Title']} in {row['Field']}")

                # Extract skills from job row
                tech_skills = [skill.strip().lower() for skill in str(row['Technical skills']).split(',')]
                general_skills = [skill.strip().lower() for skill in str(row['General Skills']).split(',')]
                all_required_skills = set(tech_skills + general_skills)

                st.markdown("**🛠️ Technical Skills:**")
                for skill in tech_skills:
                    st.markdown(f"- {skill.title()}")

                st.markdown("")  # Spacing

                st.markdown("**💡 General Skills:**")
                for skill in general_skills:
                    st.markdown(f"- {skill.title()}")

                # --- Build the report content
                report = io.StringIO()
                report.write(f"Job Skills Report\n")
                report.write(f"=================\n")
                report.write(f"Field: {selected_field}\n")
                report.write(f"Job Title: {selected_job}\n")

                if selected_program != "--None--":
                    report.write(f"Program Unit: {selected_program}\n\n")
                else:
                    report.write(f"Program Unit: Not selected\n\n")

                report.write("Required Technical Skills:\n")
                for skill in tech_skills:
                    report.write(f"- {skill.title()}\n")

                report.write("\nRequired General Skills:\n")
                for skill in general_skills:
                    report.write(f"- {skill.title()}\n")

                if selected_program != "--None--":
                    st.markdown("### 🎓 Program Skills Comparison")
                    program_skills = program_df[program_df['Program Unit'] == selected_program]['Skill'].dropna().str.lower().str.strip().tolist()
                    program_skills_set = set(program_skills)

                    matched = all_required_skills & program_skills_set
                    extra = program_skills_set - all_required_skills

                    st.markdown("✅ **Matching Skills:**")
                    for skill in sorted(matched):
                        st.markdown(f"- {skill.title()}")
                        report.write(f"\nMatching Skill: {skill.title()}")

                    st.markdown("➕ **Extra Skills (Taught but not required):**")
                    for skill in sorted(extra):
                        st.markdown(f"- {skill.title()}")
                        report.write(f"\nExtra Skill: {skill.title()}")

                else:
                    st.markdown("ℹ️ No program unit selected. Comparison not available.")
                    report.write("\n(No program selected — no comparison performed)\n")

                # Download button
                report_text = report.getvalue()
                st.download_button(
                    label="📥 Download Report",
                    data=report_text,
                    file_name=f"{selected_job}_skills_report.txt",
                    mime="text/plain"
                )

                st.markdown("---")
        else:
            st.warning("❌ No matching job found for this field and job title combination.")



