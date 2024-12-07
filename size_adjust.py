import os
from pathlib import Path
from collections import Counter
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import RectangleObject

def ensure_folder(folder_name):
    """Ensure the given folder exists."""
    folder = Path(folder_name)
    folder.mkdir(exist_ok=True)
    return folder

def floatify_rectangle(rect):
    """Convert a RectangleObject's coordinates to float."""
    return RectangleObject([float(coord) for coord in rect])

def get_most_common_page_size(pages):
    """Determine the most common page size in the document."""
    sizes = [
        tuple(float(coord) for coord in page.mediabox.upper_right)
        for page in pages
    ]
    most_common_size = Counter(sizes).most_common(1)[0][0]  # (width, height)
    return RectangleObject([0, 0, most_common_size[0], most_common_size[1]])

def adjust_page_size(page, target_size):
    """Resize a page to match the target size."""
    original_size = page.mediabox
    original_size = floatify_rectangle(original_size)

    scale_x = float(target_size.width) / float(original_size.width)
    scale_y = float(target_size.height) / float(original_size.height)

    # Centering the resized content on the new page
    page.scale_by(min(scale_x, scale_y))  # Scale uniformly to fit within target size
    page.mediabox = target_size

def adjust_pdf_page_sizes(input_file, output_dir):
    """Adjust all pages in a PDF to the most common page size."""
    try:
        reader = PdfReader(input_file)
        writer = PdfWriter()

        # Determine the most common page size
        common_page_size = get_most_common_page_size(reader.pages)

        # Adjust the size of each page
        for page in reader.pages:
            adjust_page_size(page, common_page_size)
            writer.add_page(page)

        # Write to output
        base_name = Path(input_file).stem
        output_file = output_dir / f"{base_name}_adjusted.pdf"
        with open(output_file, "wb") as f:
            writer.write(f)

        print(f"Processed: {input_file} -> {output_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def process_directory(directory, output_dir):
    """Process all PDF files in the specified directory."""
    pdf_files = list(Path(directory).glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in directory: {directory}")
        return

    for pdf_file in pdf_files:
        adjust_pdf_page_sizes(str(pdf_file), output_dir)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Adjust page sizes in PDF files to the most common size.")
    parser.add_argument(
        "input", 
        nargs="?",  # Optional argument
        help="Path to a single PDF file or a directory containing PDF files."
    )
    args = parser.parse_args()

    output_dir = ensure_folder("output")
    input_dir = ensure_folder("input")

    if args.input:
        input_path = Path(args.input)
        if input_path.is_file():
            adjust_pdf_page_sizes(str(input_path), output_dir)
        elif input_path.is_dir():
            process_directory(input_path, output_dir)
        else:
            print(f"Error: The path {args.input} is not a valid file or directory.")
    else:
        print("No input provided, processing all files in the 'input' folder...")
        process_directory(input_dir, output_dir)

if __name__ == "__main__":
    main()
