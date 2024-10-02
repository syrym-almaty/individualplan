# Pandas

## Overview of Steps

1. **Load the JSON Data**
2. **Extract and Clean the Content**
3. **Split the Content into Individual Rows**
4. **Parse Each Row into Columns**
5. **Create a Structured DataFrame**
6. **Export the Structured Data**

Let's go through each step in detail.

---

## Step 1: Setting Up Your Environment

### 1.1. Install Python

If you haven't already, download and install Python from [python.org](https://www.python.org/downloads/).

### 1.2. Create a Virtual Environment (Optional but Recommended)

Creating a virtual environment helps manage dependencies.

```bash
# Create a virtual environment named 'env'
python -m venv env

# Activate the virtual environment
# Windows:
env\Scripts\activate

# macOS/Linux:
source env/bin/activate
```

### 1.3. Install Required Libraries

Install the `pandas` library, which is essential for data manipulation.

```bash
pip install pandas
```

---

## Step 2: Loading and Understanding Your JSON Data

Assuming your JSON file (`extracted_pdf_data.json`) is structured as follows:

```json
[
    {
        "page_number": 1,
        "content": "Факультет \"Компьютерные технологии и кибербезопасность\"...\n..."
    }
]
```

The `content` field contains the raw text data extracted from the PDF, including headers and data rows.

---

## Step 3: Parsing the JSON and Structuring the Data

We'll use Python to parse the JSON, extract the content, split it into rows, and then map each row's data to the corresponding columns.

### 3.1. Define the Column Headers

First, define the list of columns in the exact order as they appear in your data.

```python
# Define the list of 38 columns
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
    "Прак тичес ких, семи нарск их занятий",
    "Лаборат орных занятий",
    "СРС П",
    "Рубежный контроль",
    "Консультации",
    "Экзаменов",
    "Всего учебных часов к расчету штатов 1 семестр",
    "Всего учебных часов к расчету штатов 2 семестр",
    "Всего учебных часов к расчету",
    "Курсера (часы)",
    "признак Курсера",
    "ФИО ППС",
    "Должность",
    "Форма оплаты",
    "Кол-во штатных часов или почасовых",
    "Шт ед по штату ИЛИ почасовой",
    "Штатная нагрузка",
    "Почасова я нагрузка",
    "Шт.ед. по штату",
    "Шт.ед. по почасовой",
    "Шт ед почасовой на 2-ой семестр",
    "Почасовая нагрузка Семестр 2",
    "Шт.ед. по почасовой по дис Семестр 2"
]
```

### 3.2. Load and Concatenate JSON Content

We'll load the JSON file and concatenate all `content` fields into a single string for processing.

```python
import json
import pandas as pd
import re

# Path to your JSON file
json_file_path = r'C:\Users\syrym\Downloads\individualplan\extracted_pdf_data.json'

# Load JSON data
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Concatenate content from all pages
full_content = ""
for page in data:
    full_content += page.get('content', '') + "\n"

# Optional: Initial cleaning
# Replace multiple spaces with a single space for easier parsing
full_content = re.sub(r'\s+', ' ', full_content)
```

### 3.3. Split the Content into Individual Rows

Assuming each row starts with a number (`№`), we'll use a regular expression to identify the start of each row.

```python
# Regex pattern to identify rows starting with a number followed by a space
pattern = re.compile(r'(\d+)\s')

# Find all matches where a new row starts
matches = list(pattern.finditer(full_content))

rows = []
for i in range(len(matches)):
    start = matches[i].start()
    if i + 1 < len(matches):
        end = matches[i + 1].start()
    else:
        end = len(full_content)
    row_text = full_content[start:end].strip()
    rows.append(row_text)
```

### 3.4. Parse Each Row into Columns

Given that there are **38 columns**, we'll split each row into 38 parts. However, due to potential inconsistencies in the data (like merged columns or missing values), we'll implement a more robust splitting mechanism.

#### 3.4.1. Define a Splitting Function

We'll use a combination of regular expressions and fixed-width splitting to accurately map data to columns.

```python
def split_row(row, num_columns):
    """
    Splits a row into the specified number of columns.
    Attempts to handle cases where fields may contain spaces.
    """
    # Split the row based on spaces, but keep in mind some fields may contain spaces
    # We'll use a regex that splits only on single spaces assuming multiple spaces were already reduced
    parts = row.split(' ')
    
    # If the number of parts is more than the number of columns, some fields contain spaces
    # We'll need to intelligently merge them
    if len(parts) < num_columns:
        # Not enough parts; return None to indicate a problematic row
        return None
    elif len(parts) == num_columns:
        return parts
    else:
        # More parts than columns; attempt to merge extra parts into specific columns
        # This requires domain-specific knowledge. For simplicity, let's assume that certain columns can have spaces
        # For example, 'Дисциплина', 'Специализация/Образовательная программа', 'ФИО ППС', 'Должность'
        # We'll attempt to merge excess parts into these columns

        # Columns likely to have spaces
        merge_columns = [1, 4, 26, 27]  # Zero-based indices for 'Дисциплина', 'Специализация...', 'ФИО ППС', 'Должность'
        
        # Initialize a list to store the corrected parts
        corrected_parts = []
        current_part = ""
        merge_idx = 0  # Index to track which column to merge

        for idx, part in enumerate(parts):
            if idx in merge_columns:
                # Start merging from this part
                current_part += part + ' '
            elif idx > merge_columns[-1] and current_part:
                # Continue merging until a pattern is detected
                current_part += part + ' '
                # Here, you might implement specific logic to detect the end of the merged field
            else:
                corrected_parts.append(part)
        
        # After merging, you need to ensure the number of parts matches
        # This can be complex and might require manual adjustments based on data patterns
        # For simplicity, this function returns None if it cannot accurately split the row
        return None
```

**Note**: The above function is a placeholder. Given the complexity of the data, a fully automated splitting might not be feasible without more specific patterns. Instead, we'll use a more straightforward approach and handle exceptions as they arise.

#### 3.4.2. Mapping Rows to Columns

We'll attempt to split each row into 38 parts. If a row doesn't match, we'll log it for manual review.

```python
parsed_data = []
problematic_rows = []

for row in rows:
    # Attempt to split the row into parts
    # We'll use a regex that splits on spaces but keeps consecutive spaces as a single delimiter
    parts = re.split(r'\s{2,}', row)  # Splitting on two or more spaces

    if len(parts) == len(columns):
        parsed_data.append(parts)
    else:
        # If the split doesn't result in 38 parts, try alternative splitting
        # For example, splitting on single spaces
        parts_single = row.split(' ')
        if len(parts_single) == len(columns):
            parsed_data.append(parts_single)
        else:
            # Row is problematic; add to the list for manual inspection
            problematic_rows.append(row)

# Inform the user about any problematic rows
if problematic_rows:
    print(f"Found {len(problematic_rows)} problematic rows that need manual review.")
else:
    print("All rows parsed successfully.")
```

**Handling Problematic Rows**:

For rows that don't split into 38 parts, you may need to:

- **Manually Inspect**: Review the `problematic_rows` list to identify patterns or specific issues.
- **Adjust Splitting Logic**: Modify the regex or splitting strategy based on observed issues.
- **Use Heuristics**: Implement rules to handle common inconsistencies.

For the sake of this guide, we'll proceed assuming that most rows split correctly. You can handle the problematic rows separately based on your specific needs.

---

## Step 4: Creating the Structured DataFrame

Now, we'll convert the parsed data into a `pandas` DataFrame with the defined columns.

```python
# Create DataFrame
df = pd.DataFrame(parsed_data, columns=columns)

# Display the first few rows to verify
print(df.head())
```

### 4.1. Data Cleaning and Type Conversion

Ensure that numerical columns are correctly formatted as integers or floats.

```python
# List of columns that should be numerical
numerical_columns = [
    "№",
    "Количество кредитов",
    "Курс обучения",
    "Количество обучающихся",
    "Количество потоков (лекции/СРСП)",
    "Количество потоков (практические/лабораторные)",
    "Лекционных занятий",
    "Лаборат орных занятий",
    "СРС П",
    "Рубежный контроль",
    "Консультации",
    "Экзаменов",
    "Всего учебных часов к расчету штатов 1 семестр",
    "Всего учебных часов к расчету штатов 2 семестр",
    "Всего учебных часов к расчету",
    "Курсера (часы)",
    "Кол-во штатных часов или почасовых",
    "Шт ед по штату ИЛИ почасовой",
    "Штатная нагрузка",
    "Почасова я нагрузка",
    "Шт.ед. по штату",
    "Шт.ед. по почасовой",
    "Шт ед почасовой на 2-ой семестр",
    "Почасовая нагрузка Семестр 2",
    "Шт.ед. по почасовой по дис Семестр 2"
]

# Convert numerical columns to appropriate data types
for col in numerical_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Check for any NaN values resulting from conversion issues
print(df[numerical_columns].isnull().sum())
```

**Handling Conversion Issues**:

- **`errors='coerce'`**: This parameter converts non-convertible values to `NaN`. You can later decide how to handle these (e.g., fill with zeros, remove rows, etc.).
- **Manual Review**: For columns with high `NaN` counts, consider manual review or more sophisticated parsing.

### 4.2. Handling Missing or Extra Data

If certain columns have missing data (`NaN`), you can choose to fill them or leave them as is based on your requirements.

```python
# Example: Fill NaN with zeros for numerical columns
df[numerical_columns] = df[numerical_columns].fillna(0)

# Alternatively, you can leave NaN values for later analysis
```

---

## Step 5: Exporting the Structured Data

Once the DataFrame is clean and structured, export it to a desired format such as CSV or Excel.

### 5.1. Export to CSV

```python
# Path to save the CSV file
csv_file_path = r'C:\Users\syrym\Downloads\individualplan\structured_data.csv'

# Export DataFrame to CSV
df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

print(f"Data exported successfully to {csv_file_path}")
```

### 5.2. Export to Excel

```python
# Path to save the Excel file
excel_file_path = r'C:\Users\syrym\Downloads\individualplan\structured_data.xlsx'

# Export DataFrame to Excel
df.to_excel(excel_file_path, index=False)

print(f"Data exported successfully to {excel_file_path}")
```

---

## Complete Python Script

For your convenience, here's the complete script combining all the steps:

```python
import json
import pandas as pd
import re

# Define the list of 38 columns
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
    "Прак тичес ких, семи нарск их занятий",
    "Лаборат орных занятий",
    "СРС П",
    "Рубежный контроль",
    "Консультации",
    "Экзаменов",
    "Всего учебных часов к расчету штатов 1 семестр",
    "Всего учебных часов к расчету штатов 2 семестр",
    "Всего учебных часов к расчету",
    "Курсера (часы)",
    "признак Курсера",
    "ФИО ППС",
    "Должность",
    "Форма оплаты",
    "Кол-во штатных часов или почасовых",
    "Шт ед по штату ИЛИ почасовой",
    "Штатная нагрузка",
    "Почасова я нагрузка",
    "Шт.ед. по штату",
    "Шт.ед. по почасовой",
    "Шт ед почасовой на 2-ой семестр",
    "Почасовая нагрузка Семестр 2",
    "Шт.ед. по почасовой по дис Семестр 2"
]

# Path to your JSON file
json_file_path = r'C:\Users\syrym\Downloads\individualplan\extracted_pdf_data.json'

# Load JSON data
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Concatenate content from all pages
full_content = ""
for page in data:
    full_content += page.get('content', '') + "\n"

# Initial cleaning: replace multiple spaces with a single space
full_content = re.sub(r'\s+', ' ', full_content)

# Regex pattern to identify rows starting with a number followed by a space
pattern = re.compile(r'(\d+)\s')

# Find all matches where a new row starts
matches = list(pattern.finditer(full_content))

rows = []
for i in range(len(matches)):
    start = matches[i].start()
    if i + 1 < len(matches):
        end = matches[i + 1].start()
    else:
        end = len(full_content)
    row_text = full_content[start:end].strip()
    rows.append(row_text)

# Split each row into parts based on two or more spaces
parsed_data = []
problematic_rows = []

for row in rows:
    parts = re.split(r'\s{2,}', row)  # Splitting on two or more spaces
    if len(parts) == len(columns):
        parsed_data.append(parts)
    else:
        # Attempt alternative splitting or log for manual review
        parts_single = row.split(' ')
        if len(parts_single) == len(columns):
            parsed_data.append(parts_single)
        else:
            problematic_rows.append(row)

# Inform the user about any problematic rows
if problematic_rows:
    print(f"Found {len(problematic_rows)} problematic rows that need manual review.")
else:
    print("All rows parsed successfully.")

# Create DataFrame
df = pd.DataFrame(parsed_data, columns=columns)

# Convert numerical columns to appropriate data types
numerical_columns = [
    "№",
    "Количество кредитов",
    "Курс обучения",
    "Количество обучающихся",
    "Количество потоков (лекции/СРСП)",
    "Количество потоков (практические/лабораторные)",
    "Лекционных занятий",
    "Лаборат орных занятий",
    "СРС П",
    "Рубежный контроль",
    "Консультации",
    "Экзаменов",
    "Всего учебных часов к расчету штатов 1 семестр",
    "Всего учебных часов к расчету штатов 2 семестр",
    "Всего учебных часов к расчету",
    "Курсера (часы)",
    "Кол-во штатных часов или почасовых",
    "Шт ед по штату ИЛИ почасовой",
    "Штатная нагрузка",
    "Почасова я нагрузка",
    "Шт.ед. по штату",
    "Шт.ед. по почасовой",
    "Шт ед почасовой на 2-ой семестр",
    "Почасовая нагрузка Семестр 2",
    "Шт.ед. по почасовой по дис Семестр 2"
]

for col in numerical_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Handle missing numerical data (optional)
df[numerical_columns] = df[numerical_columns].fillna(0)

# Export to CSV
csv_file_path = r'C:\Users\syrym\Downloads\individualplan\structured_data.csv'
df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
print(f"Data exported successfully to {csv_file_path}")

# Export to Excel (optional)
excel_file_path = r'C:\Users\syrym\Downloads\individualplan\structured_data.xlsx'
df.to_excel(excel_file_path, index=False)
print(f"Data exported successfully to {excel_file_path}")

# Optionally, save problematic rows for manual review
if problematic_rows:
    with open(r'C:\Users\syrym\Downloads\individualplan\problematic_rows.txt', 'w', encoding='utf-8') as f:
        for row in problematic_rows:
            f.write(row + '\n')
    print(f"Problematic rows saved to problematic_rows.txt")
```

---

## Step 6: Reviewing and Validating the Structured Data

After exporting, it's crucial to validate the structured data to ensure accuracy.

### 6.1. Open the Exported File

- **CSV**: Use Excel, Google Sheets, or any text editor.
- **Excel**: Use Microsoft Excel or compatible software.

### 6.2. Check for Consistency

- **Column Alignment**: Ensure that each data point is under the correct column.
- **Data Types**: Verify that numerical columns contain numbers and text columns contain appropriate data.
- **Missing Values**: Identify and address any missing or `NaN` values.

### 6.3. Handle Problematic Rows

If there are rows that didn't parse correctly:

1. **Manual Inspection**: Open the `problematic_rows.txt` file and inspect the rows.
2. **Adjust Parsing Logic**: Modify the Python script to handle specific patterns or anomalies observed.
3. **Re-Run Parsing**: Update the script and re-parse the data as needed.

---

## Additional Tips and Best Practices

1. **Backup Your Data**: Always keep a copy of the original JSON file before making changes.
2. **Iterative Parsing**: Start by parsing a subset of data to ensure the logic works before processing the entire dataset.
3. **Regular Expressions (Regex)**: Mastering regex can significantly enhance your ability to parse complex data.
4. **Data Validation**: Implement checks to validate data integrity, such as ensuring required fields are not empty.
5. **Documentation**: Keep notes on any assumptions or specific rules applied during parsing for future reference.

---

## Alternative Approach: Using Specialized PDF Table Extraction Tools

If you find the parsing process too cumbersome or if the data extraction isn't accurate, consider using specialized tools designed for extracting tables from PDFs:

1. **Tabula**: An open-source tool that can extract tables from PDFs into CSV or Excel.
   - [Tabula Website](https://tabula.technology/)
   - **Usage**: Upload your PDF and manually select the table areas for extraction.

2. **Camelot**: A Python library that can extract tables from PDFs.
   - [Camelot Documentation](https://camelot-py.readthedocs.io/en/master/)
   - **Usage**: Install Camelot and use it to programmatically extract tables.

   ```bash
   pip install camelot-py[cv]
   ```

   ```python
   import camelot

   # Path to your PDF file
   pdf_path = r'C:\Users\syrym\Downloads\individualplan\Жакыпбеков С.Ж. 2024-2025.pdf'

   # Extract tables
   tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')  # 'stream' works well for tables without borders

   # Export all tables to a single DataFrame
   df_list = [table.df for table in tables]
   combined_df = pd.concat(df_list, ignore_index=True)

   # Save to Excel or CSV
   combined_df.to_excel(r'C:\Users\syrym\Downloads\individualplan\camelot_extracted.xlsx', index=False)
   ```

3. **Adobe Acrobat Pro**: Offers advanced PDF editing and table extraction features.
   - **Usage**: Use the "Export PDF" feature to convert PDF tables to Excel or CSV.

These tools might provide a more accurate extraction, especially if the PDF has well-defined table structures.

---

## Final Thoughts

Transforming unstructured JSON data into a well-organized table with 38 columns is a meticulous process, especially with complex and potentially inconsistent data. By following the steps outlined above, you can automate much of the process and ensure that your data is accurately mapped to the desired structure.
