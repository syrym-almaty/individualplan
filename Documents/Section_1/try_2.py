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
