import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import base64
from io import BytesIO
import zipfile
import os

st.title('Very Basic Scraper')
st.subheader('by Vincent A')


url = st.text_input('Enter the URL of the website')

def add_tag():
    st.session_state.tags.append({'tag': '', 'class_name': ''})

if 'tags' not in st.session_state:
    st.session_state.tags = [{'tag': '', 'class_name': ''}]

col1, col2 = st.columns([1, 5])
with col1:
    st.header('Tags')
with col2:
    ""
    if st.button('Add another tag'):
        add_tag()

for i, tag_input in enumerate(st.session_state.tags):
    cols = st.columns(2)
    tag_input['tag'] = cols[0].text_input(f'Enter HTML tag {i+1}', value=tag_input['tag'], key=f'tag_{i}')
    tag_input['class_name'] = cols[1].text_input(f'Enter class name for tag {i+1} (optional)', value=tag_input['class_name'], key=f'class_{i}')

if 'link_tags' not in st.session_state:
    st.session_state.link_tags = [{'tag': '', 'class_name': ''}]

def add_link_tag():
    st.session_state.link_tags.append({'tag': '', 'class_name': ''})

col3, col4 = st.columns([1, 5])
with col3:
    st.header('L Tags')
with col4:
    ""
    if st.button('Add another link tag'):
        add_link_tag()

for i, link_input in enumerate(st.session_state.link_tags):
    cols = st.columns(2)
    link_input['tag'] = cols[0].text_input(f'Enter link HTML tag {i+1}', value=link_input['tag'], key=f'link_tag_{i}')
    link_input['class_name'] = cols[1].text_input(f'Enter class name for link tag {i+1} (optional)', value=link_input['class_name'], key=f'link_class_{i}')

def find_content(soup, tag, class_name):
    if class_name:
        return soup.findAll(tag, attrs={"class": class_name})
    else:
        return soup.findAll(tag)

def generate_csv_download_link(data, filename):
    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False).encode()
    b64 = base64.b64encode(csv_data).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV file</a>'

def generate_zip_download_link(data, folder_name):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for item in data:
            link = item.get('link')
            if link:
                try:
                    img_data = requests.get(link).content
                    img_filename = f"{folder_name}/{item['id']}_image.jpg"
                    zip_file.writestr(img_filename, img_data)
                except Exception as e:
                    st.write(f"Could not download image {link}. Error: {e}")
    
    zip_buffer.seek(0)
    b64 = base64.b64encode(zip_buffer.read()).decode()
    return f'<a href="data:application/zip;base64,{b64}" download="{folder_name}.zip">Download ZIP file with images</a>'

if url:
    try:
        page_source = requests.get(url)
        soup = BeautifulSoup(page_source.text, 'html.parser')

        scraped_data = []

        for i, tag_input in enumerate(st.session_state.tags):
            tag = tag_input['tag']
            class_name = tag_input['class_name']
            if tag:
                content = find_content(soup, tag, class_name)
                if content:
                    for j, c in enumerate(content):
                        scraped_data.append({'id': j + 1, 'content': c.text})

        for i, link_input in enumerate(st.session_state.link_tags):
            tag = link_input['tag']
            class_name = link_input['class_name']
            if tag:
                links = find_content(soup, tag, class_name)
                if links:
                    for j, link in enumerate(links):
                        href = link.get('href')
                        src = link.get('src')
                        if href:
                            scraped_data.append({'id': j + 1, 'link': href})
                        elif src:
                            scraped_data.append({'id': j + 1, 'link': src})

        csv_filename = st.text_input('Enter CSV filename (with .csv extension):', 'scraped.csv')

        if st.button('Save to CSV'):
            csv_download_link = generate_csv_download_link(scraped_data, csv_filename)
            st.markdown(csv_download_link, unsafe_allow_html=True)

        image_folder = st.text_input('Enter folder name to save images:', 'images')

        if st.button('Download Images'):
            with st.spinner('Zipping files...'):
                zip_download_link = generate_zip_download_link(scraped_data, image_folder)
            st.markdown(zip_download_link, unsafe_allow_html=True)

        st.subheader("Scraped Content")
        for item in scraped_data:
            st.write(item)

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.write("Please enter a URL to start scraping.")
