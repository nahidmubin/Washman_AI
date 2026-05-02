from smolagents import ToolCallingAgent, InferenceClientModel
from smolagents.agents import FinalAnswerStep, ActionStep
from washman_tools import database_search, walton_website_search

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ["HUGGINGFACE_API_KEY"]

model = InferenceClientModel(
    api_key=API_KEY,
    # model_id="moonshotai/Kimi-K2-Thinking",
    # provider="novita",
    # model_id="Qwen/Qwen3-4B-Thinking-2507",
    # provider="nscale",
    # tool_choice = "auto",
    model_id="openai/gpt-oss-120b",
    provider="novita"
)


# init the agent
agent = ToolCallingAgent(
    tools=[database_search, walton_website_search],
    model=model
)

agent.instructions = """
    You are Walton Washman — an AI assistant for Walton washing machines.
    All responses must be in English, clear, friendly, and step-by-step.

    Use the tools from the provided list of tools. Incase no clue from the
    tools list use web search.

    IMPORTANT: You MUST always respond using a valid JSON tool call.
    Never respond with plain text. Always call either a tool or final_answer
    """


def washmans_reply(user_prompt):
    for chunk in agent.run(user_prompt, stream=True):
        if isinstance(chunk, ActionStep):
            reasoning = getattr(chunk.model_output_message.raw.choices[0].message, "reasoning_content", None)
            if reasoning:
                yield f"🤔THINKING:\n{reasoning}\n\n"

        if isinstance(chunk, FinalAnswerStep):
            yield f"💬 Final Answer:\n{chunk.output}"

if __name__ == "__main__":

    user_prompt = input("What's your question? ")
    reply = washmans_reply(user_prompt)

    print("\n\nModel Response:\n")
    for token in reply:
        print(token, end="", flush=True)