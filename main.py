import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    prompt = ""

    if sys.argv[1] != None:
        prompt = sys.argv[1]
    else:
        print("Error, no prompt argument given")
        return 1

    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt)
        
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    

if __name__ == "__main__":
    main()
