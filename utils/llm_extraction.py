from groq import Groq
def extract_info_from_text(search_results, api_key):
    client = Groq(api_key=api_key)
    info_list = []

    for result in search_results:
        prompt = f"Extract the specific information: {result['snippet']}"
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192" 
        )
        info_list.append(chat_completion.choices[0].message.content.strip())

    return info_list


