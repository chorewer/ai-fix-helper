from langchain.chains import LLMChain
from langchain_community.llms import ChatGLM
from langchain_core.prompts import PromptTemplate

# import os

template = """{question}"""
prompt = PromptTemplate.from_template(template)

# default endpoint_url for a local deployed ChatGLM api server
endpoint_url = "http://127.0.0.1:8000"

# direct access endpoint in a proxied environment
# os.environ['NO_PROXY'] = '127.0.0.1'

llm = ChatGLM(
    endpoint_url=endpoint_url,
    max_token=80000,
    history=[
    ],
    top_p=0.9,
    model_kwargs={"sample_model_args": False},
)

# turn on with_history only when you want the LLM object to keep track of the conversation history
# and send the accumulated context to the backend model api, which make it stateful. By default it is stateless.
# llm.with_history = True

llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "My Dell Inspiron 13 7368's battery is not working, can you help me replace it?"

response = llm_chain.run(question)

print(response)