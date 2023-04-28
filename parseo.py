import ai21
import streamlit as st
import textstat
import chardet
import pandas as pd

ai21.api_key = "f25QoeZfixey11leRFNFBNTlKwwcRdZW"

keywords_prompt = "Task: Generate important keywords based on an input or uploaded text text:\n{description}\n. Output: A list of the more important SEO keywords that accurately represent the content of the input text. Prompt: Develop an algorithm that analyses the input text and generates a list of relevant SEO keywords. The list should include primary and secondary keywords that are important for search engine optimization. The keywords should be selected based on their relevance to the content and their search volume. The algorithm should prioritize popular and commonly searched terms while also considering the specific context of the input text.The final output should be a list of keywords in a readable and user-friendly format. Each keyword should be separated by a comma or line break, and the list should be presented in order of importance with primary keywords at the top. The maximum number of keywords should be limited to 15 to ensure relevance and usability in a list."
title_prompt = "Task: Generate a Meta Title for a given text text:\n{description}\n. Output: A Meta Title that accurately represents the content of the input text and is optimized for search engine ranking. Prompt: Develop an algorithm that analyzes the input text and generates an optimized Meta Title. The Meta Title should accurately represent the content of the text while also containing important keywords for search engine ranking. The algorithm should prioritize popular and commonly searched terms while also considering the specific context of the input text.The final output should be a Meta Title that is concise, clear, and user-friendly. It should not exceed the maximum length of 60 characters to ensure maximum visibility on search engine result pages. The Meta Title should also include the primary keyword at the beginning of the title, followed by any secondary keywords, and the brand name (if applicable) at the end."
description_prompt = "Task: Generate a Meta Description for a given text. text:\n{description}\n.Output: A Meta Description that accurately summarizes the content of the input text and is optimized for search engine ranking.Prompt: Develop an algorithm that analyzes the input text and generates an optimized Meta Description. The Meta Description should provide a concise and accurate summary of the content of the text while also containing important keywords for search engine ranking. The algorithm should prioritize popular and commonly searched terms while also considering the specific context of the input text.The final output should be a Meta Description that is compelling, engaging, and user-friendly. It should not exceed the maximum length of 155 characters to ensure maximum visibility on search engine result pages. The Meta Description should include the primary keyword at the beginning of the description, followed by any secondary keywords, and a clear call-to-action (if applicable)."
tags_prompt = "Generate SEO tags for text:\n{description}\n, prioritizing popular and commonly searched terms, and limiting the tags to 10 for relevance and usability. Output: A list of SEO tags that accurately represent the content of the input text and are optimized for search engine ranking. Prompt: Develop an algorithm that analyzes the input text and generates optimized SEO tags. The SEO tags should accurately represent the content of the text while also containing primary and secondary keywords for search engine ranking. The algorithm should prioritize popular and commonly searched terms while also considering the specific context of the input text.The final output should be a list of up to 10 SEO tags that are readable, user-friendly, and presented in order of importance. Each tag should contain at least one primary keyword and be relevant to the content of the input text."

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
        numResults=3,
    )
    seo_title = response.completions[0].data.text

    return seo_title

    # Generate meta description
def generate_description(text):
    prompt = description_prompt.format(description=text)
    response = ai21.Completion.execute(
        model="j2-grande-instruct",
        prompt=prompt,
        temperature=0.6,
        minTokens=1,
        maxTokens=150,
        numResults=3,
    )
    seo_description = response.completions[0].data.text

    return seo_description

    # Generate tags
def generate_tags(text):
    prompt = tags_prompt.format(description=text)
    response = ai21.Completion.execute(
        model="j2-jumbo-instruct",
        prompt=prompt,
        temperature=0.6,
        minTokens=1,
        maxTokens=150,
        numResults=3,
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
        temperature=0.6,
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


st.image("https://github.com/Juancorreaph/parseo/blob/93b0b40aad58beccf68f853fdf51654f23189810/logo-parseo-white.png")
st.title("Welcome to parseo, parce!")
st.write("Elevate your content with our all-in-one AI solution, designed to streamline your workflow and help you create content that stands out!")
st.divider()
# Add file upload option
uploaded_file = st.file_uploader("Upload a text document", type=["txt", "docx"])
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
    col1, col2 = st.columns(2 , gap="medium")
    with col1:
        st.header("SEO Title")
        st.write(st.session_state.output[2])
        
    with col2:
        st.header("Keywords")
        st.write(f"{st.session_state.output[0]}")

    st.divider()

    st.header("Flesh Kincaid Grade")
    st.write("The Flesch-Kincaid grade is a readability formula that calculates the grade level needed to understand a piece of text based on its average sentence length and syllable count.")
    st.subheader(f"Grade Level: {st.session_state.output[1]}")
    st.image("https://github.com/Juancorreaph/parseo/blob/main/score%20table.png")


    st.divider()   
    
    col1, col2= st.columns(2 , gap="medium") 
    with col1:
        st.header("Meta Description")
        if st.session_state.output and len(st.session_state.output) >= 4:
            st.write(st.session_state.output[3])
        else:
            st.write("No SEO description generated.")
    with col2:
        st.header("Tags")
        if st.session_state.output and len(st.session_state.output) >= 4:
            st.write(st.session_state.output[4])
        else:
            st.write("No SEO description generated.")
