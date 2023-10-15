# Configure your local machine to run Semantic Kernel
import semantic_kernel as sk
from semantic_kernel.connectors.ai.hugging_face import HuggingFaceTextCompletion
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion
"""
    kernel is for managing resoruces that necessary to run code in 
    ai application
    resoruce: confguration, services and pugins 
"""
# import openai
# import os
# openai.api_key = os.getenv("OPENAI_API_KEY")
# print(openai.api_key)
kernel = sk.Kernel()

useAzureOpenAI = False

if useAzureOpenAI:
    deployment, api, endpoint = sk.azure_openai_settings_from_dot_env()
    kernel.add_text_completion_service("azureioenai", AzureChatCompletion)
else:
    api_key, org_id = sk.openai_settings_from_dot_env()
    kernel.add_text_completion_service("openai", OpenAIChatCompletion("gpt-3.5-turbo-0301", api_key, org_id))
print("you made a kernel!")


"""for hugging face need torch and transformers
    """
# get semantic kernel from hugging face
kernel.add_text_completion_service("huggingface", HuggingFaceTextCompletion("gpt2"),task="text-generation")
print("you made a kernel for hugging faces!")