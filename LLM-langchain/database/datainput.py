import sys;
sys.path.append(r"/root/autodl-tmp/fix-helper/LLM-langchain/database/textspliter")
import stdspliter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

if __name__ == "__main__":
    print("Begin work!")
    
    database_src = r"/root/autodl-tmp/persistentDB"
    
    
    # embed = ToEmbed(tokenizer)
    embedding_model_name = r'/root/autodl-tmp/bce-embedding-base_v1'
    embedding_model_kwargs = {'device': 'cuda:0'}
    embedding_encode_kwargs = {'batch_size': 32, 'normalize_embeddings': True, 'show_progress': True}

    embedding = HuggingFaceEmbeddings(
        model_name=embedding_model_name,
        model_kwargs=embedding_model_kwargs,
        encode_kwargs=embedding_encode_kwargs
    )
    print("Init Embedding!")

    persist_path= r"/root/autodl-tmp/persistentDB"
    
    result = stdspliter.HandleAllSplit(chunk_size=1000,chunk_overlap=0)
    
    vectordb = Chroma.from_documents(documents=result, embedding=embedding, persist_directory=persist_path)

    vectordb.persist()
    
    print("Init Client Successfully!")
    
    # collection = client.get_or_create_collection(
    #     name="Fixing_Guide",
    #     metadata={
    #         "hnsw:space": "cosine",
    #     },
    #     embedding_function=embed
    # )
    # ids = []
    # for it in range(len(result)):
    #     ids.append("id"+str(it))
    # collection.add(
    #     documents=result,
    #     ids = ids
    # )
    
    