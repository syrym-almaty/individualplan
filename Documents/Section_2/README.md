# Pdfplumber Pandas

---

## **1. Enhanced Python Script: PDF to Structured JSON Extraction**

This script is designed to be more robust, handling cases where headers might not be detected automatically and ensuring that data aligns correctly with your predefined 38 columns.

### **Complete Python Script**

```python
import pdfplumber
import pandas as pd
import json
import re
import os

# =======================
# Configuration Parameters
# =======================

# Path to your PDF file
PDF_FILE_PATH = r'C:\Users\syrym\Downloads\individualplan\Documents\Section_2\Жакыпбеков С.Ж. 2024-2025.pdf'

# Path to save the structured JSON output
JSON_OUTPUT_PATH = r'C:\Users\syrym\Downloads\individualplan\structured_data.json'

# Path to save problematic rows for manual review
PROBLEMATIC_ROWS_PATH = r'C:\Users\syrym\Downloads\individualplan\problematic_rows.json'

# Define the list of 38 columns in the exact order
COLUMN_HEADERS = [
    "№",
    "Дисциплина",
    "Форма обучения",
    "Шифр специальности",
    "Специализация/Образовательная программа",
    "Группы",
    "Количество кредитов",
    "Компонент дисциплины",
    "Язык обучения",
    "Курс обучения",
    "Академический период",
    "Количество обучающихся",
    "Количество потоков (лекции/СРСП)",
    "Количество потоков (практические/лабораторные)",
    "Лекционных занятий",
    "Практических, семинарских занятий",
    "Лабораторных занятий",
    "СРСП",
    "Рубежный контроль",
    "Консультации",
    "Экзаменов",
    "Всего учебных часов к расчету штатов 1 семестр",
    "Всего учебных часов к расчету штатов 2 семестр",
    "Всего учебных часов к расчету",
    "Курсера (часы)",
    "Признак Курсера",
    "ФИО ППС",
    "Должность",
    "Форма оплаты",
    "Кол-во штатных часов или почасовых",
    "Шт. ед. по штату ИЛИ почасовой",
    "Штатная нагрузка",
    "Почасовая нагрузка",
    "Шт. ед. по штату",
    "Шт. ед. по почасовой",
    "Шт. ед. почасовой на 2-ой семестр",
    "Почасовая нагрузка Семестр 2",
    "Шт. ед. по почасовой по дис Семестр 2"
]

# ==========================
# Function Definitions
# ==========================

import pdfplumber
import pandas as pd
import json
import re
import os

# =======================
# Configuration Parameters
# =======================

# Path to your PDF file
PDF_FILE_PATH = r"Жакыпбеков С.Ж. 2024-2025.pdf"

# Path to save the structured JSON output
JSON_OUTPUT_PATH = r"structured_data.json"

# Path to save problematic rows for manual review
PROBLEMATIC_ROWS_PATH = r"problematic_rows.json"

# Define the list of 38 columns in the exact order
COLUMN_HEADERS = [
    "№",
    "Дисциплина",
    "Форма обучения",
    "Шифр специальности",
    "Специализация/Образовательная программа",
    "Группы",
    "Количество кредитов",
    "Компонент дисциплины",
    "Язык обучения",
    "Курс обучения",
    "Академический период",
    "Количество обучающихся",
    "Количество потоков (лекции/СРСП)",
    "Количество потоков (практические/лабораторные)",
    "Лекционных занятий",
    "Практических, семинарских занятий",
    "Лабораторных занятий",
    "СРСП",
    "Рубежный контроль",
    "Консультации",
    "Экзаменов",
    "Всего учебных часов к расчету штатов 1 семестр",
    "Всего учебных часов к расчету штатов 2 семестр",
    "Всего учебных часов к расчету",
    "Курсера (часы)",
    "Признак Курсера",
    "ФИО ППС",
    "Должность",
    "Форма оплаты",
    "Кол-во штатных часов или почасовых",
    "Шт. ед. по штату ИЛИ почасовой",
    "Штатная нагрузка",
    "Почасовая нагрузка",
    "Шт. ед. по штату",
    "Шт. ед. по почасовой",
    "Шт. ед. почасовой на 2-ой семестр",
    "Почасовая нагрузка Семестр 2",
    "Шт. ед. по почасовой по дис Семестр 2",
]

# ==========================
# Function Definitions
# ==========================


def extract_tables_from_pdf(pdf_path):
    """
    Extracts all tables from the given PDF and returns a list of DataFrames.
    """
    df_list = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            # Extract tables from the current page
            tables = page.extract_tables()
            if not tables:
                print(f"No tables found on page {page_number}.")
                continue
            for table_number, table in enumerate(tables, start=1):
                # Convert the table to a DataFrame
                df = pd.DataFrame(table)
                df_list.append(df)
                print(f"Extracted table {table_number} from page {page_number}.")
    return df_list


def assign_headers(combined_df, headers):
    """
    Assign predefined headers to the DataFrame.
    Assumes that the DataFrame has the correct number of columns.
    """
    if combined_df.shape[1] < len(headers):
        # Add missing columns with empty strings
        for _ in range(len(headers) - combined_df.shape[1]):
            combined_df[len(combined_df.columns)] = ""
    elif combined_df.shape[1] > len(headers):
        # Trim extra columns
        combined_df = combined_df.iloc[:, : len(headers)]

    # Assign headers to the DataFrame
    combined_df.columns = headers
    return combined_df


def clean_and_structurize_data(combined_df, headers):
    """
    Cleans the combined DataFrame and structures it according to the predefined headers.
    Returns a cleaned DataFrame and a list of problematic rows.
    """
    # Assign predefined headers
    combined_df = assign_headers(combined_df, headers)

    # Drop rows with all NaN or empty strings
    combined_df.replace("", pd.NA, inplace=True)
    combined_df.dropna(how="all", inplace=True)

    # Function to validate if a row is a valid data entry
    def is_valid_row(row):
        # Check if the first column '№' is a valid integer
        try:
            int(str(row["№"]).strip())
            return True
        except (ValueError, TypeError):
            return False

    # Filter out invalid rows
    valid_df = combined_df[combined_df.apply(is_valid_row, axis=1)].reset_index(
        drop=True
    )

    # Identify problematic rows
    problematic_df = combined_df[~combined_df.apply(is_valid_row, axis=1)].reset_index(
        drop=True
    )

    return valid_df, problematic_df


def convert_df_to_json(df):
    """
    Converts the DataFrame to a list of dictionaries suitable for JSON output.
    """
    return df.to_dict(orient="records")


def save_json(data, output_path):
    """
    Saves the given data to a JSON file at the specified path.
    """
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"JSON data successfully saved to {output_path}.")


def save_problematic_rows(problematic_df, output_path):
    """
    Saves the problematic rows to a JSON file for manual review.
    """
    if problematic_df.empty:
        print("No problematic rows to save.")
        return
    problematic_data = problematic_df.to_dict(orient="records")
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(problematic_data, json_file, ensure_ascii=False, indent=4)
    print(f"Problematic rows saved to {output_path}.")


def main():
    """
    Main function to orchestrate the PDF extraction and JSON conversion.
    """
    # Check if the PDF file exists
    if not os.path.exists(PDF_FILE_PATH):
        print(f"Error: PDF file not found at {PDF_FILE_PATH}.")
        return

    print("Starting PDF table extraction...")

    # Step 1: Extract tables from PDF
    tables = extract_tables_from_pdf(PDF_FILE_PATH)
    if not tables:
        print("No tables extracted from the PDF.")
        return

    # Step 2: Combine all extracted tables into a single DataFrame
    combined_df = pd.concat(tables, ignore_index=True)
    print(
        f"Combined DataFrame created with {combined_df.shape[0]} rows and {combined_df.shape[1]} columns."
    )

    # Step 3: Clean and structure the data
    valid_df, problematic_df = clean_and_structurize_data(combined_df, COLUMN_HEADERS)
    print(f"Valid data rows: {valid_df.shape[0]}")
    print(f"Problematic rows: {problematic_df.shape[0]}")

    # Step 4: Convert the valid DataFrame to JSON
    json_data = convert_df_to_json(valid_df)

    # Step 5: Save the JSON data to a file
    save_json(json_data, JSON_OUTPUT_PATH)

    # Step 6: Save problematic rows for manual review
    save_problematic_rows(problematic_df, PROBLEMATIC_ROWS_PATH)

    print("PDF to JSON extraction completed successfully.")


# ==========================
# Execute the Script
# ==========================

if __name__ == "__main__":
    main()

```

### **Explanation of Enhancements**

1. **Header Assignment Without Detection**:
    - **Issue**: The previous script attempted to detect the header row automatically, which failed in your case.
    - **Solution**: Directly assign the predefined `COLUMN_HEADERS` to the DataFrame, ensuring that the number of columns matches. If there are fewer columns, additional columns are added with empty strings; if there are more, extra columns are trimmed.

2. **Handling Inconsistent Row Structures**:
    - **Issue**: Merged cells or inconsistent row structures can lead to mismatched columns.
    - **Solution**: The script now ensures that each row has exactly 38 columns by adjusting the DataFrame accordingly. Rows that do not start with a valid number in the first column (`№`) are flagged as problematic.

3. **Improved Data Cleaning**:
    - Replaces empty strings with `NaN` and drops rows that are entirely empty.
    - Strips whitespace from data entries to prevent mismatches.

4. **Enhanced Error Handling and Logging**:
    - Provides clear console messages about the extraction process and any issues encountered.
    - Saves problematic rows separately for manual inspection.

### **How to Use the Enhanced Script**

1. **Install Required Libraries**:

    Ensure you have the necessary Python libraries installed. Open your terminal or command prompt and run:

    ```bash
    pip install pdfplumber pandas
    ```

2. **Prepare the Script**:

    - Save the provided Python script to a file named, for example, `pdf_to_json_extractor.py`.
    - Ensure that the `PDF_FILE_PATH`, `JSON_OUTPUT_PATH`, and `PROBLEMATIC_ROWS_PATH` variables are correctly set to your desired file paths.

3. **Run the Script**:

    Navigate to the directory containing the script and execute:

    ```bash
    python pdf_to_json_extractor.py
    ```

4. **Review the Outputs**:

    - **Structured JSON**: Located at the path specified in `JSON_OUTPUT_PATH`.
    - **Problematic Rows**: Located at the path specified in `PROBLEMATIC_ROWS_PATH`. Review these rows to identify patterns or specific issues that can be addressed manually or by refining the script further.

### **Sample `requirements.txt`**

To ensure reproducibility and manage dependencies, create a `requirements.txt` file with the following content:

```bash
pdfplumber==0.7.4
pandas==2.1.1
```

**How to Use:**

1. **Save the above content** into a file named `requirements.txt`.
2. **Install the dependencies** by running:

    ```bash
    pip install -r requirements.txt
    ```

---

## **2. Methodologies and Best Practices for Handling Unstructured PDFs**

Working with unstructured PDFs requires a strategic approach to ensure accurate data extraction. Here are some methodologies and best practices:

### **A. Understanding the PDF Structure**

1. **Consistent Column Structure**:
    - **Benefit**: Knowing that the columns are fixed allows you to map data accurately even if rows vary in length.
    - **Action**: Utilize this consistency to align data based on order rather than relying solely on content matching.

2. **Variable Number of Rows**:
    - **Benefit**: Allows flexibility in data processing.
    - **Action**: Implement dynamic handling in your script to accommodate varying numbers of rows.

3. **Irrelevant Data at the End**:
    - **Benefit**: Knowing the pattern helps in ignoring noise.
    - **Action**: Implement termination conditions or filters to exclude irrelevant data after the main table.

### **B. PDF Parsing Techniques**

1. **Using `pdfplumber`**:
    - **Advantages**:
        - Precise control over table extraction.
        - Ability to specify areas for table detection.
    - **Best Practices**:
        - Experiment with different extraction strategies (`lines`, `words`, `auto`) to find what works best for your PDF.
        - Use bounding boxes (`bbox`) if tables are consistently placed on each page.

2. **Alternative Libraries**:
    - **Camelot**:
        - **Pros**: Good for PDFs with clearly defined table borders.
        - **Cons**: May struggle with complex or borderless tables.
    - **Tabula-py**:
        - **Pros**: Java-based, often effective with various table structures.
        - **Cons**: Requires Java runtime, which might complicate deployment.
    - **PyMuPDF (fitz)**:
        - **Pros**: High flexibility in text extraction.
        - **Cons**: Requires more manual processing to detect table structures.

3. **Modern Tools and AI-Based Solutions**:
    - **Deep Learning Models**:
        - Models like **LayoutLM** can understand the layout and content of documents.
    - **Commercial Tools**:
        - **Adobe Acrobat Pro**: Offers advanced table extraction features.
        - **Docparser**, **Rossum**, **ABBYY FineReader**: Provide AI-powered PDF parsing.

### **C. Data Cleaning and Transformation**

1. **Predefine Columns**:
    - **Action**: Use the known column order to map data accurately, reducing reliance on content-based matching.

2. **Row Detection and Cleanup**:
    - **Action**: Implement validation checks to ensure each row has the correct number of columns. Flag or correct rows that don't.

3. **Handling Noise and Irrelevant Data**:
    - **Action**: Use pattern recognition (e.g., rows not starting with a number) to identify and exclude irrelevant data.

### **D. Handling Complexities**

1. **Row Alignment Issues**:
    - **Solution**: Use heuristics to detect merged or split rows. For instance, check if the number of elements exceeds the expected columns and adjust accordingly.

2. **Multi-line Cells**:
    - **Solution**: Detect when a cell spans multiple lines and merge them before splitting into columns.

3. **Consistent Formatting**:
    - **Solution**: If possible, standardize the PDF formatting before extraction. This might involve using PDF editing tools to ensure tables are uniformly structured.

### **E. Validation and Verification**

1. **Automated Checks**:
    - **Action**: Implement checks in your script to verify data types, required fields, and overall data integrity.

2. **Manual Review**:
    - **Action**: Save problematic rows for manual inspection to identify patterns or specific issues that require adjustments in the script.

3. **Iterative Refinement**:
    - **Action**: Continuously refine your extraction logic based on the insights gained from manual reviews.

---

## **3. Recommendations for Modern Tools and Techniques**

To enhance the accuracy and efficiency of your data extraction process, consider the following modern tools and techniques:

### **A. Advanced PDF Parsing Libraries**

1. **Camelot**:
    - **Usage**:

        ```python
        import camelot

        pdf_path = r'C:\path\to\your\file.pdf'
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')  # or 'lattice'

        # Combine all tables into one DataFrame
        combined_df = pd.concat([table.df for table in tables], ignore_index=True)
        ```

    - **Pros**: Effective with well-defined tables.
    - **Cons**: May require tuning `flavor` and other parameters for optimal results.

2. **Tabula-py**:
    - **Usage**:

        ```python
        import tabula

        pdf_path = r'C:\path\to\your\file.pdf'
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

        # Combine all tables into one DataFrame
        combined_df = pd.concat(tables, ignore_index=True)
        ```

    - **Pros**: Robust table extraction capabilities.
    - **Cons**: Requires Java runtime.

### **B. AI-Powered PDF Parsing Tools**

1. **LayoutLM**:
    - **Description**: A deep learning model by Microsoft for understanding document layouts.
    - **Usage**: Requires knowledge of NLP and deep learning frameworks like PyTorch or TensorFlow.

2. **Commercial Solutions**:
    - **Docparser**, **Rossum**, **ABBYY FineReader**:
        - **Pros**: High accuracy with minimal setup.
        - **Cons**: May involve subscription costs.

### **C. Preprocessing PDFs**

1. **Standardize Table Formats**:
    - Use PDF editing tools to ensure that tables have consistent structures across all pages.

2. **Remove Irrelevant Data**:
    - Manually or programmatically remove sections of the PDF that contain irrelevant data to minimize extraction errors.

### **D. Hybrid Approach: Combining Multiple Tools**

Sometimes, using multiple tools in combination can yield better results. For example:

1. **Extract Tables with Camelot or Tabula-py**.
2. **Post-process the extracted data with `pdfplumber` or Pandas** to handle any remaining inconsistencies.

### **E. Utilizing Regular Expressions (Regex) for Enhanced Parsing**

Implement regex patterns to accurately split and validate data within cells, especially if cells contain delimiters or complex text.

**Example:**

```python
import re

def split_row(row_text, expected_columns):
    """
    Splits a row of text into columns based on predefined patterns.
    """
    # Example pattern: split by two or more spaces
    parts = re.split(r'\s{2,}', row_text)
    
    if len(parts) == expected_columns:
        return parts
    else:
        # Implement additional logic to handle discrepancies
        # For instance, merge certain parts or flag the row
        return None
```

---

## **4. Quick Solutions and Workflow Optimization**

To expedite the extraction process and ensure accuracy, follow this optimized workflow:

### **Step 1: Preprocess the PDF**

- **Ensure Consistent Table Structure**: If possible, edit the PDF to ensure that all tables have consistent formatting and no merged cells.
- **Remove Irrelevant Sections**: Use PDF editing tools to remove non-essential data that could interfere with table extraction.

### **Step 2: Choose the Right Tool**

- **Start with `pdfplumber`**: It's versatile and offers precise control.
- **If Issues Persist, Try Camelot or Tabula-py**: Depending on your PDF's table structure, these tools might handle extraction better.

### **Step 3: Implement Robust Error Handling in Your Script**

- **Validate Row Lengths**: Ensure each extracted row has the expected number of columns.
- **Log and Save Problematic Rows**: For manual correction and iterative improvement.

### **Step 4: Post-process Extracted Data**

- **Clean Data**: Remove unwanted characters, handle missing values, and ensure data types are correct.
- **Map Data to JSON**: Convert the cleaned DataFrame into JSON format.

### **Step 5: Automate and Iterate**

- **Run the Script on Multiple PDFs**: Ensure that your script can handle different instances of the table structure.
- **Refine Based on Feedback**: Use the problematic rows to improve your extraction logic continuously.

---

## **5. Final Recommendations**

1. **Iterative Development**:
    - **Start Simple**: Begin with extracting data as-is and gradually handle complexities.
    - **Enhance Over Time**: Use feedback from problematic rows to refine your extraction logic.

2. **Leverage Community Resources**:
    - **GitHub Repositories**: Explore repositories related to PDF table extraction for additional scripts and ideas.
    - **Forums and Q&A Sites**: Platforms like Stack Overflow can be invaluable for troubleshooting specific issues.

3. **Consider Professional Tools for Critical Projects**:
    - If accuracy is paramount and resources allow, investing in professional PDF parsing tools can save time and ensure high-quality data extraction.

4. **Documentation and Logging**:
    - **Maintain Clear Logs**: Document each step of the extraction process and log any issues encountered.
    - **Keep Your Code Documented**: Clear comments and documentation will help in maintaining and updating your scripts.

---
