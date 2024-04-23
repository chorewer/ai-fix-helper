import transformers
from transformers import AutoTokenizer
from typing import Dict, Optional, Sequence,List
import numpy as np
from tqdm import tqdm
from chromadb import Documents, EmbeddingFunction, Embeddings

class ToEmbed(EmbeddingFunction):
    tokenizer: transformers.PreTrainedTokenizer
    
    def __init__(self,tokenizer : transformers.PreTrainedTokenizer):
        self.tokenizer = tokenizer
    
    def __call__(self, textlist : List) -> Embeddings:
        # embed the documents somehow
        result = []
        for it in tqdm(textlist):
            result.append(self.tokenizer(it,return_tensors="pt")["input_ids"].tolist()[0])
        return result
    
    def embed_query(self,textlist : List) -> Embeddings:
        result = []
        for it in tqdm(textlist):
            result.append(self.tokenizer(it,return_tensors="pt")["input_ids"].tolist()[0])
        return result
    def embed_documents(self, textlist : List[str]) -> List[List[float]]:
        result = []
        for it in tqdm(textlist):
            result.append(self.tokenizer(it,return_tensors="pt")["input_ids"].tolist()[0])
        return result
        
        
if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(r"/root/autodl-tmp/chatglm2-6b-int4", trust_remote_code=True)
    embed = ToEmbed(tokenizer=tokenizer)
    strex = ["HEllosc I Will Try this Embeding","HELLO WORLD!"]
    print( embed.embed_query(strex))