import ai21
import streamlit as st
import textstat
import chardet
import pandas as pd

ai21.api_key = "f25QoeZfixey11leRFNFBNTlKwwcRdZW"

keywords_prompt = "Based on the input or uploaded text generate the important SEO keywords that can be used to optimize the content for search engines \nKeywords: {description}\n"
title_prompt = "Based on the input or uploaded text generate a meta title that accurately represents the content of the text. The meta title should be optimized for search engines and be concise yet descriptive. The generated meta title should adhere to best practices for SEO and provide meaningful information about the content of the text.\n{description}\n"
description_prompt = "Based on the input or uploaded text generate a concise and compelling Meta Description that accurately summarizes the content of the text. The Meta Description should be limited to a maximum of 155-160 characters and should contain relevant keywords and phrases to optimize search engine results. The generated Meta Description should effectively convey the purpose and value of the text to potential readers.:\n{description}\n"
tags_prompt = "Given the input text, generate a list of relevant SEO tags to improve the visibility of the content on search engines. Consider the keywords, phrases, and entities present in the text to generate the tags. The output should be a list of words or phrases that could be used as tags for the content.:\n{description}\n"

# Initialization of the output variable
if "output" not in st.session_state:
    st.session_state.output = None

    # Generate Flesch Score
def generate_score(text):
    score = textstat.flesch_kincaid_grade(text)
    return score
    
    # Generate SEO title
def generate_title(text):
    prompt = title_prompt.format(description=text)
    response = ai21.Completion.execute(
        model="j2-grande-instruct",
        prompt=prompt,
        temperature=0.5,
        minTokens=1,
        maxTokens=40,
        numResults=1,
    )
    seo_title = response.completions[0].data.text

    return seo_title

    # Generate meta description
def generate_description(text):
    prompt = description_prompt.format(description=text)
    response = ai21.Completion.execute(
        model="j2-grande-instruct",
        prompt=prompt,
        temperature=0.5,
        minTokens=1,
        maxTokens=200,
        numResults=1,
    )
    seo_description = response.completions[0].data.text

    return seo_description

    # Generate tags
def generate_tags(text):
    prompt = tags_prompt.format(description=text)
    response = ai21.Completion.execute(
        model="j2-grande-instruct",
        prompt=prompt,
        temperature=0.5,
        minTokens=1,
        maxTokens=100,
        numResults=1,
    )
    seo_tags = response.completions[0].data.text

    return seo_tags

def generate_seo_data(inp):
    if not len(inp):
        return None

    score = generate_score(inp)    

    # Generate keywords
    prompt = keywords_prompt.format(description=inp)
    response = ai21.Completion.execute(
        model="j2-grande-instruct",
        prompt=prompt,
        temperature=0.5,
        minTokens=1,
        maxTokens=100,
        numResults=1,
    )

    # Generate responses
    seo_title = generate_title(inp)
    seo_description = generate_description(inp)
    seo_tags = generate_tags(inp)

    # return the data
    st.session_state["output"] = response.completions[0].data.text, score, seo_title, seo_description , seo_tags


st.image("https://github.com/Juancorreaph/parseo/blob/5a90601d83917f145640c96c7dcfc2842349a8e7/logo-parseo-white.png")
st.title("Welcome to parseo, parce!")
st.write("Elevate your content with our all-in-one AI solution, designed to streamline your workflow and help you create content that stands out!")
st.divider()
# Add file upload option
uploaded_file = st.file_uploader("Upload a text document", type=["txt"])
if uploaded_file is not None:
        # Read the contents of the file
        file_contents = uploaded_file.read()
        # Detect the character encoding of the file
        encoding = chardet.detect(file_contents)['encoding']
        # If the detected encoding is None, use utf-8 as the default encoding
        encoding = encoding or 'utf-8'
        try:
            # Decode the file contents using the detected encoding
            file_contents = file_contents.decode(encoding, errors='strict')
        except UnicodeDecodeError:
            # If decoding fails, try again using 'replace' as the error handler
            file_contents = file_contents.decode(encoding, errors='replace')
        st.text(file_contents)
        generate_seo_data(file_contents)
        
        # check if file_contents is defined before using it
        if 'file_contents' in locals():
            # do something with file_contents
            encoding = chardet.detect(file_contents.encode())['encoding']
        
st.divider()
inp = st.text_area("Or enter your text here")
st.button("Generate my SEO parce!", on_click=lambda: generate_seo_data(inp))


if st.session_state.output:
    col1, col2, col3 = st.columns(3 , gap="medium")
    with col1:
        st.header("SEO Title")
        st.write(st.session_state.output[2])
        

    with col2:
        st.header("Flesh Kincaid Grade")
        st.subheader(f"{st.session_state.output[1]}")

    with col3:
        st.header("Keywords")
        st.write(f"{st.session_state.output[0]}")


    
    col1, col2= st.columns(2 , gap="medium") 
    with col1:
        st.header("Meta Description")
        if st.session_state.output and len(st.session_state.output) >= 4:
            st.write(st.session_state.output[4])
        else:
            st.write("No SEO description generated.")
    with col2:
        st.header("Tags")
        if st.session_state.output and len(st.session_state.output) >= 4:
            st.write(st.session_state.output[3])
        else:
            st.write("No SEO description generated.")
