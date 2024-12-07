import os
import subprocess
from pathlib import Path

def ensure_folder(folder_name):
    """Ensure the given folder exists."""
    folder = Path(folder_name)
    folder.mkdir(exist_ok=True)
    return folder

def process_pdf_with_pdftk(input_file, output_dir):
    """Use pdftk to switch even and odd pages for a single PDF file."""
    base_name = Path(input_file).stem
    odd_pdf = f"{base_name}_odd.pdf"
    even_pdf = f"{base_name}_even.pdf"
    output_file = output_dir / f"{base_name}_swapped.pdf"

    try:
        # Extract odd and even pages
        subprocess.run(["pdftk", input_file, "cat", "odd", "output", odd_pdf], check=True)
        subprocess.run(["pdftk", input_file, "cat", "even", "output", even_pdf], check=True)

        # Merge even and odd pages
        subprocess.run(
            ["pdftk", "A=" + even_pdf, "B=" + odd_pdf, "shuffle", "A", "B", "output", str(output_file)],
            check=True
        )
        
        # Cleanup temporary files
        os.remove(odd_pdf)
        os.remove(even_pdf)
        
        print(f"Processed: {input_file} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {input_file}: {e}")

def process_directory(directory, output_dir):
    """Process all PDF files in the specified directory."""
    pdf_files = list(Path(directory).glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in directory: {directory}")
        return

    for pdf_file in pdf_files:
        process_pdf_with_pdftk(str(pdf_file), output_dir)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Swap even and odd pages in PDF files using pdftk.")
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
            process_pdf_with_pdftk(str(input_path), output_dir)
        elif input_path.is_dir():
            process_directory(input_path, output_dir)
        else:
            print(f"Error: The path {args.input} is not a valid file or directory.")
    else:
        print("No input provided, processing all files in the 'input' folder...")
        process_directory(input_dir, output_dir)

if __name__ == "__main__":
    main()
