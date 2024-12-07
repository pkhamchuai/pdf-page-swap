import os
import subprocess
from pathlib import Path

def ensure_output_folder():
    """Ensure the output folder exists."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def process_pdf_with_pdftk(input_file, output_dir):
    """
    Use pdftk to switch even and odd pages for a single PDF file.
    
    Args:
        input_file (str): Path to the input PDF file.
        output_dir (Path): Path to the output directory.
    """
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
        process_pdf_with_pdftk(str(pdf_file), output_dir)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Swap even and odd pages in PDF files using pdftk.")
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
        process_pdf_with_pdftk(str(input_path), output_dir)
    elif input_path.is_dir():
        process_directory(str(input_path))
    else:
        print(f"Error: The path {args.input} is not a valid file or directory.")

if __name__ == "__main__":
    main()
