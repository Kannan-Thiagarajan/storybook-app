import streamlit as st
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import requests

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="Storybook Reflection Corner",
    page_icon="📚",
    layout="centered"
)

# --- CONSTANTS ---
SCHOOL_LOGO_URL = "https://kannan-thiagarajan.github.io/d7/d7.png"
TEACHER_AVATAR_URL = "https://kannan-thiagarajan.github.io/teacher/teacher.png"
SCHOOL_NAME = "SJKT Ladang Sungai Ular"
CREATOR_NAME = "Kannan Thiagarajan"

# --- HELPER FUNCTION: GENERATE PDF ---
def generate_certificate(student_name, book_title, author, moral):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # 1. Draw Border
    c.setStrokeColorRGB(0.2, 0.4, 0.6)
    c.setLineWidth(5)
    c.rect(30, 30, width-60, height-60)
    
    # 2. Add School Logo
    try:
        logo_response = requests.get(SCHOOL_LOGO_URL)
        if logo_response.status_code == 200:
            logo_img = ImageReader(io.BytesIO(logo_response.content))
            c.drawImage(logo_img, width/2 - 40, height - 130, width=80, height=80, mask='auto')
    except:
        pass # If logo fails, just skip it

    # 3. Header Text
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(width/2, height - 170, "Certificate of Completion")
    
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height - 200, SCHOOL_NAME)

    # 4. Main Content
    c.setFont("Helvetica", 18)
    text = f"This certifies that {student_name}"
    c.drawCentredString(width/2, height - 260, text)
    
    c.setFont("Helvetica", 14)
    text2 = f"has successfully completed a reading reflection for the book:"
    c.drawCentredString(width/2, height - 290, text2)
    
    c.setFont("Helvetica-BoldOblique", 20)
    c.drawCentredString(width/2, height - 330, f"'{book_title}' by {author}")

    # 5. The Moral (Lesson)
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(width/2, height - 380, f"Key Lesson Learned: \"{moral}\"")

    # 6. Footer / Signatures
    c.setFont("Helvetica", 10)
    c.drawString(100, 80, f"Verified by AI Teacher")
    c.drawString(width - 250, 80, f"App Created by: {CREATOR_NAME}")
    
    # AI Teacher Image in Footer
    try:
        teacher_response = requests.get(TEACHER_AVATAR_URL)
        if teacher_response.status_code == 200:
            teacher_img = ImageReader(io.BytesIO(teacher_response.content))
            c.drawImage(teacher_img, 60, 100, width=50, height=50, mask='auto')
    except:
        pass

    c.save()
    buffer.seek(0)
    return buffer

# --- MAIN APP UI ---
# Display Header with Columns
col1, col2 = st.columns([1, 4])
with col1:
    st.image(SCHOOL_LOGO_URL, width=100)
with col2:
    st.title("Storybook Reflection Corner")
    st.write(f"**{SCHOOL_NAME}**")

st.divider()

# Intro Section with AI Teacher
c1, c2 = st.columns([1, 3])
with c1:
    st.image(TEACHER_AVATAR_URL, caption="AI Teacher", width=120)
with c2:
    st.info(f"👋 Hello! I am your AI Teacher. Please tell me about the book you read, and I will generate a special certificate for you!")

# Instructions (This replaces your broken HTML list)
st.markdown("""
### 🚀 How it works:
* ✨ Read **ANY** book you like.
* 📝 Fill in the details below.
* 🎓 Click submit to get your certificate!
""")

st.divider()

# Input Form
with st.form("reflection_form"):
    s_name = st.text_input("Student Name")
    b_title = st.text_input("Book Title")
    b_author = st.text_input("Author")
    b_moral = st.text_area("What was the moral or lesson of the story?")
    
    submitted = st.form_submit_button("Submit & Generate Certificate")

# Logic on Submit
if submitted:
    if s_name and b_title and b_author and b_moral:
        st.success(f"Great job, {s_name}! Generating your certificate now...")
        
        # Generate PDF
        pdf_file = generate_certificate(s_name, b_title, b_author, b_moral)
        
        # Download Button
        st.download_button(
            label="📥 Download Your Certificate",
            data=pdf_file,
            file_name=f"Certificate_{s_name}.pdf",
            mime="application/pdf"
        )
        st.balloons()
    else:
        st.error("Please fill in all the fields so I can make your certificate!")
