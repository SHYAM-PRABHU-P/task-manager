from google import genai

client = genai.Client(api_key="AIzaSyDMjO0OFtf9HTbKvBXDqY-ErokljGxa_NA")

response = client.models.generate_content(
    model="models/gemini-flash-latest",
    contents="Say hello in one line"
)

print(response.text)



