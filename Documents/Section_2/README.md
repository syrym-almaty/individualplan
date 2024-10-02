# Pandas Pdfplumber Fitz

## **Algorithm Overview**

1. **Set Up the Environment**
   - Install necessary Python libraries: `pdfplumber`, `PyMuPDF` (`fitz`), and `pandas`.

2. **Define Column Headers**
   - Use the predefined list of 38 columns to structure the data.

3. **Extract Tables from PDF**
   - Use `pdfplumber` to accurately extract table data.
   - Handle multi-page PDFs and different table types.

4. **Clean and Transform Data**
   - Ensure each row corresponds to the 38 columns.
   - Handle merged cells and multi-line entries.
   - Remove irrelevant data at the end of the table.

5. **Convert Data to JSON**
   - Structure the data into a list of dictionaries matching the column headers.
   - Output the data in JSON format.

6. **Validate Data Integrity**
   - Implement checks to ensure data accuracy.
   - Handle any exceptions or anomalies.

---

## **Step-by-Step Implementation**

### **1. Set Up the Environment**

**Install Required Libraries:**

```bash
pip install pdfplumber pandas
```

**Note:** We can use `pdfplumber` for precise table extraction. If `pdfplumber` doesn't handle certain complexities, we can consider `PyMuPDF` (`fitz`), but `pdfplumber` should suffice for structured tables.

### **2. Define Column Headers**

```python
# List of 38 columns
columns = [
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
```

### **3. Extract Tables from PDF**

**Using `pdfplumber` to Extract Tables:**

```python
import pdfplumber
import pandas as pd

# Path to your PDF file
pdf_path = r'Жакыпбеков С.Ж. 2024-2025.pdf'

# Initialize an empty list to store data frames
df_list = []

with pdfplumber.open(pdf_path) as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
        # Extract tables from the page
        tables = page.extract_tables()
        
        # Process each table
        for table in tables:
            # Convert table to DataFrame
            df = pd.DataFrame(table)
            df_list.append(df)
```

**Note:** `pdfplumber` automatically detects tables on each page. However, we need to ensure that the extracted tables correspond to the desired data.

### **4. Clean and Transform Data**

**4.1. Combine DataFrames:**

```python
# Combine all DataFrames
combined_df = pd.concat(df_list, ignore_index=True)
```

**4.2. Assign Column Headers:**

First, we need to find the header row within the extracted data.

```python
# Find the header row index
header_row_index = None
for i, row in combined_df.iterrows():
    if set(row.values) & set(columns):
        header_row_index = i
        break

if header_row_index is not None:
    # Set the column headers
    combined_df.columns = combined_df.iloc[header_row_index]
    # Drop rows up to the header row
    combined_df = combined_df.iloc[header_row_index+1:].reset_index(drop=True)
else:
    print("Header row not found.")
```

**4.3. Clean Up the DataFrame:**

```python
# Keep only the columns we need
combined_df = combined_df[columns]

# Reset index
combined_df.reset_index(drop=True, inplace=True)

# Drop rows with all NaN values
combined_df.dropna(how='all', inplace=True)

# Remove rows that are not data entries (e.g., footnotes or summaries)
def is_valid_row(row):
    # Check if the first column is a number (№)
    try:
        int(row["№"])
        return True
    except (ValueError, TypeError):
        return False

combined_df = combined_df[combined_df.apply(is_valid_row, axis=1)]
```

**4.4. Handle Merged Cells and Multi-line Entries:**

If some cells are merged or span multiple lines, you may need to adjust the extraction method.

**Example:**

```python
# Fill NaN values in '№' column forward (in case of merged cells)
combined_df["№"].fillna(method='ffill', inplace=True)
```

**4.5. Ensure Each Row Has 38 Columns:**

```python
# Verify that each row has all columns
for idx, row in combined_df.iterrows():
    if len(row) != len(columns):
        print(f"Row {idx} does not have the correct number of columns.")
```

If rows are missing columns or have extra columns, you may need to adjust the parsing logic for those specific rows.

### **5. Convert Data to JSON**

**5.1. Convert DataFrame to JSON:**

```python
# Convert DataFrame to a list of dictionaries
data_records = combined_df.to_dict(orient='records')

# Output data to JSON
import json

json_output_path = r'structured_data.json'

with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json.dump(data_records, json_file, ensure_ascii=False, indent=4)

print(f"Data successfully exported to {json_output_path}")
```

### **6. Validate Data Integrity**

**6.1. Check for Missing Values:**

```python
# Identify rows with missing values
missing_data = combined_df.isnull().sum()

print("Missing data per column:")
print(missing_data)
```

**6.2. Handle Missing Data:**

You can choose to fill missing values, drop incomplete rows, or flag them for manual review.

**Example:**

```python
# Drop rows with missing critical information
critical_columns = ["№", "Дисциплина", "ФИО ППС"]
combined_df.dropna(subset=critical_columns, inplace=True)
```

**6.3. Verify Data Types:**

Ensure numerical columns contain numbers.

```python
numerical_columns = [
    "№",
    "Количество кредитов",
    "Курс обучения",
    "Количество обучающихся",
    # Add other numerical columns as needed
]

for col in numerical_columns:
    combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
```

**6.4. Final Data Verification:**

```python
# Check if any numerical columns contain NaN after conversion
for col in numerical_columns:
    if combined_df[col].isnull().any():
        print(f"Column {col} contains non-numeric data.")

# Ensure all rows have 38 columns
assert all(len(row) == 38 for _, row in combined_df.iterrows()), "Not all rows have 38 columns."
```

---

## **Handling Irrelevant Data**

Since the irrelevant data appears at the end of the table, we can implement a termination condition.

**Identify End of Table:**

- **Pattern Detection**: If the data stops matching the expected format, we can assume the table has ended.

**Implementation:**

```python
def is_table_row(row):
    # Check if '№' is a valid number and 'Дисциплина' is not empty
    try:
        int(row["№"])
        return True
    except (ValueError, TypeError):
        return False

# Filter out non-table rows
combined_df = combined_df[combined_df.apply(is_table_row, axis=1)]
```

---

## **Potential Challenges and Solutions**

### **1. Row Alignment Issues**

**Problem:** Some rows may not align correctly due to merged cells or multi-line text.

**Solution:**

- **Adjust Cell Merging Logic**: Use forward-fill or backward-fill methods to handle merged cells.
- **Multi-line Handling**: If a cell spans multiple lines, ensure that the extraction captures the entire content.

**Example:**

```python
# Combine multi-line entries in 'Дисциплина'
combined_df["Дисциплина"] = combined_df["Дисциплина"].str.replace('\n', ' ')
```

### **2. Inconsistent Table Structures**

If the tables in the PDF vary slightly but share the same columns, you may need to adjust the extraction per table.

**Solution:**

- **Process Each Table Individually**: Extract and clean each table separately before combining them.
- **Custom Parsing Logic**: For tables that don't conform, write custom logic to map their data correctly.

### **3. Irrelevant Data Within Table**

Sometimes, irrelevant rows might appear within the table.

**Solution:**

- **Row Validation**: Implement validation checks for each row to ensure it contains valid data.
- **Exclude Rows Based on Criteria**: If a row lacks essential data or doesn't match expected patterns, exclude it.

---

## **Alternative Approach: Using Coordinates in `pdfplumber`**

If the tables are always in the same position on the page, you can specify the exact area to extract.

**Example:**

```python
# Define the coordinates of the table area (x0, y0, x1, y1)
table_area = (50, 100, 550, 750)  # Adjust these values based on your PDF

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table(
            table_settings={
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "snap_tolerance": 3,
                "explicit_vertical_lines": [],
                "explicit_horizontal_lines": [],
                "intersection_tolerance": 5,
                "join_tolerance": 3,
                "edge_min_length": 3,
            },
            bbox=table_area
        )
        # Process the table as before
```

---

## **Final Thoughts**

While it's challenging to guarantee 100% accuracy due to the inherent variability in PDF formatting, following the steps above should provide a robust algorithm capable of accurately extracting and structuring your data into JSON.

**Recommendations:**

- **Test on Multiple PDFs**: Validate the algorithm with different PDFs to ensure it handles various cases.
- **Adjust Parameters**: Fine-tune the `pdfplumber` settings (like `snap_tolerance`, `join_tolerance`) to better suit your PDFs.
- **Manual Review**: For critical data, consider implementing a manual review step for rows that don't meet validation criteria.

**If you encounter specific issues or need further assistance with refining the algorithm, feel free to ask!**

---

## **Additional Resources**

- **`pdfplumber` Documentation**: [https://pdfplumber.readthedocs.io/](https://pdfplumber.readthedocs.io/)
- **`pandas` Documentation**: [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)

---

Certainly! Below is a complete Python script that automates the extraction of structured data from a PDF and converts it into a well-organized JSON format based on your predefined 38 columns. This script uses the `pdfplumber` library for PDF parsing and `pandas` for data manipulation.

### **Complete Python Script: PDF to Structured JSON Extraction**

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
PDF_FILE_PATH = r'Жакыпбеков С.Ж. 2024-2025.pdf'

# Path to save the structured JSON output
JSON_OUTPUT_PATH = r'structured_data.json'

# Path to save problematic rows for manual review
PROBLEMATIC_ROWS_PATH = r'problematic_rows.json'

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

def find_header_row(combined_df, headers):
    """
    Identifies the header row in the combined DataFrame.
    Returns the index of the header row or None if not found.
    """
    for i, row in combined_df.iterrows():
        # Compare the row with the predefined headers
        row_values = [str(item).strip() for item in row.values]
        match_count = sum([1 for header in headers if header in row_values])
        if match_count >= len(headers) * 0.5:  # At least 50% headers match
            return i
    return None

def clean_and_structurize_data(combined_df, headers):
    """
    Cleans the combined DataFrame and structures it according to the predefined headers.
    Returns a cleaned DataFrame and a list of problematic rows.
    """
    # Identify the header row
    header_row_index = find_header_row(combined_df, headers)
    if header_row_index is not None:
        # Assign column headers
        combined_df.columns = combined_df.iloc[header_row_index]
        # Drop rows up to and including the header row
        combined_df = combined_df.iloc[header_row_index + 1:].reset_index(drop=True)
        print(f"Header row found at index {header_row_index}.")
    else:
        print("Header row not found. Proceeding without reassigning column headers.")
    
    # Keep only the predefined columns
    combined_df = combined_df[headers]
    
    # Drop rows with all NaN values
    combined_df.dropna(how='all', inplace=True)
    
    # Function to validate if a row is a valid data entry
    def is_valid_row(row):
        # Check if the first column '№' is a valid integer
        try:
            int(row["№"])
            return True
        except (ValueError, TypeError):
            return False
    
    # Filter out invalid rows
    valid_df = combined_df[combined_df.apply(is_valid_row, axis=1)].reset_index(drop=True)
    
    # Identify problematic rows
    problematic_df = combined_df[~combined_df.apply(is_valid_row, axis=1)].reset_index(drop=True)
    
    return valid_df, problematic_df

def convert_df_to_json(df):
    """
    Converts the DataFrame to a list of dictionaries suitable for JSON output.
    """
    return df.to_dict(orient='records')

def save_json(data, output_path):
    """
    Saves the given data to a JSON file at the specified path.
    """
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"JSON data successfully saved to {output_path}.")

def save_problematic_rows(problematic_df, output_path):
    """
    Saves the problematic rows to a JSON file for manual review.
    """
    if problematic_df.empty:
        print("No problematic rows to save.")
        return
    problematic_data = problematic_df.to_dict(orient='records')
    with open(output_path, 'w', encoding='utf-8') as json_file:
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
    print(f"Combined DataFrame created with {combined_df.shape[0]} rows and {combined_df.shape[1]} columns.")
    
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

### **Explanation of the Script**

1. **Configuration Parameters:**
   - **`PDF_FILE_PATH`**: Update this variable with the path to your PDF file.
   - **`JSON_OUTPUT_PATH`**: Path where the structured JSON will be saved.
   - **`PROBLEMATIC_ROWS_PATH`**: Path to save any rows that couldn't be parsed correctly for manual review.
   - **`COLUMN_HEADERS`**: A list of your 38 predefined column names in the exact order they appear in the PDF.

2. **Function Definitions:**
   - **`extract_tables_from_pdf`**: Uses `pdfplumber` to extract all tables from each page of the PDF and stores them as pandas DataFrames.
   - **`find_header_row`**: Identifies the header row within the combined DataFrame by matching it against the predefined headers.
   - **`clean_and_structurize_data`**: Cleans the combined DataFrame by:
     - Assigning the correct headers.
     - Dropping irrelevant rows.
     - Separating valid data rows from problematic ones.
   - **`convert_df_to_json`**: Converts the cleaned DataFrame into a list of dictionaries suitable for JSON serialization.
   - **`save_json`**: Saves the JSON data to the specified output path.
   - **`save_problematic_rows`**: Saves any rows that couldn't be parsed correctly for manual inspection.
   - **`main`**: Orchestrates the entire extraction and conversion process.

3. **Execution:**
   - The script checks if the specified PDF file exists.
   - Extracts all tables from the PDF.
   - Combines the tables into a single DataFrame.
   - Cleans and structures the data according to the predefined columns.
   - Converts the structured data into JSON format.
   - Saves the JSON data and any problematic rows to their respective files.

### **How to Use the Script**

1. **Install Required Libraries:**

   Ensure you have the necessary Python libraries installed. You can install them using `pip`:

   ```bash
   pip install pdfplumber pandas
   ```

2. **Update Configuration Parameters:**

   - Replace the `PDF_FILE_PATH` with the actual path to your PDF file.
   - Optionally, adjust the `JSON_OUTPUT_PATH` and `PROBLEMATIC_ROWS_PATH` as needed.

3. **Run the Script:**

   Save the script to a `.py` file, for example, `pdf_to_json_extractor.py`, and run it using Python:

   ```bash
   python pdf_to_json_extractor.py
   ```

4. **Review the Output:**

   - **Structured JSON**: The extracted and structured data will be saved to the path specified in `JSON_OUTPUT_PATH`.
   - **Problematic Rows**: Any rows that couldn't be parsed correctly will be saved to `PROBLEMATIC_ROWS_PATH` for your manual review and correction.

### **Handling Potential Issues**

- **Header Row Detection:**
  
  The script attempts to find the header row by matching at least 50% of the predefined headers with the extracted data. If your headers are not being detected correctly, you may need to adjust the `find_header_row` function or ensure that the PDF tables are consistently formatted.

- **Problematic Rows:**
  
  Rows that do not start with a valid number (`№`) are considered problematic and are saved separately. You should manually review these rows to identify any patterns or issues that can be addressed by refining the parsing logic.

- **Merged Cells and Multi-line Entries:**
  
  If some cells contain merged data or span multiple lines, additional preprocessing might be necessary. You can modify the `clean_and_structurize_data` function to handle such cases, possibly by using more sophisticated text processing or regex patterns.

- **Irrelevant Data at the End of Tables:**
  
  The script filters out any data that does not conform to the expected row format based on the predefined columns. Ensure that your irrelevant data does not inadvertently match the valid row patterns.

### **Advanced Enhancements**

For even more robust extraction, consider the following enhancements:

- **Using Coordinates for Table Extraction:**
  
  If your tables are always located in the same position within the PDF pages, you can specify the bounding box coordinates to extract tables more accurately.

  ```python
  table_area = (x0, y0, x1, y1)  # Replace with actual coordinates
  table = page.extract_table(bbox=table_area)
  ```

- **Regular Expressions for Enhanced Row Validation:**
  
  Implement more advanced regex patterns to validate and parse rows, especially if certain columns contain complex or variable data formats.

- **Logging and Error Handling:**
  
  Incorporate logging mechanisms to track the script's progress and capture any errors or anomalies during the extraction process.

  ```python
  import logging

  # Configure logging
  logging.basicConfig(
      filename='pdf_extraction.log',
      level=logging.INFO,
      format='%(asctime)s:%(levelname)s:%(message)s'
  )

  # Example usage within functions
  logging.info("Starting PDF table extraction.")
  logging.error("Error message here.")
  ```

- **Interactive Manual Correction:**
  
  Develop an interface or use existing tools to manually correct problematic rows and re-import them into the JSON structure.

### **Final Remarks**

This script provides a foundational approach to extracting structured data from PDFs into JSON. Depending on the complexity and variability of your PDF tables, you might need to further customize and refine the extraction logic. Always validate the extracted data to ensure its accuracy and completeness.
