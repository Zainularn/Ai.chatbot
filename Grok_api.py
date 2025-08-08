from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"  # Only this line added!
)
command = '''
[8:35 pm, 01/08/2025] +91 88106 55864: Gym
[10:55 pm, 05/08/2025] Zain: Bta de bhai aayega ya nii
[10:59 pm, 05/08/2025] +91 88106 55864: Zada raat hori nhi aa sakta
[11:00 pm, 05/08/2025] Zain: Dekhleta bhai koi nii









'''
response = client.chat.completions.create(
    model="llama3-70b-8192",  # Just change the model name
    messages=[
        {"role": "system", "content": "You are a person named zainul who speaks hindi and english . he is from India and is a student.you analyze chat history and respond like zainul"},
        {"role": "user", "content": command}
        
        
        
        
        ]  # Everything else stays the same!
)

print(response.choices[0].message.content)