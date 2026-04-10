import argparse
import json

from pydantic import BaseModel

from client import DEFAULT_MODEL, get_openai_client
from tools import AVAILABLE_TOOLS, TOOL_FUNCTIONS


MAX_TURNS = 5


class ChatRequest(BaseModel):
    model: str = DEFAULT_MODEL
    message: str


class ChatResponse(BaseModel):
    model: str
    response: str


def run_agent_loop(request: ChatRequest) -> ChatResponse:
    """
    Core agent loop:
    pass the message to the model, let it decide tool calls automatically,
    and keep looping until a final answer appears or max turns is reached.
    """
    if not request.message:
        raise ValueError("message cannot be empty")

    client = get_openai_client()
    messages = [{"role": "user", "content": request.message}]

    print(f"[Agent] Starting agent loop with model: {request.model}")
    print(f"[Agent] User message: {request.message}")

    for turn in range(MAX_TURNS):
        print(f"[Agent] Turn {turn + 1}/{MAX_TURNS}")

        response = client.chat.completions.create(
            model=request.model,
            messages=messages,
            tools=AVAILABLE_TOOLS,
            tool_choice="auto",
            max_tokens=1024,
        )

        message = response.choices[0].message

        if message.tool_calls:
            messages.append(
                {
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in message.tool_calls
                    ],
                }
            )

            for tc in message.tool_calls:
                tool_name = tc.function.name
                tool_args = json.loads(tc.function.arguments)

                print(f"[Agent] Decided to call tool: '{tool_name}'")
                print(f"[Agent] Tool arguments: {tool_args}")

                if tool_name in TOOL_FUNCTIONS:
                    tool_result = TOOL_FUNCTIONS[tool_name](**tool_args)
                    result_str = json.dumps(tool_result, indent=2)
                    if len(result_str) > 500:
                        result_str = result_str[:500] + "..."
                    print(f"[System] Tool Output: '{result_str}'")
                else:
                    tool_result = {"error": f"Unknown tool: {tool_name}"}
                    print(f"[System] Tool Error: Unknown tool '{tool_name}'")

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": json.dumps(tool_result),
                    }
                )

            continue

        content = message.content or "No response"
        print(f"[Agent] Final Answer: '{content[:200]}...'")
        return ChatResponse(model=request.model, response=content)

    print(f"[Agent] Max turns ({MAX_TURNS}) reached without final answer")
    raise RuntimeError(
        f"Agent loop exceeded max turns ({MAX_TURNS}) without producing a final answer"
    )


def chat(request: ChatRequest) -> ChatResponse:
    """
    Compatibility wrapper kept for other projects that import `chat()` directly.
    """
    return run_agent_loop(request)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the core agent loop once.")
    parser.add_argument("message", help="User message passed into the agent loop.")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model id to use. Defaults to {DEFAULT_MODEL}.",
    )
    args = parser.parse_args()

    response = run_agent_loop(ChatRequest(model=args.model, message=args.message))
    print(response.response)


if __name__ == "__main__":
    main()
