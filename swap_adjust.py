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

def swap_even_odd_pages_and_adjust_size(input_file, output_dir):
    """Swap even and odd pages, adjust page sizes, and swap the first two pages."""
    try:
        reader = PdfReader(input_file)
        writer = PdfWriter()

        # Determine the most common page size
        common_page_size = get_most_common_page_size(reader.pages)

        # Separate pages into odd and even
        odd_pages = reader.pages[::2]  # Odd-indexed pages
        even_pages = reader.pages[1::2]  # Even-indexed pages

        # Combine pages in swapped order
        swapped_pages = []
        for even, odd in zip(even_pages, odd_pages):
            swapped_pages.append(even)
            swapped_pages.append(odd)

        # If the PDF has an odd number of pages, append the last page
        if len(reader.pages) % 2 != 0:
            swapped_pages.append(odd_pages[-1])

        # Adjust page sizes and swap the first two pages
        for page in swapped_pages:
            adjust_page_size(page, common_page_size)

        if len(swapped_pages) >= 2:
            swapped_pages[0], swapped_pages[1] = swapped_pages[1], swapped_pages[0]

        # Add adjusted and swapped pages to the writer
        for page in swapped_pages:
            writer.add_page(page)

        # Write to output
        base_name = Path(input_file).stem
        output_file = output_dir / f"{base_name}_swapped_adjusted.pdf"
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
        swap_even_odd_pages_and_adjust_size(str(pdf_file), output_dir)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Swap even and odd pages in PDF files and adjust page sizes.")
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
            swap_even_odd_pages_and_adjust_size(str(input_path), output_dir)
        elif input_path.is_dir():
            process_directory(input_path, output_dir)
        else:
            print(f"Error: The path {args.input} is not a valid file or directory.")
    else:
        print("No input provided, processing all files in the 'input' folder...")
        process_directory(input_dir, output_dir)

if __name__ == "__main__":
    main()
