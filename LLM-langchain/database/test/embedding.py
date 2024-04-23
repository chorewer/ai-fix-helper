from transfomers import AutoTokenizer
from chromadb import Documents, EmbeddingFunction, Embeddings

class MyEmbeddingFunction(EmbeddingFunction):
    tokenizer: transformers.PreTrainedTokenizer,
    
    def __call__(self, input: Documents) -> Embeddings:
        # embed the documents somehow
        
        
        
        return embeddings