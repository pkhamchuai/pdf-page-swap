import os
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter

def ensure_output_folder():
    """Ensure the output folder exists."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def swap_even_odd_pages(input_file, output_dir):
    """
    Swap even and odd pages in a PDF file using PyPDF2.
    
    Args:
        input_file (str): Path to the input PDF file.
        output_dir (Path): Path to the output directory.
    """
    try:
        reader = PdfReader(input_file)
        writer = PdfWriter()

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

        for page in swapped_pages:
            writer.add_page(page)

        # Write to output
        base_name = Path(input_file).stem
        output_file = output_dir / f"{base_name}_swapped.pdf"
        with open(output_file, "wb") as f:
            writer.write(f)

        print(f"Processed: {input_file} -> {output_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def process_directory(directory):
    """
    Process all PDF files in the specified directory.
    
    Args:
        directory (str): Path to the directory containing PDF files.
    """
    output_dir = ensure_output_folder()
    pdf_files = list(Path(directory).glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in directory: {directory}")
        return

    for pdf_file in pdf_files:
        swap_even_odd_pages(str(pdf_file), output_dir)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Swap even and odd pages in PDF files using PyPDF2.")
    parser.add_argument(
        "input", 
        help="Path to a single PDF file or a directory containing PDF files."
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: The path {args.input} does not exist.")
        return

    if input_path.is_file():
        output_dir = ensure_output_folder()
        swap_even_odd_pages(str(input_path), output_dir)
    elif input_path.is_dir():
        process_directory(str(input_path))
    else:
        print(f"Error: The path {args.input} is not a valid file or directory.")

if __name__ == "__main__":
    main()
