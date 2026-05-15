from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001"
)


#store chunks 

def store_chunks(pdf_id,chunks):
    vector_store = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=f"./chroma_db/{pdf_id}"
    )


def get_vectorstore(pdf_id):
    return Chroma(
        persist_directory=f"./chroma_db/{pdf_id}",
        embedding_function=embeddings
    )

def search_chunk(pdf_id,question):
    vectorstore =  get_vectorstore(pdf_id)
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    docs = retriever.get_relevant_documents(question)

    return [doc.page_content for doc in docs]