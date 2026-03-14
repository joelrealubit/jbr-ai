import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types

from prompts import system_prompt

from call_function import available_functions
from call_function import call_function

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("no api key!")

client = genai.Client(api_key=api_key)


response = client.models.generate_content( 
    model='gemini-2.5-flash', 
    contents=messages, 
    config=types.GenerateContentConfig(tools = [available_functions] ,system_instruction=system_prompt,temperature=0)
    )

if response.usage_metadata == None:
    raise RuntimeError("error getting usage_metadata!")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    

#print(f"Response: ")
#print(response.text)
function_results = []
if response.function_calls != None:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
        function_call_result = call_function(function_call)
        if len(function_call_result.parts) == 0:
            raise RuntimeError("Error: no function call result content parts!\n")
        if function_call_result.parts[0].function_response == None:
            raise RuntimeError("Error: no function response!\n")
        function_results.append(function_call_result.parts[0].function_response)
        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

else:
    print(f"Response: ")
    print(response.text)