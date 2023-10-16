"""
Do the project from sk microsoft docs
"""
import semantic_kernel as sk
from semantic_kernel.connectors.ai.hugging_face import HuggingFaceTextCompletion
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion
from semantic_kernel.core_skills import ConversationSummarySkill

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

    # create a new context and set the variables
    variables = sk.ContextVariables()
    variables["input"] = "Yes"
    variables[
        "history"
    ] = """Bot: How can I help you?
    User: What's the weather like today?
    Bot: Where are you located?
    User: I'm in Seattle.
    Bot: It's 70 degrees and sunny in Seattle today.
    User: Thanks! I'll wear shorts.
    Bot: You're welcome.
    User: Could you remind me what I have on my calendar today?
    Bot: You have a meeting with your team at 2:00 PM.
    User: Oh right! My team just hit a major milestone; I should send them an email to congratulate them.
    Bot: Would you like to write one for you?"""
    variables["options"] = "SendEmail, ReadEmail, SendMeeting, RsvpToMeeting, SendChat"
    # import the orchestratorplugin from the plugins directory
    orchestrator_plugin = kernel.import_semantic_skill_from_directory(
       plugins_directory, "orchestratorPlugin"
    )

    conversation_summary_plugin = kernel.import_skill(
        ConversationSummarySkill(kernel = kernel),
        skill_name="ConversationSummarySkill"
    )

    # Run the GetIntent function with the context
    result = await kernel.run_async(
        orchestrator_plugin["GetIntent"],
        input_vars=variables,
    )
    
    print(result)

# run the main function
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

# must be on a paid version of openai
