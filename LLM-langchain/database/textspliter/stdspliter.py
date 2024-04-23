import os
from langchain.text_splitter import MarkdownTextSplitter
from langchain.document_loaders import TextLoader
from tqdm import tqdm

Guide_src = "/root/autodl-tmp/fix-helper/data/Guide"
Wiki_src = "/root/autodl-tmp/fix-helper/data/Wiki"

class My_MarkDown_Splitter(MarkdownTextSplitter):
    def __init__(self,**kwags):
        super().__init__(**kwags)
    def split(self, documents):
        docsList = self.split_documents(documents)
        # sent_list = [i.page_content for i in docsList if i]
        return docsList

def get_splitted_list(base: str, file: str, Splitter: My_MarkDown_Splitter):
    loader = TextLoader(base + "/" + file)
    doc = loader.load()
    return Splitter.split(documents = doc)
    

def HandleAllSplit(
    chunk_size : int,
    chunk_overlap : int
):
    ListOfGuide = os.listdir(Guide_src)
    ListOfWiki = os.listdir(Wiki_src)
    # print("ListOfGuide:::"+str(ListOfGuide))
    splitter = My_MarkDown_Splitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    result_list = []
    for it in tqdm(ListOfGuide):
        temp_list = get_splitted_list(Guide_src,it,splitter)
        result_list.extend(temp_list)
    for it in tqdm(ListOfWiki):
        temp_list = get_splitted_list(Wiki_src,it,splitter)
        result_list.extend(temp_list)
    return result_list
        
        
if __name__ == "__main__":
    result = HandleAllSplit(chunk_size=1000,chunk_overlap=0)
    # print(result[:5])
