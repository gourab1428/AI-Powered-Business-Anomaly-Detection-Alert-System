import os
import requests


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ API key not found")
    exit()


url = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-3.6-flash:generateContent"
)


headers = {
    "x-goog-api-key": API_KEY,
    "Content-Type": "application/json"
}


body = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Say hello in one sentence."
                }
            ]
        }
    ]
}


print("🔑 API key found")
print("📡 Sending request...")


try:

    response = requests.post(
        url,
        headers=headers,
        json=body,
        timeout=30
    )

    print("HTTP STATUS:", response.status_code)


    if response.status_code != 200:

        print("❌ API ERROR:")
        print(response.text)

    else:

        print("✅ Gemini API responded!")

        result = response.json()

        print("\nRAW RESPONSE:")
        print(result)


except requests.exceptions.Timeout:

    print("❌ Request timed out.")


except Exception as e:

    print("❌ Error:", e)