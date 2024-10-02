import json
import pdfplumber

# Specify the path to your PDF file
pdf_file_path = r"Жакыпбеков С.Ж. 2024-2025.pdf"

# Initialize a list to store extracted data
data = []

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            data.append({
                "page_number": page_num + 1,
                "content": page_text
            })

# Call the function to extract text
extract_text_from_pdf(pdf_file_path)

# Convert the extracted data into a JSON object
json_output = json.dumps(data, ensure_ascii=False, indent=4)

# Save the JSON output to a file
output_json_path = r"extracted_pdf_data.json"
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_output)

# Print the JSON output
print(json_output)