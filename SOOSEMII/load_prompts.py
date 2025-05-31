import yaml
import numpy as np
from langchain_core.example_selectors.base import BaseExampleSelector
from langchain_core.prompts import loading
from langchain_core.prompts.base import BasePromptTemplate
from langchain_core.prompts import ChatPromptTemplate



# def load_prompt(file_path, encoding="utf8") :
#     with open(file_path, "r", encoding=encoding) as f:
#         config = yaml.safe_load(f)

#     return ChatPromptTemplate.from_messages(config["messages"])

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate

def load_prompt(file_path, encoding="utf-8"):
    with open(file_path, "r", encoding=encoding) as file:
        config = yaml.safe_load(file)
    
    messages = []
    for message in config["messages"]:
        if message["role"] == "system":
            messages.append(SystemMessagePromptTemplate.from_template(message["content"]))
        elif message["role"] == "human":
            messages.append(HumanMessagePromptTemplate.from_template(message["content"]))
        elif message["role"] == "ai":
            messages.append(AIMessagePromptTemplate.from_template(message["content"]))
    
    return ChatPromptTemplate.from_messages(messages)
