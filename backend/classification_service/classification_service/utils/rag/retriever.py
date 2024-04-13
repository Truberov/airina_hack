import chromadb
from chromadb.config import Settings

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI

from procure_base_ai.config import get_settings
from .splitter import text_splitter

settings = get_settings()

chroma_client = chromadb.HttpClient(
    settings=Settings(
        chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
        chroma_client_auth_credentials=settings.CHROMA_TOKEN
    ),
    host=settings.CHROMA_HOST,
    port=settings.CHROMA_PORT,
)

remote_retriever = Chroma(
    embedding_function=OpenAIEmbeddings(),
    client=chroma_client,
    collection_name='44fz-collection'
).as_retriever()

others_44_retriever = Chroma(
    embedding_function=OpenAIEmbeddings(),
    client=chroma_client,
    collection_name='total'
).as_retriever(search_kwargs={"k": 5, "filter": {"fz": "44"}})

others_223_retriever = Chroma(
    embedding_function=OpenAIEmbeddings(),
    client=chroma_client,
    collection_name='total'
).as_retriever(search_kwargs={"k": 5, "filter": {"fz": "223"}})

terms_retriever = Chroma(
    embedding_function=OpenAIEmbeddings(),
    client=chroma_client,
    collection_name='terms'
).as_retriever(search_kwargs={"k": 5})

from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import LocalFileStore, create_kv_docstore

store = LocalFileStore('procure_base_ai/local_store_44')

llm = ChatOpenAI(model='gpt-3.5-turbo-16k')

store = create_kv_docstore(store)

parent_law_44_retriever = ParentDocumentRetriever(
    docstore=store,
    vectorstore=Chroma(
        embedding_function=OpenAIEmbeddings(),
        client=chroma_client,
        collection_name='44-law'),
    child_splitter=text_splitter,
)

from langchain.retrievers.multi_query import MultiQueryRetriever

multi_law_44_retriever = MultiQueryRetriever.from_llm(
    retriever=parent_law_44_retriever, llm=llm
)

store = LocalFileStore('procure_base_ai/local_store_223')


store = create_kv_docstore(store)

law_223_retriever = ParentDocumentRetriever(
    docstore=store,
    vectorstore=Chroma(
        embedding_function=OpenAIEmbeddings(),
        client=chroma_client,
        collection_name='223-law'),
    child_splitter=text_splitter,
)


from langchain.retrievers import EnsembleRetriever

total_retriever_44 = EnsembleRetriever(
    retrievers=[multi_law_44_retriever, others_44_retriever], weights=[0.5, 0.5]
)


from langchain.retrievers import EnsembleRetriever

total_retriever_223 = EnsembleRetriever(
    retrievers=[law_223_retriever, others_223_retriever], weights=[0.5, 0.5]
)

instructions_retriever = Chroma(
    embedding_function=OpenAIEmbeddings(),
    client=chroma_client,
    collection_name='instructions'
).as_retriever(search_kwargs={"k": 5})
