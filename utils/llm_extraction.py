from groq import Groq
from config import  GROQ_API_KEY
def extract_info_from_text(search_results, api_key):
    client = Groq(api_key="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")
    info_list = []

    for result in search_results:
        print("Processing result:", result)  
        
        if 'snippet' in result:
            prompt = f"Extract the specific information: {result['snippet']}"
        else:
            print("Warning: 'snippet' key not found in result. Skipping this result.")
            continue  
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192" 
        )
        info_list.append(chat_completion.choices[0].message.content.strip())

    return info_list