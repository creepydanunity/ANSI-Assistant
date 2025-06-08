import requests

response = requests.post("http://localhost:8000/ask", json={
    "text": "please i need to fetch pferdlexxie/CharCreate_GenAI"
})

print("✅ Status:", response.status_code)
print("📦 Response:", response.json())
