import google.genai as genai
from google.genai import types
import os
import sys
import argparse
from dotenv import load_dotenv
from prompts import system_prompt
from functions.call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="?", type=str)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    user_prompt = args.prompt

    if args.prompt is None:
        print("No prompt provided, exiting...")
        sys.exit(1)

    if args.verbose:
        print(f"User prompt: {user_prompt}")


    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]

    for call in range(20):

        response = client.models.generate_content(
            model= 'gemini-2.5-flash', 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], 
                system_instruction=system_prompt, 
                ),  
            )

        usage = response.usage_metadata

        if args.verbose and usage:
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}\n")
            
        if response.candidates:
            for c in response.candidates:
                if c.content:
                    messages.append(c.content)

        if not response.function_calls:
            print(response.text)
            return

        if response.function_calls:
            response_list = []
            
            for function_call in response.function_calls:
                function_result = call_function(function_call, verbose=args.verbose)
                if not function_result.parts[0].function_response:
                    raise Exception("Function response cannot be empty")
                if not function_result.parts or not function_result.parts[0].function_response.response:
                    raise Exception("Content parts list cannot be empty")
                
                response_list.append(function_result.parts[0])
                if args.verbose:
                    print(f"-> {function_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=response_list))

    print("Unable to reach final response within 20 iterations.")
    sys.exit(1)


if __name__ == "__main__":
    main()


