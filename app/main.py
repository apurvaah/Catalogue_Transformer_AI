import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import datetime
import openai
import fitz
from PyPDF2 import PdfReader
import pymongo
import base64
import uvicorn

app = FastAPI()

# Set up CORS middleware to allow all origins (*)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMG_DIR = "output"
db_connection_string = ""

def get_json_new(FILE_FLDR, FILE_NAME):
    load_dotenv()
    db_connection_string = os.getenv("DB_CONNECTION")
    db = os.getenv("STGSUPPLIER_DB")
    # img_ids = image_save(FILE_FLDR, FILE_NAME, db_connection_string, db)
    # text_save(FILE_FLDR, FILE_NAME)
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    # processor = NewDataProcessor()
    # return processor.process_unique_keys(FILE_FLDR, FILE_NAME), img_ids

#EDIT THIS
def get_json_html(FILE_FLDR, FILE_NAME):
    load_dotenv()
    db_connection_string = os.getenv("DB_CONNECTION")
    db = os.getenv("DB")
    text_save_txt(FILE_FLDR, FILE_NAME)
    # img_ids = image_save_web(FILE_FLDR, FILE_NAME, db_connection_string, db)
    # print(f"Image IDS: {img_ids}")
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    # processor = HTMLDataProcessor()
    # return processor.process_unique_keys(FILE_FLDR, FILE_NAME), img_ids

def extract_text_from_pdf(pdf_path):
    
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        num_pages = len(reader.pages)
        text_content = ""
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text_content += page.extract_text()
    
    
    return text_content


def text_save(FILE_FLDR, FILE_NAME):
    pdf_file_path = os.path.join(FILE_FLDR, FILE_NAME)
    folder_name = os.path.splitext(FILE_NAME)[0]
    pdf_folder_path = os.path.join(FILE_FLDR, folder_name)
    os.makedirs(pdf_folder_path, exist_ok=True)
    print(f"Created folder '{folder_name}'.")
    text_file_path = os.path.join(pdf_folder_path, folder_name+".txt")
    with open(text_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(extract_text_from_pdf(pdf_file_path))
    
    
    print(f"Created text file '{folder_name}.txt' in the folder.")
    pdf_file = fitz.open(pdf_file_path)

def text_save_txt(FILE_FLDR, FILE_NAME):
    txt_file_path = os.path.join(FILE_FLDR, FILE_NAME)
    folder_name = os.path.splitext(FILE_NAME)[0]
    txt_folder_path = os.path.join(FILE_FLDR, folder_name)
    os.makedirs(txt_folder_path, exist_ok=True)
    print(f"Created folder '{folder_name}'.")
    new_txt_file_path = os.path.join(txt_folder_path, FILE_NAME)

    # Open the source text file for reading
    with open(txt_file_path, 'r', encoding='utf-8') as src_file:
        # Open the destination text file for writing
        with open(new_txt_file_path, 'w', encoding='utf-8') as dest_file:
            # Read the content of the source file and write it to the destination file
            dest_file.write(src_file.read())

    print(f"Saved text file '{FILE_NAME}' in the folder.")


@app.post("/upload/pdf/single")
async def upload_pdf_file(file: UploadFile = File(...)):
    c_directory = os.getcwd()

    c_year = str(datetime.date.today().year)
    c_date = str(datetime.date.today().month) + \
        '-' + str(datetime.date.today().day)
    fname = c_directory + f"/data/{c_year}/{c_date}/{file.filename}"
    folder_name = c_directory + f"/data/{c_year}/{c_date}"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    with open(fname, "wb") as buffer:
        buffer.write(await file.read())

    # Read the PDF file
    # Ensure pdf file size is < 11MB
    with open(fname, "rb") as pdf_file:
        pdf_data = pdf_file.read()

    # Encode the binary PDF data as Base64
    encoded_pdf_data = base64.b64encode(pdf_data)
    pdf_document = {
        "filename": file.filename,  # Set the desired filename for the PDF
        # Convert binary to string before inserting
        "pdf_data": encoded_pdf_data.decode()
    }

    # Insert the document into the MongoDB collection
    # pdf_collection.insert_one(pdf_document)

    # data, img_ids = get_json_single(folder_name, file.filename)

    # return data, img_ids

@app.post("/upload/pdf/bulknew")
async def upload_pdf_file(file: UploadFile = File(...)):
    c_directory = os.getcwd()

    c_year = str(datetime.date.today().year)
    c_date = str(datetime.date.today().month) + \
        '-' + str(datetime.date.today().day)
    fname = c_directory + f"/data/{c_year}/{c_date}/{file.filename}"
    folder_name = c_directory + f"/data/{c_year}/{c_date}"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    with open(fname, "wb") as buffer:
        buffer.write(await file.read())

    # Read the PDF file
    # Ensure pdf file size is < 11MB
    with open(fname, "rb") as pdf_file:
        pdf_data = pdf_file.read()

    # Encode the binary PDF data as Base64
    encoded_pdf_data = base64.b64encode(pdf_data)
    pdf_document = {
        "filename": file.filename,  # Set the desired filename for the PDF
        # Convert binary to string before inserting
        "pdf_data": encoded_pdf_data.decode()
    }

    # Insert the document into the MongoDB collection
    # pdf_collection.insert_one(pdf_document)

    data, img_ids = get_json_new(folder_name, file.filename)

    return data, img_ids

@app.post("/upload/htmlcontent")
async def upload_html(file: UploadFile = File(...)):
    c_directory = os.getcwd()

    c_year = str(datetime.date.today().year)
    c_date = str(datetime.date.today().month) + \
        '-' + str(datetime.date.today().day)
    fname = c_directory + f"/data/{c_year}/{c_date}/{file.filename}"
    folder_name = c_directory + f"/data/{c_year}/{c_date}"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    with open(fname, "wb") as buffer:
        buffer.write(await file.read())
    data, img_ids = get_json_html(folder_name, file.filename)
    
    return data, img_ids

@app.post("/upload/pdf/bulk")
async def upload_pdf_file_bulk(file: UploadFile = File(...)):
    c_directory = os.getcwd()

    c_year = str(datetime.date.today().year)
    c_date = str(datetime.date.today().month) + \
        '-' + str(datetime.date.today().day)
    fname = c_directory + f"/data/{c_year}/{c_date}/{file.filename}"
    folder_name = c_directory + f"/data/{c_year}/{c_date}"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    with open(fname, "wb") as buffer:
        buffer.write(await file.read())

    # data, img_ids = get_json(folder_name, file.filename)

    # return data, img_ids

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
