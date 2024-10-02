# Individual Plan Automatization

## Step 1: Install required libraries

You may need to install the required libraries using pip:

```bash
pip install PyPDF2 pdfplumber json
```

## Step 2: Code to extract PDF content and convert it to JSON

```python
import json
import pdfplumber

# Specify the path to your PDF file
pdf_file_path = r"C:\Users\syrym\Downloads\Жакыпбеков С.Ж. 2024-2025.pdf"

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
output_json_path = r"C:\Users\syrym\Downloads\extracted_pdf_data.json"
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_output)

# Print the JSON output
print(json_output)
```

## Explanation

1. **Libraries used**: `pdfplumber` is used to extract text from the PDF pages.
2. **Extracting text**: The code loops through each page of the PDF, extracts the text, and stores it along with the page number.
3. **JSON conversion**: The extracted data is formatted into a JSON structure where each page is an object with a `page_number` and `content`.
4. **Output**: The resulting JSON is saved into a file called `extracted_pdf_data.json`.

### Step-by-Step Guide

#### Step 1: Install `virtualenv` (if not already installed)

You can use `venv` (which is included in Python 3.3 and later) or `virtualenv` (which is more flexible for different Python versions). Here's how to install `virtualenv`:

```bash
pip install virtualenv
```

#### Step 2: Create a virtual environment

Navigate to your project directory and create a virtual environment. Replace `myenv` with the name of your environment:

```bash
cd C:\Users\syrym\Downloads\your_project_folder
virtualenv myenv
```

Alternatively, if you prefer using `venv`, use this command:

```bash
python -m venv myenv
```

#### Step 3: Activate the virtual environment

To activate the environment:

- **Windows**:

```bash
myenv\Scripts\activate
```

- **Ubuntu/Linux/macOS**:

```bash
source myenv/bin/activate
```

After activation, your command line will show the name of the virtual environment, indicating that it’s active.

#### Step 4: Create a `requirements.txt` file

In your project directory, create a `requirements.txt` file that lists the packages your project depends on. You can either write the dependencies manually or automatically generate it from the installed packages in your environment.

Here’s how to generate `requirements.txt` automatically:

1. Install the necessary packages for your project:

   ```bash
   pip install pdfplumber
   pip install PyPDF2
   ```

2. Export the list of installed packages to a `requirements.txt` file:

   ```bash
   pip freeze > requirements.txt
   ```

This will create a `requirements.txt` file that might look like this:

```bash
pdfplumber==0.5.28
PyPDF2==3.0.0
```

#### Step 5: Install packages from `requirements.txt`

If you or someone else needs to recreate the environment later, simply run the following command to install all dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### Step 6: Deactivate the environment

Once you're done working, you can deactivate the virtual environment by running:

```bash
deactivate
```

### Full Example Directory Structure

```bash
your_project_folder/
│
├── myenv/               # Virtual environment directory
├── requirements.txt     # File listing dependencies
└── main.py              # Your Python script(s)
```

### Summary

1. **Create a virtual environment**: `virtualenv myenv`
2. **Activate it**: `myenv\Scripts\activate` (Windows) or `source myenv/bin/activate` (Linux/macOS)
3. **Install dependencies**: `pip install <package>`
4. **Export dependencies**: `pip freeze > requirements.txt`
5. **Install from `requirements.txt`**: `pip install -r requirements.txt`
6. **Deactivate the environment**: `deactivate`

---

### Step-by-Step Instructions

1. **Make sure you're in your project directory**:

   You've already navigated to `~/Downloads/individualplan`, so you can skip this step. If not, navigate using:

   ```bash
   cd ~/Downloads/individualplan
   ```

2. **Create the virtual environment** (if you haven't already):

   ```bash
   python -m venv individualplan
   ```

3. **Activate the virtual environment in Git Bash**:

   Use forward slashes (`/`) instead of backslashes (`\`):

   ```bash
   source individualplan/Scripts/activate
   ```

4. **Verify Activation**:

   You should now see the virtual environment `(individualplan)` at the beginning of your prompt.

5. **Deactivate when done**:

   To deactivate the virtual environment, simply run:

   ```bash
   deactivate
   ```
