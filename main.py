import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
    flipkartSearch,
    amazonSearch
)
from parse import parse_with_ollama
import pandas as pd
from gemini import bard

# Streamlit UI
st.title("Web Scraper")

# Help section
st.sidebar.header("Help")
st.sidebar.text("1. Enter a valid website URL.")
st.sidebar.text("2. Click 'Scrape Website' to get the content.")
st.sidebar.text("3. Describe what you want to parse and click 'Parse Content'.")

# User input
urlQuery = st.text_input("Enter Query")


def scrapeFunction(url):
    if url:
        with st.spinner("Scraping the website..."):
            try:
                dom_content = scrape_website(url)
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)

                # Store the DOM content in Streamlit session state
                st.session_state.dom_content = cleaned_content

                # Display the DOM content in an expandable text box
                with st.expander("View DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)

                st.success("Scraping completed successfully.")

            except Exception as e:
                st.error(f"An error occurred during scraping: {e}")

if st.button("Scrape Website [URL]"):
    scrapeFunction(urlQuery)

#Scrape the Website
if st.button("Scrape Query using Flipkart "):
    url = flipkartSearch(urlQuery)
    scrapeFunction(url)

if st.button("Scrape Query using Amazon "):
    url = amazonSearch(urlQuery)
    scrapeFunction(url)
# Export DOM content to CSV
if st.button("Export Content"):
    if "dom_content" in st.session_state:
        try:
            # Export DOM content to a CSV file
            with open("dom_content.csv", "w") as f:
                f.write(st.session_state.dom_content)
            st.success("DOM content exported as CSV.")
        except Exception as e:
            st.error(f"An error occurred while exporting: {e}")

#Parse Content using Ollama
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            with st.spinner("Parsing the content..."):
                try:
                    # Parse the content with Ollama
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    parsed_result = parse_with_ollama(dom_chunks, parse_description)
                    st.write(parsed_result)

                    # Save parsed result to a file
                    with open("parsed_result_ollama.txt", "w") as f:
                        f.write(parsed_result)  
                    st.success("Parsed result saved as parsed_result_ollama.txt.")
                except Exception as e:
                    st.error(f"An error occurred during parsing: {e}")

    if st.button("Parse Content using Gemini"):
        if parse_description:
            with st.spinner("Parsing the content..."):
                try:
                    # Parse the content with Ollama
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    parsed_result = bard(dom_chunks,parse_description)
                    st.write(parsed_result)

                    with open("parsed_result_gemini.txt", "w") as f:
                        f.write(parsed_result)  
                    st.success("Parsed result saved as parsed_result_gemini.txt.")
                    
                except Exception as e:
                    st.error(f"An error occurred during parsing: {e}")
