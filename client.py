import asyncio
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from mcp import Client, StdioServerParameters


load_dotenv()


async def main():
    # Connect to MCP server
    server = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with Client(server) as mcp_client:

        # Discover all MCP tools
        result = await mcp_client.list_tools()

        print("MCP server connected!")
        print("\nAvailable tools:")

        for tool in result.tools:
            print(f"- {tool.name}")

        # Convert MCP tools to Gemini function declarations
        function_declarations = []

        for tool in result.tools:
            function_declarations.append(
                {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema,
                }
            )

        gemini_tool = types.Tool(
            function_declarations=function_declarations
        )

        # Connect to Gemini
        gemini = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        print("\nAI Notes Assistant is ready!")
        print("Type 'exit' to quit.\n")

        while True:
            user_input = input("You: ")

            if user_input.lower() == "exit":
                break

            # Ask Gemini what to do
            response = gemini.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input,
                config=types.GenerateContentConfig(
                    tools=[gemini_tool],
                ),
            )

            # Check whether Gemini wants to use a tool
            if response.function_calls:

                function_call = response.function_calls[0]

                print(
                    f"\nGemini is calling: {function_call.name}"
                )
                print(
                    f"Arguments: {function_call.args}"
                )

                # Execute the MCP tool
                tool_result = await mcp_client.call_tool(
                    function_call.name,
                    function_call.args,
                )

                # Collect ALL returned content
                result_text = "\n".join(
                    item.text
                    for item in tool_result.content
                )

                print(f"MCP result: {result_text}")

                # Send MCP result back to Gemini
                final_response = gemini.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        user_input,
                        response.candidates[0].content,
                        types.Content(
                            role="tool",
                            parts=[
                                types.Part.from_function_response(
                                    name=function_call.name,
                                    response={
                                        "result": result_text
                                    },
                                )
                            ],
                        ),
                    ],
                    config=types.GenerateContentConfig(
                        tools=[gemini_tool],
                    ),
                )

                print(
                    f"\nAssistant: {final_response.text}\n"
                )

            else:
                print(
                    f"\nAssistant: {response.text}\n"
                )


if __name__ == "__main__":
    asyncio.run(main())