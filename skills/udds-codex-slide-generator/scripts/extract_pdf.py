import sys
import os
import argparse
from pathlib import Path

def extract_pdf_to_images(pdf_path, base_output_dir):
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("Error: PyMuPDF not installed. Please run: pip install PyMuPDF")
        sys.exit(1)
        
    if not os.path.exists(pdf_path):
        print(f"Error: File not found - {pdf_path}")
        sys.exit(1)
        
    # Create a subfolder named after the PDF file (without extension)
    pdf_filename = Path(pdf_path).stem
    working_dir = os.path.join(base_output_dir, pdf_filename)
    
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        print(f"Found {total_pages} pages in PDF.")
        print(f"Creating working directory: {working_dir}")
        print("Starting extraction...")
        
        for i in range(total_pages):
            page = doc.load_page(i)
            # Increase resolution (zoom factor 2 = high quality)
            zoom_x = 2.0
            zoom_y = 2.0
            mat = fitz.Matrix(zoom_x, zoom_y)
            pix = page.get_pixmap(matrix=mat)
            
            # Save as page_1.png, page_2.png...
            output_filename = f"page_{i+1}.png"
            output_path = os.path.join(working_dir, output_filename)
            pix.save(output_path)
            print(f"Extracted: {output_filename}")
            
        print(f"\nSuccessfully extracted all {total_pages} pages to {working_dir}")
        
    except Exception as e:
        print(f"An error occurred during extraction: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract all pages of a PDF as PNG images into a dedicated working directory.")
    parser.add_argument("pdf_path", help="Path to the source PDF file")
    parser.add_argument("--output", "-o", default=".", help="Base output directory (a subfolder will be created inside this). Defaults to current dir.")
    
    args = parser.parse_args()
    extract_pdf_to_images(args.pdf_path, args.output)
