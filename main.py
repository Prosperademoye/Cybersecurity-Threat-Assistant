import os
from pypdf import PdfReader
import json
import re #to process the text
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
from spacy.util import minibatch
import random
from spacy.training import Example


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

#NER
def train_ner_model(data, output_dir='ner_models'):
    nlp = spacy.blank("en") #initialize a new spacy model
    if "ner" not in nlp.pipe_names: #Check if ner is already int he pipeline
        ner = nlp.add_pipe("ner", last=True)
    else: #if its not add it
        ner = nlp.get_pipe("ner")
    
    for _, annotations in training_data:  #loop through the training data. the goal is to get the label in this case it is MALWARE
        for ent in annotations['entities']: #loop though the entities dictionary
            ner.add_label(ent[2]) # add the label to our ner pipeline. to know which label to recognize when training 
    
    optimizer = nlp.begin_training()  # initiazlize the training process
    examples = []
    for text, annotations in training_data:
        if not isinstance(text, str):  # Debugging check
            raise TypeError(f"Expected 'text' to be str, got {type(text).__name__}")
        doc = nlp.make_doc(text)  # Convert the text to a spaCy Doc object
        example = Example.from_dict(doc, annotations)  # Create an Example object
        examples.append(example) #split the training data into input and output
    for _ in range(80): #run the training process 20 times
        random.shuffle(examples) #shuffle the training data so the model doesn't overfit to the order
        losses = {} #dictionary to track losses
        for batch in minibatch(examples, size=2): #split the training data into smaller batches of size 2 for each training step. THis improves performance and reduces memory overload
            nlp.update(batch, losses=losses)
            print(f"loss: {losses}")
    nlp.to_disk(output_dir) #save the model to output_dir
    print(f"model saved to {output_dir}")
            

def extract_entities(text, model):
    if not model:
        raise ValueError("Load a value first")
    doc = model(text) #passes the text through the model
    entities = []
    for ent in doc.ents:  #put the text into a specific format
        entity = {
            "text": ent.text,
            "start": ent.start_char,
            "end": ent.end_char,
            "label": ent.label_
        }
        entities.append(entity)

    return entities
    
def load_ner_model(model_path):  #loading our ner model
    nlp = spacy.load(model_path) # load model from the path
    print(f"Model loaded successfully from {model_path}")
    return nlp
    
    
    
    
    


if __name__ == "__main__":
    input_path = "message.txt" #Input Path
    text_collection_output_path = "data_process.json" # Output path for storing the data from text collection
    text_lemmatizer_output_path = "lemmatized.json" # Output path for storing the data from text proccessing
    
    extracted_text = load_raw_data(input_path) #returned data from data collection
    save_processed_data({"raw_text": extracted_text}, text_collection_output_path) # Saved process data as JSON

    with open(text_collection_output_path, 'r', encoding='utf-8') as file: # read the json file so it can be used for text processing
        json_data = json.load(file)
        raw_text = json_data.get("raw_text", "")        
    processed_text = text_preprocessing(raw_text) # text processing function
    
    # Step 3: Train NER Model
    training_data = [
    (
        "Wannacry is a malware that exploited Windows systems.",
        {"entities": [(0, 8, "MALWARE"), (12, 19, "MALWARE"), (41, 48, "SYSTEM")]}
    ),
    (
        "NotPetya, a ransomware, targeted Linux servers.",
        {"entities": [(0, 8, "MALWARE"), (24, 29, "MALWARE"), (38, 43, "SYSTEM")]}
    ),
    (
        "The Emotet malware affects macOS and Linux systems.",
        {"entities": [(4, 10, "MALWARE"), (15, 22, "MALWARE"), (30, 35, "SYSTEM"), (40, 45, "SYSTEM")]}
    ),
    (
        "The CVE-2021-44228 vulnerability is linked to Apache Log4j.",
        {"entities": [(4, 20, "CVE"), (44, 50, "SYSTEM")]}
    ),
    (
        "A critical issue was discovered in CVE-2023-1234 affecting servers.",
        {"entities": [(29, 41, "CVE"), (52, 59, "SYSTEM")]}
    ),
    (
        "Researchers found that CVE-2019-0708 is actively exploited on Windows systems.",
        {"entities": [(21, 33, "CVE"), (57, 64, "SYSTEM")]}
    ),
    (
        "The ransomware attack exploited CVE-2022-22620 and targeted macOS devices.",
        {"entities": [(4, 14, "MALWARE"), (30, 42, "CVE"), (57, 62, "SYSTEM")]}
    ),
    (
        "CVE-2017-0144 was used by the EternalBlue exploit to target Windows.",
        {"entities": [(0, 12, "CVE"), (48, 55, "SYSTEM")]}
    ),
    (
        "Trickbot, a malware, uses CVE-2020-10189 to affect IoT devices.",
        {"entities": [(0, 9, "MALWARE"), (13, 20, "MALWARE"), (26, 38, "CVE"), (50, 61, "SYSTEM")]}
    ),
    (
        "The attack caused a denial-of-service on Linux and Windows servers.",
        {"entities": [(38, 43, "SYSTEM"), (48, 55, "SYSTEM")]}
    ),
    (
        "MacOS and iOS devices were targeted by the spyware.",
        {"entities": [(0, 5, "SYSTEM"), (10, 13, "SYSTEM"), (43, 50, "MALWARE")]}
    ),
    (
        "Android phones and tablets were infected by the malware.",
        {"entities": [(0, 7, "SYSTEM"), (18, 25, "SYSTEM"), (41, 48, "MALWARE")]}
    ),
    (
        "CVE-2021-34527, known as PrintNightmare, affects Windows print services.",
        {"entities": [(0, 14, "CVE"), (25, 39, "MALWARE"), (49, 56, "SYSTEM")]}
    ),
    (
        "SolarWinds Orion was compromised by SUNBURST malware through CVE-2020-10148.",
        {"entities": [(0, 18, "SYSTEM"), (36, 43, "MALWARE"), (51, 63, "CVE")]}
    ),
    (
        "The exploit CVE-2022-23818 targets IoT and Android systems.",
        {"entities": [(12, 26, "CVE"), (35, 38, "SYSTEM"), (43, 50, "SYSTEM")]}
    ),]
    training_data += [
    ("Another case of malware was reported.", {"entities": [(17, 24, "MALWARE")]}),
    ("This is a report about Wannacry affecting Windows.", {"entities": [(22, 30, "MALWARE"), (41, 48, "SYSTEM")]}),
    ("That vulnerability, CVE-2023-4567, affects Linux servers.", {"entities": [(21, 35, "CVE"), (44, 49, "SYSTEM")]}),
    ("Another example involves no specific malware or systems.", {"entities": []}),]
    training_data += [
    ("A malware named Trickbot attacked Linux systems.", 
     {"entities": [(2, 9, "MALWARE"), (24, 32, "MALWARE"), (41, 46, "SYSTEM")]}),
    ("Windows servers were targeted by the ransomware.", 
     {"entities": [(0, 7, "SYSTEM"), (39, 48, "MALWARE")]}),
    ("The malware affects both macOS and Linux.", 
     {"entities": [(4, 11, "MALWARE"), (28, 33, "SYSTEM"), (38, 43, "SYSTEM")]}),
]




    train_ner_model(training_data)
    
    ner_model = load_ner_model("ner_models")
    
    test_text = "Another malware named Wannacry affected Windows systems in 2017."
    entities = extract_entities(test_text, ner_model)
    print("Extracted Entities:", entities)