import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama
import pandas as pd

# Streamlit UI
st.title("Web Scraper")

# Help section
st.sidebar.header("Help")
st.sidebar.text("1. Enter a valid website URL.")
st.sidebar.text("2. Click 'Scrape Website' to get the content.")
st.sidebar.text("3. Describe what you want to parse and click 'Parse Content'.")

# User input
url = st.text_input("Enter Website URL")

#Scrape the Website
if st.button("Scrape Website"):
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
                except Exception as e:
                    st.error(f"An error occurred during parsing: {e}")
