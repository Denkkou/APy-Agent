import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.file_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.file_write import schema_write_file
from functions.file_contents import schema_get_file_content

from functions.file_info import get_files_info
from functions.file_contents import get_file_content 
from functions.file_write import write_file
from functions.run_python import run_python_file

from functions.prompts import *

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Prompt
    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
    else:
        print("Error, no prompt argument given")
        return 1

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    # Lane Wagner's solution (I am really struggling to get this to work)
    iters = 0
    while True:
        iters += 1
        if iters > 20:
            print(f"Maximum iterations ({20}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, True)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")



def generate_content(client, messages, verbose):
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_run_python_file,
            schema_write_file,
            schema_get_file_content
        ]
    )

    response = client.models.generate_content(
    model="gemini-2.0-flash-001", 
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
        )
    )

    if verbose == True:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    # Also Lane Wagner's solution (Still really struggling!!!!)
    if response.candidates:
            for candidate in response.candidates:
                function_call_content = candidate.content
                messages.append(function_call_content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
             or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])

        if not function_responses:
            raise Exception("no function responses generated, exiting.")

        messages.append(types.Content(role="tool", parts=function_responses))



def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f" - Calling function: '{function_call_part.name}'({function_call_part.args})")
    else:
        print(f" - Calling function: '{function_call_part.name}'")
    
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }        

    function_name = function_call_part.name

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call_part.args)
    args.update({"working_directory": "./calculator"})

    function_result = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

       

if __name__ == "__main__":
    main()