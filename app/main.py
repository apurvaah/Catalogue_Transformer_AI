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

# ... (rest of the file remains unchanged)
