import google.generativeai as genai

genai.configure(api_key="AIzaSyDwWXPiINhDitLRH8_9_GAvuvTFN9ryj_I")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)
