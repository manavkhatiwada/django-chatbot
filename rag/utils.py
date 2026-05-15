# from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma


# from .embeddings import embeddings

from pypdf import PdfReader
import re

CHROMA_PATH = 'chroma_db'


#extract text 

def text_extract_pdf(pdf_path):
        reader = PdfReader(pdf_path)

        text = " "

        for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                        text += page_text + " "

        return text 



def get_text_splitter():
        return RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )


def split_text(text):
        splitter = get_text_splitter()
        return splitter.split_text(text)
    