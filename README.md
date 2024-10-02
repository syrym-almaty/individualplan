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

### Step 1: Create a `.gitignore` File

A `.gitignore` file tells Git which files or directories to ignore, ensuring they don’t get added to your repository. To create a `.gitignore` file in your project directory, follow these steps:

1. **Open a terminal (Git Bash or Command Prompt)**.
2. **Navigate to your project directory**:

   ```bash
   cd ~/Downloads/individualplan
   ```

3. **Create the `.gitignore` file**:
   Use a text editor to create the `.gitignore` file. You can use `touch` to create it:

   ```bash
   touch .gitignore
   ```

4. **Open the file** and add the following common entries to exclude unnecessary files. You can edit it with a text editor like `nano` or use Visual Studio Code:

   ```bash
   nano .gitignore
   ```

### Sample `.gitignore` for Python projects

```bash
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.so

# Virtual environments
venv/
individualplan/

# Logs
*.log

# OS generated files
.DS_Store
Thumbs.db

# Python-specific cache and settings
*.sqlite3
*.db
*.env
.env.*

# IDE and editor settings
.vscode/
.idea/
*.sublime-project
*.sublime-workspace

# Coverage reports
htmlcov/
.coverage

# Jupyter Notebook files
.ipynb_checkpoints/

# Other project files
*.bak
*.tmp
```

This will exclude common unnecessary files and directories, such as:

- Python bytecode (`__pycache__/` and `*.pyc`)
- Virtual environments (`venv/`, `individualplan/`)
- Log files (`*.log`)
- IDE/editor settings (e.g., `.vscode/`, `.idea/`)

### Step 2: Stop Tracking Unnecessary Files Already Added

If you’ve already run `git add .` and committed unnecessary files, you can stop tracking them without deleting them from your working directory by following these steps:

1. **Update `.gitignore`** with the appropriate rules (as shown above).

2. **Remove cached files** that were already added but should be ignored:

   ```bash
   git rm -r --cached .
   ```

   This will unstage all files, but **won’t delete them** from your local directory. It simply removes them from Git’s index so they won’t be tracked.

3. **Re-add the necessary files**:

   ```bash
   git add .
   ```

   This will re-add only the files that are **not excluded by the `.gitignore` file**.

4. **Commit the changes**:

   ```bash
   git commit -m "Remove unnecessary files and update .gitignore"
   ```

### Step 3: Undoing the Accidental `git add .`

If you accidentally ran `git add .` and staged a lot of unnecessary files, you can undo it:

1. **Unstage all files**:

   If you haven’t committed yet, you can unstage everything by running:

   ```bash
   git reset
   ```

   This will unstage all files, but they will still remain in your working directory.

2. **Check the status**:

   After running the reset, check the status to verify:

   ```bash
   git status
   ```

   You should now see all files unstaged.

3. **Add only the necessary files**:

   Now you can manually add only the necessary files or directories:

   ```bash
   git add <specific_file_or_directory>
   ```

### Step 4: Abort an Accidental Commit

If you’ve already committed and need to undo the last commit:

1. **Soft reset the last commit** (keeps your changes):

   ```bash
   git reset --soft HEAD~1
   ```

   This will undo the last commit but leave your changes staged, so you can amend them or remove them.

2. **Hard reset (if necessary)**:

   If you want to completely remove the last commit and the changes (be careful as this cannot be undone):

   ```bash
   git reset --hard HEAD~1
   ```

   This will remove the commit and any changes made in it.

### Step 5: Exclude Specific Files Already Added by Mistake

If you want to exclude specific files or directories that you accidentally committed and push that change, you can do the following:

1. Add the paths of the unwanted files to your `.gitignore`.
2. Then run:

   ```bash
   git rm --cached <file_or_directory>
   ```

3. Finally, commit the changes:

   ```bash
   git commit -m "Remove unwanted files from being tracked"
   ```

Now your repository should be clean and your `.gitignore` will prevent unwanted files from being tracked in the future.

### Step 6: Push the Changes to GitHub (If Necessary)

Once everything looks good, push the changes:

```bash
git push origin main
```

It seems that you’ve accidentally staged a large number of files in your Git repository, including virtual environment files (which should generally be excluded). Let me guide you through aborting this and cleaning up your repository.

### Step 1: Undo `git add .`

If you accidentally staged files with `git add .` and you want to unstage them (but **keep them** in your working directory), use:

```bash
git reset
```

```bash
git status
```

### Step 2: Update `.gitignore` to Exclude Unnecessary Files

You should update your `.gitignore` to prevent unnecessary files from being staged in the future. Since your virtual environment was staged, add it to `.gitignore`.

1. Open `.gitignore` (or create it if it doesn’t exist):

    ```bash
    nano .gitignore
    ```

2. Add the following entries to ignore virtual environment and other unnecessary files:

    ```bash
    # Virtual environment directories
    .venv/
    venv/

    # Byte-compiled / optimized files
    __pycache__/
    *.py[cod]

    # OS generated files
    .DS_Store
    Thumbs.db

    # Logs
    *.log

    # Python egg metadata
    *.egg-info/
    .eggs/
    ```

3. Save and close the file.

### Step 3: Remove Tracked Virtual Environment Files

If you’ve already committed files from your `.venv/` folder and you now want Git to stop tracking them, but keep them locally, run:

```bash
git rm -r --cached .venv
```

This will remove the virtual environment files from Git’s tracking, but not from your local machine.

Next, commit the removal:

```bash
git commit -m "Remove .venv from tracking"
```

### Step 4: Add Relevant Files Back

After cleaning up, you can re-add the files you actually want to stage:

```bash
git add <file_or_directory>
```

Or if everything is cleaned up, use:

```bash
git add .
```

### Step 5: Push Changes to Remote (Optional)

If you are working with a remote repository (like GitHub) and you’ve cleaned up everything, push the changes:

```bash
git push origin main
```

### Recap

- **`git reset`** to unstage the files.
- **Add `.venv/` to `.gitignore`** to prevent the virtual environment from being tracked.
- **`git rm -r --cached .venv`** to stop tracking the virtual environment files already added.
- **Re-add the files you actually need** for the commit.
