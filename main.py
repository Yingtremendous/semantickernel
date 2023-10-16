import semantic_kernel as sk
from semantic_kernel.connectors.ai.hugging_face import HuggingFaceTextCompletion
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion

async def main():
    # initialize kernel
    kernel = sk.Kernel()
    useAzureOpenAI = False

    if useAzureOpenAI:
        deployment, api, endpoint = sk.azure_openai_settings_from_dot_env()
        kernel.add_text_completion_service("azureioenai", AzureChatCompletion)
    else:
        api_key, org_id = sk.openai_settings_from_dot_env()
        kernel.add_text_completion_service("openai", OpenAIChatCompletion("gpt-3.5-turbo-0301", api_key, org_id))
    print("you made a kernel!")

    plugins_directory = "./Plugins"

    # import the orchestratorplugin from the plugins directory
    orchestrator_plugin = kernel.import_semantic_skill_from_directory(
       plugins_directory, "orchestratorPlugin"
    )

    # Run the GetIntent function with the context
    result = await kernel.run_async(
        orchestrator_plugin["GetIntent"],
        input_str="I want to send an email to the marketing team celebrating their recent milestone.")
    
    print(result)

# run the main function
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

# must be on a paid version of openai
