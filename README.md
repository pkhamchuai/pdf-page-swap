Here is the **Markdown documentation** for both programs, formatted for a GitHub repository:

---

# PDF Page Manipulation Tools

This repository contains two Python programs to process PDF files using the `PyPDF2` library. Each tool performs a specific task: 

1. **Swap Even and Odd Pages with Optional Page Size Adjustment**  
2. **Adjust PDF Page Sizes to the Most Common Dimensions**

---

## Table of Contents
- [Requirements](#requirements)
- [Tool 1: Swap Even and Odd Pages with Optional Page Size Adjustment](#tool-1-swap-even-and-odd-pages-with-optional-page-size-adjustment)
  - [Description](#description)
  - [Usage Instructions](#usage-instructions)
- [Tool 2: Adjust PDF Page Sizes to the Most Common Dimensions](#tool-2-adjust-pdf-page-sizes-to-the-most-common-dimensions)
  - [Description](#description)
  - [Usage Instructions](#usage-instructions)

---

## Requirements

Both tools require the following:
- **Python 3.8+**
- **PyPDF2 library**

Install the required library using pip:
```bash
pip install pypdf2
```

---

## Tool 1: Swap Even and Odd Pages with Optional Page Size Adjustment

### Description
This tool:
1. **Swaps even and odd pages** in a PDF document.
2. **Swaps the first two pages** for additional customization.
3. **Adjusts all page sizes** to match the most common dimensions in the document.

### Usage Instructions

#### Input Preparation
- Place all PDF files you want to process in the `input` folder.
- Alternatively, specify the input file or directory in the command line.

#### Command
```bash
python swap_pages.py [input]
```

- **If no input is specified**, the program processes all PDF files in the `input` folder.
- **Output**: Processed PDFs will be saved in the `output` folder with `_swapped_adjusted` appended to the filename.

#### Examples
- Process a single file:
  ```bash
  python swap_pages.py /path/to/file.pdf
  ```
- Process all PDFs in a specific directory:
  ```bash
  python swap_pages.py /path/to/directory
  ```
- Process all PDFs in the `input` folder (default behavior):
  ```bash
  python swap_pages.py
  ```

---

## Tool 2: Adjust PDF Page Sizes to the Most Common Dimensions

### Description
This tool:
1. Analyzes the page sizes of a PDF file.
2. Adjusts all pages to the **most common dimensions** (e.g., width and height) in the document.

### Usage Instructions

#### Input Preparation
- Place all PDF files you want to process in the `input` folder.
- Alternatively, specify the input file or directory in the command line.

#### Command
```bash
python adjust_page_size.py [input]
```

- **If no input is specified**, the program processes all PDF files in the `input` folder.
- **Output**: Processed PDFs will be saved in the `output` folder with `_adjusted` appended to the filename.

#### Examples
- Adjust a single file:
  ```bash
  python adjust_page_size.py /path/to/file.pdf
  ```
- Adjust all PDFs in a specific directory:
  ```bash
  python adjust_page_size.py /path/to/directory
  ```
- Adjust all PDFs in the `input` folder (default behavior):
  ```bash
  python adjust_page_size.py
  ```

---

## Output Folders
Both tools generate an `output` folder automatically if it does not exist. Processed files are saved here with descriptive suffixes:
- `_swapped_adjusted` for the first tool.
- `_adjusted` for the second tool.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This documentation should make your repository clear and easy to use. Let me know if you need more details or additional sections!
