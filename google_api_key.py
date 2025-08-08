import google.generativeai as genai

# Replace with your actual API key
genai.configure(api_key="AIzaSyDJN7HpPbBBY6eGXpYVYktAdjKXo5LnOh0")

# ✅ Specify model from v1
model = genai.GenerativeModel(model_name="models/gemini-pro")  # fully qualified name

# Use the model
response = model.generate_content("Give me a motivational quote in Hindi")

print(response.text)
