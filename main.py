import os
import argparse
from call_function import available_functions,call_function
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API Key not found")
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="My Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0))

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
            if response.function_calls:
                function_results = []
                for function_call in response.function_calls:
                    print(f"Calling function: {function_call.name}({function_call.args})")
                    function_call_result = call_function(function_call,args.verbose)
                    if function_call_result.parts is None:
                        raise Exception(f"Error: Function call returns no parts")
                    if function_call_result.parts[0].function_response is None:
                        raise Exception(f"Error: No response object in first response part")
                    if function_call_result.parts[0].function_response.response is None:
                        raise Exception(f"Error: No response in response object")
                    function_results.append(function_call_result.parts[0])
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                messages.append(types.Content(role="user", parts=function_results))
            else:
                if args.verbose:
                    print(f"User prompt: {args.user_prompt}")
                    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                print(f"Response:\n {response.text}")
                return

    print("ERROR: Too much iterations, possibly a loop")
    return 1

if __name__ == "__main__":
    main()
