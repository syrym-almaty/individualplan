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
