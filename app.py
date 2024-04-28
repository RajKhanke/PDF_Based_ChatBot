import streamlit as st
import google.generativeai as genai
import os
from PyPDF2 import PdfReader

# Set your API key as an environment variable
os.environ["GOOGLE_API_KEY"] = 'ENTER_YOUR_API_KEY'

# Configure the API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

# CSS styling
css = '''
<style>
.chat-message {
    padding: 1.5rem; 
    border-radius: 0.5rem; 
    margin-bottom: 1rem; 
    display: flex;
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
.bold-heading {
    font-weight: bold;
    font-size: 24px;
    margin-bottom: 20px;
}
.torchlight-sticker {
    width: 24px;
    height: 24px;
    margin-left: 10px;
}
</style>
'''

# HTML template
message_template = '''
<div class="chat-message {}">
    <div class="avatar">
        <img src="{}">
    </div>
    <div class="message">{}</div>
</div>
'''

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def generate_response(pdf_text, user_input):
    # Combine the PDF text and user input to generate a response
    input_text = pdf_text + user_input
    response = model.generate_content(input_text)
    return message_template.format("bot", "https://tse2.mm.bing.net/th?id=OIP.C5v0eJ_tW4UiG9zYK6OWcAHaHa&pid=Api&P=0&h=180", response.text)


# Streamlit app
def main():
    st.markdown(css, unsafe_allow_html=True)

    # Display bold heading with torchlight sticker
    st.header("CHAT WITH PDF 🧠")

    # File uploader for PDF
    pdf_file = st.sidebar.file_uploader("Upload PDF file", type=["pdf"])

    if pdf_file is not None:
        # Process uploaded PDF
        text_from_pdf = extract_text_from_pdf(pdf_file)

        # User input field
        user_input = st.text_input("Ask a question:")

        if user_input:
            # Bot response based on the text from PDF and user input
            bot_response = generate_response(text_from_pdf, user_input)
            st.markdown(message_template.format("user", "https://png.pngtree.com/png-vector/20190710/ourlarge/pngtree-user-vector-avatar-png-image_1541962.jpg", user_input), unsafe_allow_html=True)
            st.markdown(bot_response, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
