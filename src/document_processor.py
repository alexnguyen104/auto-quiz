import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import Language
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.parsers.pdf import (
   extract_from_images_with_rapidocr,
)
from langchain.schema import Document

# SCANNED PAGES MEAN PAGES WITH NO TEXT CONTENTS.
def process_pdf(source, chunk_size):
    loader = PyPDFLoader(source)
    documents = loader.load()

    # Filter out scanned pages
    unscanned_documents = [doc for doc in documents if doc.page_content.strip() != ""]

    scanned_pages = len(documents) - len(unscanned_documents)
    if scanned_pages > 0:
        logging.info(f"Omitted {scanned_pages} scanned page(s) from the PDF.")

    if not unscanned_documents:
        raise ValueError(
            "All pages in the PDF appear to be scanned. Please use a PDF with text content."
        )

    return split_documents(unscanned_documents, chunk_size)

def process_image(source, chunk_size, num_doc):
    # Extract text from image using OCR
    image_bytes_list = []
    extracted_text = ""

    for i in range(num_doc):
        with open(source[i], "rb") as image_file:
            image_bytes = image_file.read()
            image_bytes_list.append(image_bytes)

    for i in range(num_doc):
        extracted_text += " " + extract_from_images_with_rapidocr([image_bytes_list[i]])

    documents = [Document(page_content=extracted_text)]
    return split_documents(documents, chunk_size)

def split_documents(documents, chunk_size):
    # Split documents into smaller chunks for processing
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=chunk_size, chunk_overlap=chunk_size/5 #these are magic numbers :))
    )
    return text_splitter.split_documents(documents)

def process_document(source, mode, doc_num = 1):
    if(mode == "detailed"): chunk_size = 500
    else: chunk_size = 1000

    # Determine file type and process accordingly
    if source[0].lower().endswith(".pdf"):
        return process_pdf(source[0], chunk_size)
    else:
        return process_image(source, chunk_size, doc_num)
    # elif source[].lower().endswith((".png", ".jpg", ".jpeg")):
    #     return process_image(source, chunk_size, doc_num)
    # else:
    #     raise ValueError(f"Unsupported file type: {source}")
