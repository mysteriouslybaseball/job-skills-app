import streamlit as st
import pandas as pd

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
        # Step 3: Select program unit
        program_units = program_df['Program Unit'].dropna().unique().tolist()
        program_units.sort()
        selected_program = st.selectbox("Select a program unit:", ["--Select program unit--"] + program_units)

        # Step 4: Get job-related skills
        matching_jobs = job_df[(job_df['Field'] == selected_field) & (job_df['Job Title'] == selected_job)]

        if not matching_jobs.empty:
            for _, row in matching_jobs.iterrows():
                st.subheader(f"🔧 Skills for: {row['Job Title']} in {row['Field']}")

                # Extract skills from job row
                tech_skills = [skill.strip().lower() for skill in str(row['Technical skills']).split(',')]
                general_skills = [skill.strip().lower() for skill in str(row['General Skills']).split(',')]
                all_required_skills = set(tech_skills + general_skills)

                # Display job skills
                st.markdown("**🛠️ Technical Skills:**")
                for skill in tech_skills:
                    st.markdown(f"- {skill.title()}")
                st.markdown("**💡 General Skills:**")
                for skill in general_skills:
                    st.markdown(f"- {skill.title()}")

                # If a program unit is selected
                if selected_program != "--Select program unit--":
                    st.markdown("### 🎓 Program Skills Comparison")
                    program_skills = program_df[program_df['Program Unit'] == selected_program]['Skill'].dropna().str.lower().str.strip().tolist()
                    program_skills_set = set(program_skills)

                    # Compare
                    matched = all_required_skills & program_skills_set
                    missing = all_required_skills - program_skills_set
                    extra = program_skills_set - all_required_skills

                    st.markdown("✅ **Matching Skills:**")
                    if matched:
                        for skill in sorted(matched):
                            st.markdown(f"- {skill.title()}")
                    else:
                        st.write("_None_")

                    st.markdown("❌ **Missing Skills (Required but not taught):**")
                    if missing:
                        for skill in sorted(missing):
                            st.markdown(f"- {skill.title()}")
                    else:
                        st.write("_None_")

                    st.markdown("➕ **Extra Skills (Taught but not required):**")
                    if extra:
                        for skill in sorted(extra):
                            st.markdown(f"- {skill.title()}")
                    else:
                        st.write("_None_")

                st.markdown("---")
        else:
            st.warning("❌ No matching job found for this field and job title combination.")


