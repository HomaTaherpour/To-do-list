import openai
import sys
import json



# Set API Key
api_key = "YOURAPIKEY"


client = openai.OpenAI(api_key=api_key)

if len(sys.argv) > 1:
    user_input = sys.argv[1]
else:
    user_input = "Write a simple task-related message."

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_input}],
        max_tokens=80
    )

    print(json.dumps({"response": response.choices[0].message.content}))

except openai.OpenAIError as e:
    print(json.dumps({"response": f"API Connection Failed: {str(e)}"}))
