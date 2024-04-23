import chromadb as cdb
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import VectorDBQA
from langchain.chains import LLMChain
from langchain_community.llms import ChatGLM
from langchain_core.prompts import PromptTemplate


persist_directory = "/root/autodl-tmp/persistentDB"

embedding_model_name = r'/root/autodl-tmp/bce-embedding-base_v1'
embedding_model_kwargs = {'device': 'cuda:0'}
embedding_encode_kwargs = {'batch_size': 32, 'normalize_embeddings': True}

embedding = HuggingFaceEmbeddings(
    model_name=embedding_model_name,
    model_kwargs=embedding_model_kwargs,
    encode_kwargs=embedding_encode_kwargs
)

vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

endpoint_url = "http://127.0.0.1:8000"
# template = """{question}"""
# prompt = PromptTemplate.from_template(template)
llm = ChatGLM(
    endpoint_url=endpoint_url,
    max_token=80000,
    history=[
    ],
    top_p=0.9,
    model_kwargs={"sample_model_args": False},
)

qa = VectorDBQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=vectordb)

query = "How Can I D-Link HD Wi-Fi Camera Troubleshooting"
result = qa.run(query)
print(result)