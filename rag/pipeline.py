from .utils import text_extract_pd,split_text
from .chroma import store_chunks,search_chunk


def process_pdf(pdf_path,pdf_id):
    text = text_extract_pd(pdf_path)
    chunks = split_text(text)
    store_chunks(pdf_id,chunks)

    return len(chunks)