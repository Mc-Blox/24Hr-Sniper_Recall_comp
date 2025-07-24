from openai import OpenAI
import json
from recall_tool import recall_trade_tool

client = OpenAI(base_url="https://qwen72b.gaia.domains/v1", api_key="YOUR_GAIA_API_KEY") # You won't need an API Key if you're running a local node. This example is with one of our Public Nodes

def run_trade_conversation():
    # Step 1: Define the user message and available tool
    messages = [{
        "role": "user",
        "content": "Swap 100 USDC to WETH on Ethereum mainnet to verify my Recall account"
    }]
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "recall_trade_tool",
                "description": "Executes a token trade using the Recall API on Ethereum Mainnet",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fromToken": {
                            "type": "string",
                            "description": "ERC-20 token address to trade from"
                        },
                        "toToken": {
                            "type": "string",
                            "description": "ERC-20 token address to trade to"
                        },
                        "amount": {
                            "type": "string",
                            "description": "Amount of the fromToken to trade"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for making the trade"
                        }
                    },
                    "required": ["fromToken", "toToken", "amount", "reason"]
                }
            }
        }
    ]

    response = client.chat.completions.create(
        model="Qwen3-235B-A22B-Q4_K_M",  # Replace with your Gaia model name
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "recall_trade_tool": recall_trade_tool
        }

        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            function_response = function_to_call(
                fromToken=function_args["fromToken"],
                toToken=function_args["toToken"],
                amount=function_args["amount"],
                reason=function_args["reason"]
            )

            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(function_response)
            })

        second_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )

        return second_response

if __name__ == "__main__":
    result = run_trade_conversation()
    print(result.choices[0].message.content)


