import os
from pypdf import PdfReader
import json
import re #to process the text
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')         # Tokenizer
nltk.download('stopwords')     # Stopword list
nltk.download('wordnet')       # Lemmatizer model

# Data Collection
def load_raw_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"file not found: {path}")
    
    if path.endswith(".pdf"):  # If it is a pdf file
        print('This is a PDF')
        return parse_pdf_to_text(path)
    elif path.endswith(".txt"): # If it is a pdf file
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        raise ValueError("This file is unsupported")

def parse_pdf_to_text(path):
    extracted_text = ""
    reader = PdfReader(path)
    for i in reader.pages: #Loop though the pdf pages and use pypdf to extract text
        extracted_text += i.extract_text() or ""
    return extracted_text # return text

def save_processed_data(data, output_path):
    if output_path.endswith(".json"): # IF output path ends with json
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4) # save in a json file
    elif output_path.endswith(".txt"): # IF output path ends with txt
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(data) # save in a json file
    else:
        raise ValueError("Unsupported output format. Use .json or .txt extensions.")
    print(f"Data saved successfully to {output_path}")


#Text Processing
def text_preprocessing(text):
    
    text = text.lower() #convert the text to lowercase
    text = re.sub(r"http\S+|www\S+",'', text) # this removes urls
    
    text = re.sub(r"\S+@\S+",'',text) # this line removes email addresses
    
    text = re.sub("[^\w\s]",'',text) # this line removes punctuations
    text = re.sub(r'\d+','',text) # this line removes numbers
    text = re.sub(r'\s+', ' ', text).strip() # this line removes excessive whitespaces and replaces with just one
    tokens_text = word_tokenize(text) # to break down the text into an array based on whitespaces
    stopwords_arr = set(stopwords.words('english')) #group of stopwords gotten from the library
    filtered_token_text = []
    for i in tokens_text: # loop through stopword, if i not in stopword add it to filtered_token_text
        if i not in stopwords_arr:
            filtered_token_text.append(i)
    lemmatizer = WordNetLemmatizer() # to reduce words to their simplest form. e.g running -> run
    lemmatized_array = []
    for i in filtered_token_text: # loop through filtered tokens text and use the lemmatizer library
        lemmatized_word = lemmatizer.lemmatize(i)
        lemmatized_array.append(lemmatized_word)
    
    save_processed_data({"raw_text": lemmatized_array}, text_lemmatizer_output_path) # save th elemmatized output into a file
    return lemmatized_array # return the lemmatized array
    
    
    
    
    


if __name__ == "__main__":
    input_path = "message.txt" #Input Path
    text_collection_output_path = "data_process.json" # Output path for storing the data from text collection
    text_lemmatizer_output_path = "lemmatized.json" # Output path for storing the data from text proccessing
    
    extracted_text = load_raw_data(input_path) #returned data from data collection
    save_processed_data({"raw_text": extracted_text}, text_collection_output_path) # Saved process data as JSON

    with open(text_collection_output_path, 'r', encoding='utf-8') as file: # read the json file so it can be used for text processing
        json_data = json.load(file)
        raw_text = json_data.get("raw_text", "")        
    text_preprocessing(raw_text) # text processing function