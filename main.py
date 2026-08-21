import streamlit as st
from google import genai
import os

st.set_page_config(page_title="ApplyEasy 💼🤝🏽")
st.title("ApplyEasy: Make Applying to Jobs Easier 💼🤝🏽")
st.caption("Enter information about the job you're eyeing and your skills - we'll optimize your application. 🔎")


jobDescription = st.text_area("Type or paste information about the job here, including its description and any necessary skills and qualifications. 💻")
userSkills = st.text_area("Type or paste key skills, qualifications, or experiences that you possess. 💡")


if st.button("Enter!"):
    if jobDescription and userSkills:
        with st.spinner("Thinking... 🤔"):
            # Fetch API key safely across both local and deployed environments
            api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

            if not api_key:
                st.error("API Key not found! Please add GEMINI_API_KEY to your Streamlit Secrets.")
                st.stop()

            client = genai.Client(api_key=api_key)

            prompt = (
                "You are an expert Technical Recruiter with 10 years of experience. Come up with 10 detailed questions that could be asked in a job interview that pertain with the information written in the Job Description.\n"
                "Assess if there is a match between the candidate's skills and the job descriptions.\n"
                "Thoroughly highlight what skills and experiences are matching and what is missing between the candidate and job description\n"
                "Assess if the candidate's experiences are relevant and a good fit for the job.\n"
                "Return the results in two markdown tables: one for the interview questions, and the other for the match with two columns 'Aligned' and 'Unaligned'\n"
                "Ensure the explanations are thoroughly detailed.\n\n"
                f"Job Description:\n{jobDescription}\n\n"
                f"Candidate skills:\n{userSkills}\n\n"
            )
            
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                st.success("Done! Good luck on your application! 😉🎉")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("At least one of the text fields are missing information. 😔")