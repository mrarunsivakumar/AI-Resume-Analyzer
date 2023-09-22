import streamlit as st
import pdfplumber
import openai
import io
import time
import re
import spacy

# Set up OpenAI API key
openai.api_key = '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'  # Replace with your actual API key

# Streamlit App
st.markdown('<h1 style="color: red;">AI Resume Analyzer</h1>', unsafe_allow_html=True)

# Sidebar for user input
st.sidebar.header("Input")
uploaded_resume = st.sidebar.file_uploader("Upload a resume (PDF)", type=["pdf"])

# Function to analyze the resume using OpenAI's LLM
def analyze_resume(resume_text, user_domain):
    # Customize the prompt based on your analysis requirements
    prompt = f"Analyze the following resume:\n{resume_text}\n\nUser Domain: {user_domain}\n\nAnalysis:\n"
    
    # Generate analysis using GPT-4 (LLM)
    response = openai.Completion.create(
        engine="text-davinci-002",  # Use the appropriate LLM engine
        prompt=prompt,
        max_tokens=150  # Adjust this when  needed
    )
    
    return response.choices[0].text

# Function to extract text from PDF using pdfplumber
def extract_text_from_pdf(pdf_file):
    pdf_bytes_io = io.BytesIO(pdf_file)
    resume_text = ""
    with pdfplumber.open(pdf_bytes_io) as pdf:
        for page in pdf.pages:
            resume_text += page.extract_text()
    return resume_text

# Function to predict candidate experience level
def predict_experience_level(resume_text):
    
    if 'EXPERIENCE' in resume_text:
        return "Experienced"      
    elif 'INTERNSHIP' in resume_text:
        return "Intermediate"        
    else:
        return "Fresher"
        
# Function for skill recommendations based on domain
def skill_recommendations(user_domain, resume_text):
    ds_keywords = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep learning', 'python', 'nlp', 'computer vision', 'statistics']
    data_analyst_keywords = ['python', 'statistics', 'sql', 'power bi', 'tableau', 'excel']
    data_engineering_keywords = ['hadoop', 'pyspark', 'kafka', 'sql', 'amazon redshift', 'aws', 'azure', 'google cloud']
    web_keywords = ['html', 'css', 'react', 'django', 'node.js', 'react.js', 'php', 'laravel', 'magento', 'wordpress', 'javascript', 'angular js', 'c#', 'asp.net', 'flask']
    android_keywords = ['android', 'flutter', 'kotlin', 'xml', 'kivy']
    ios_keywords = ['ios', 'swift', 'cocoa', 'cocoa touch', 'xcode']
    uiux_keywords = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes', 'storyframes', 'adobe photoshop','adobe illustrator']

    # Function to check if any skill keywords exist in the text
    def find_matching_skills(keywords, text):
        matching_skills = [keyword for keyword in keywords if re.search(fr'\b{keyword}\b', text, re.IGNORECASE)]
        return matching_skills

    if user_domain == 'data science':
        recommended_skills = find_matching_skills(ds_keywords, resume_text)
    elif user_domain == 'data analyst':
        recommended_skills = find_matching_skills(data_analyst_keywords, resume_text)
    elif user_domain == 'data engineering':
        recommended_skills = find_matching_skills(data_engineering_keywords, resume_text)
    elif user_domain == 'web development':
        recommended_skills = find_matching_skills(web_keywords, resume_text)
    elif user_domain == 'android developer':
        recommended_skills = find_matching_skills(android_keywords, resume_text)
    elif user_domain == 'ios developer':
        recommended_skills = find_matching_skills(ios_keywords, resume_text)
    elif user_domain == 'ui/ux developer':
        recommended_skills = find_matching_skills(uiux_keywords, resume_text)
    else:
        recommended_skills = []

    return recommended_skills


# Function to calculate resume score
def calculate_resume_score(resume_text):
    # Initialize the score
    resume_score = 0
    st.subheader("Score Analysis")
   
    
    
    # Check for the presence of 'Objective' or 'Summary'
    if 'Objective' in resume_text or 'Summary' in resume_text:
        resume_score += 5
        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective/Summary</h4>''',unsafe_allow_html=True)                
    else:        
        st.markdown('''<h5 style='text-align: left; color: #FF0000;'>[-] Please add your career objective, it will give your career intention to the Recruiters.</h5>''', unsafe_allow_html=True)

    # Check for the presence of 'Education', 'School', or 'College'
    if 'Education' in resume_text or 'School' in resume_text or 'College' in resume_text:
        resume_score += 10
        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Education Details</h4>''',unsafe_allow_html=True)
    else:
        st.markdown('''<h5 style='text-align: left; color: #FF0000;'>[-] Please add Education. It will give your Qualification level to the recruiter</h5>''', unsafe_allow_html=True)

    # Check for the presence of 'EXPERIENCE' or 'Experience'
    if 'EXPERIENCE' in resume_text or 'Experience' in resume_text:
        resume_score += 15
        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Experience</h4>''',unsafe_allow_html=True)
    else:
        st.markdown('''<h5 style='text-align: left; color: #FF0000;'>[-] Please add Experience. It will help you stand out from the crowd</h5>''', unsafe_allow_html=True)

    # Check for the presence of 'INTERNSHIPS' or 'INTERNSHIP' or 'Internships' or 'Internship'
    if 'INTERNSHIPS' in resume_text or 'INTERNSHIP' in resume_text or 'Internships' in resume_text or 'Internship' in resume_text:
        resume_score += 9
        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
    else:
        st.markdown('''<h5 style='text-align: left; color: #FF0000;'>[-] Please add Internships. It will help you stand out from the crowd</h5>''', unsafe_allow_html=True)

    # Check for the presence of 'SKILLS', 'SKILL', 'Skills', or 'Skill'
    if 'SKILLS' in resume_text or 'SKILL' in resume_text or 'Skills' in resume_text or 'Skill' in resume_text:
        resume_score += 8
        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
    else:
        st.markdown('''<h5 style='text-align: left; color: #FF0000;'>[-] Please add Skills. It will help you a lot</h5>''', unsafe_allow_html=True)

    # Check for the presence of 'HOBBIES' or 'Hobbies'
    if 'HOBBIES' in resume_text or 'Hobbies' in resume_text:
        resume_score += 4
        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies</h4>''',unsafe_allow_html=True)
    else:        
        st.markdown('''<h5 style='text-align: left; color: #FF0000;'>[-] Please add Hobbies. It will show your personality to the Recruiters and give the assurance that you are fit for this role or not.</h5>''', unsafe_allow_html=True)

    # Check for the presence of 'INTERESTS' or 'Interests'
    if 'INTERESTS' in resume_text or 'Interests' in resume_text:
        resume_score += 5
        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Interests</h4>''',unsafe_allow_html=True)
    else:        
        st.markdown('''<h5 style='text-align: left; color: #FF0000;'>[-] Please add Interests. It will show your interests other than the job.</h5>''', unsafe_allow_html=True)

    # Check for the presence of 'ACHIEVEMENTS' or 'Achievements'
    if 'ACHIEVEMENTS' in resume_text or 'Achievements' in resume_text:
        resume_score += 12
        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements</h4>''',unsafe_allow_html=True)
    else:        
        st.markdown('''<h5 style='text-align: left; color: #FF0000;'>[-] Please add Achievements. It will show that you are capable for the required position.</h5>''', unsafe_allow_html=True)

    # Check for the presence of 'CERTIFICATIONS', 'Certifications', or 'Certification'
    if 'CERTIFICATIONS' in resume_text or 'Certifications' in resume_text or 'Certification' in resume_text:
        resume_score += 12
        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications</h4>''',unsafe_allow_html=True)
    else:
        st.markdown('''<h5 style='text-align: left; color: #FF0000;'>[-] Please add Certifications. It will show that you have done some specialization for the required position.</h5>''', unsafe_allow_html=True)

    # Check for the presence of 'PROJECTS', 'PROJECT', 'Projects', or 'Project'
    if 'PROJECTS' in resume_text or 'PROJECT' in resume_text or 'Projects' in resume_text or 'Project' in resume_text:
        resume_score += 20
        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
    else:
        st.markdown('''<h5 style='text-align: left; color: #FF0000;'>[-] Please add Projects. It will show that you have done work related to the required position or not.</h5>''', unsafe_allow_html=True)
   
    
    return resume_score

#function for basic information:
def extract_basic_info(resume_text, pdf_content=None):
    name = None
    email = None
    contact = None
    no_of_pages = None

    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(resume_text)

    # Define regular expressions for extracting email and phone number
    email_pattern = r'(?i)([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
    phone_pattern = r'(?i)(\b\d{10}\b|\+\d{2,3}\s?\d{10})'

    # Search for email and phone number using regular expressions
    email_match = re.search(email_pattern, resume_text)
    phone_match = re.search(phone_pattern, resume_text)

    # Extract email and phone number if found
    if email_match:
        email = email_match.group().strip()
    if phone_match:
        contact = phone_match.group().strip()

    # Get the number of pages from the pdf content
    if pdf_content:
        with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
            no_of_pages = len(pdf.pages)

    # Extract names based on capitalization and context
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Check if the name contains more than one word
            if len(ent.text.split()) > 1:
                name = ent.text.strip()
                break

    return name, email, contact, no_of_pages

# Main content area
if uploaded_resume is not None:
    with st.spinner("Analyzing..."):
        # Read the PDF file as bytes
        pdf_file = uploaded_resume.read()
        
        # Extract text from PDF using pdfplumber
        resume_text = extract_text_from_pdf(pdf_file)
        
        # Extract user domain (you can replace this with actual user input)
        user_domain = st.text_input("Enter User Domain (e.g., data science, data analyst):")
       
        
        
        if user_domain:
            # Analyze the resume
            analysis = analyze_resume(resume_text, user_domain)
    
            st.subheader("Resume Analysis:")
            st.write(analysis)

            # Extract and display basic information
            name, email, contact, no_of_pages= extract_basic_info(resume_text,pdf_file)
            
            st.subheader("Basic Information")
            if name:
              st.write(f"Name: {name}")
            if email:
              st.write(f"Email: {email}")
            if contact:
              st.write(f"Contact: {contact}")
            if no_of_pages:
              st.write(f"Total Resume Pages: {no_of_pages}")

            
            # Predict candidate experience level
            experience_level = predict_experience_level(resume_text)
            st.subheader("Candidate Experience Level")
            # Display the experience level with different colors
            if experience_level == "Experienced":
                st.markdown('''<h4 style='text-align: left; color: #fba171;'>Experienced</h4>''', unsafe_allow_html=True)
            elif experience_level == "Intermediate":
                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Intermediate</h4>''', unsafe_allow_html=True)
            else:
                st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>Fresher</h4>''', unsafe_allow_html=True)
            

           
            
            

            # Display recommended skills
            st.subheader("Recommended Skills:")
            if user_domain and resume_text:
               recommended_skills = skill_recommendations(user_domain, resume_text)

              
               if recommended_skills:
                  
                  recommended_keywords = ', '.join(recommended_skills)
                  st.markdown(f"**Recommended skills for you:** <font color='#1ed760'>{recommended_keywords}</font>", unsafe_allow_html=True)
               else:
                   st.warning("No recommendations available for this domain.")
            

            resume_score = calculate_resume_score(resume_text)
            st.subheader("**Resume Score 📝**")
                
            st.markdown(
               """
               <style>
                  .stProgress > div > div > div > div {
                      background-color: #d73b5c;
                  }
               </style>""",
               unsafe_allow_html=True,
            )
            ### Score Bar
            my_bar = st.progress(0)
            score = 0
            for percent_complete in range(resume_score):
               score +=1
               time.sleep(0.1)
               my_bar.progress(percent_complete + 1)

            ### Score
            st.success('Your Resume Writing Score: ' + str(score)+'**')
            st.warning("** Note: This score is calculated based on the content that you have in your Resume. **")
             
               
else:
    st.info("Please upload a PDF resume to analyze.")
