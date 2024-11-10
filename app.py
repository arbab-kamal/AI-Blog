import streamlit as st
import google.generativeai as genai
from openai import OpenAI
from streamlit_carousel import carousel
from dotenv import load_dotenv
import os

load_dotenv()
client=OpenAI(api_key=os.environ["openai_api_key"])
genai.configure(api_key=os.environ["GEMINI_API_KEY"])


single_image=dict(
    title="",
    text="",
    interval=None,
    img=""
)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)


st.set_page_config(layout="wide")
st.title('✍️🤖 BlogCraft : Your AI writing companion')

st.subheader("Now you can craft perfect blogs with the help of AI- BlogCraft is your New AI Blog Companion")
with st.sidebar:
    st.title("Input Your Blog Detail")
    st.subheader("Enter Details of the Blog you want to generate")
    blog_title=st.text_input("Blog Title")
    keywords=st.text_area("Keywords (comma-separated)")
    num_words=st.slider("Number of Words",min_value=250,max_value=2000,step=250)
    num_images=st.number_input("Number of Images",min_value=1,max_value=5,step=1)
    
    prompt_parts=[
        f"Generate  a comprehensive engaging blog post relevant to the given title\"{blog_title}\" and keywords\"{keywords}\".The blog should be approximately{num_words} words in length,suitable for online audience.Ensure the content is original informative and maintains a consistent tone throughout"
        ]
    
    submit_button=st.button("Generate Blog")
if submit_button:
    response = model.generate_content(prompt_parts)
    images=[]
    images_gallery=[]
    for i in range (num_images):
        image_response = client.images.generate(
        model="dall-e-3",
        prompt=f"Generate a Blog Post Image on Title: {blog_title}",
        size="1024x1024",
        quality="standard",
        n=1,
        )
        new_image=single_image.copy()
        new_image["title"]=f"Image {i+1}"
        new_image["text"]=f"{blog_title}"
        new_image["img"]=image_response.data[0].url
        images_gallery.append(new_image)


    st.title("YOUR BLOG IMAGE(S) ARE HERE:")
    carousel(items=images_gallery,width=1)
    st.title("YOUR BLOG POST")
    st.write(response.text)