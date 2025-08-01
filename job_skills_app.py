import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("jobs.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.title("🔍 Job Skills Finder")

# Step 1: Select field
fields = df['Field'].dropna().unique().tolist()
fields.sort()
selected_field = st.selectbox("Select a field:", ["--Select field--"] + fields)

if selected_field != "--Select field--":

    # Step 2: Filter jobs by selected field, then select job title
    jobs = df[df['Field'] == selected_field]['Job Title'].dropna().unique().tolist()
    jobs.sort()
    selected_job = st.selectbox("Select a job title:", ["--Select job--"] + jobs)

    if selected_job != "--Select job--":

        # Step 3: Filter dataframe by both field and job title
        matching_jobs = df[(df['Field'] == selected_field) & (df['Job Title'] == selected_job)]

        if not matching_jobs.empty:
            for _, row in matching_jobs.iterrows():
                st.subheader(f"🔧 Skills for: {row['Job Title']} in {row['Field']}")

                # Display Technical Skills as a bullet-point list
                st.markdown("**🛠️ Technical Skills:**")
                tech_skills = [skill.strip() for skill in str(row['Technical skills']).split(',')]
                for skill in tech_skills:
                    st.markdown(f"- {skill}")

                # Display General Skills as a bullet-point list
                st.markdown("**💡 General Skills:**")
                general_skills = [skill.strip() for skill in str(row['General Skills']).split(',')]
                for skill in general_skills:
                    st.markdown(f"- {skill}")

                st.markdown("---")
        else:
            st.warning("❌ No matching job found for this field and job title combination.")

