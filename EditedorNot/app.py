from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image 
import google.generativeai as genai
import json

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
## Streamlit App

st.set_page_config(page_title="EDITED OR NOT")
st.header("EDITED OR NOT")
st.text("CHECKS WHETHER A PICTURE IS EDITED OR NOT!")
input_text = st.text_area("Give us a hint where might be the picture edited: ", key="input",placeholder="Write here! What do you think?")
uploaded_file = st.file_uploader("Upload your Image...", type=["jpg", "jpeg", "png"])

# if uploaded_file is not None:
#     st.write("Image Uploaded Successfully")
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the Image")


input_prompt = """
 You are an experienced forensic image analyst, your task is to review the provided image.You can take help from the users view which is : {}. 
  Please share your professional evaluation on whether the image is edited or not. 
 Highlight the areas of the image with whatever you think is best to point out the areas.
"""

if submit:
    if uploaded_file is not None:
        image = input_image_setup(uploaded_file)
        formatted_prompt = input_prompt.format(json.dumps(input_text))
        response = get_gemini_response(input_prompt, image, input_text)
        st.subheader("What I think is")
        st.write(response)
    else:
        st.write("Please upload the image")
