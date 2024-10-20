from bs4 import BeautifulSoup
from docx import Document
import os
from tqdm import tqdm
import re

# Function to extract text from an HTML file
def html_to_text(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        return soup.get_text()

# Function to clean text
def clean_text(text):
    # Remove NULL bytes and control characters
    return re.sub(r'[\x00-\x1F\x7F]', '', text)

# Create a new Word document
doc = Document()

# Specify the folder containing HTML files
html_folder = r"C:\Users\Bao Viet\Downloads\Compressed\demuc"

# Get the list of HTML files in the folder
html_files = [f for f in os.listdir(html_folder) if f.endswith(".html")]

# Iterate through all HTML files in the folder with a progress bar
for filename in tqdm(html_files, desc="Processing HTML files"):
    html_file_path = os.path.join(html_folder, filename)
    # Extract text from each HTML file
    text = html_to_text(html_file_path)
    # Clean the extracted text
    cleaned_text = clean_text(text)
    # Add the cleaned text to the Word document
    doc.add_paragraph(cleaned_text)
    doc.add_page_break()  # Add a page break after each file's content

# Save the final merged .docx file
doc.save("merged_document.docx")

print("HTML files have been merged into a single .docx file.")