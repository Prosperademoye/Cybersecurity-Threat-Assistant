import os
from pypdf import PdfReader
import json

# Data Collection
def load_raw_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"file not found: {path}")
    
    if path.endswith(".pdf"):
        print('pdf')
        return parse_pdf_to_text(path)
    elif path.endswith(".txt"):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        raise ValueError("This file is unsupported")

def parse_pdf_to_text(path):
    extracted_text = ""
    reader = PdfReader(path)
    for i in reader.pages:
        extracted_text += i.extract_text() or ""
    return extracted_text

def save_processed_data(data, output_path):
    if output_path.endswith(".json"):
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    elif output_path.endswith(".txt"):
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(data)
    else:
        raise ValueError("Unsupported output format. Use .json or .txt extensions.")
    print(f"Data saved successfully to {output_path}")



if __name__ == "__main__":
    # input_path = "midterm.pdf"
    input_path = "message.txt"
    output_path = "out.json"
    extracted = load_raw_data(input_path)
    save_processed_data(extracted, output_path)