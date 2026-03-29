import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 👉 Replace with your Groq API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 🔹 Fake Order Database
orders = {
    "DH1234": {"status": "Shipped", "delivery": "2 April"},
    "DH5678": {"status": "Processing", "delivery": "5 April"}
}

# 🔹 Intent + Order ID Detection
def detect_intent(message):
    prompt = f"""
    You are an API. Return ONLY valid JSON.

    Extract:
    - intent (order_tracking, return, general)
    - order_id (if present)

    Message: {message}

    Strict JSON format:
    {{
      "intent": "",
      "order_id": ""
    }}

    Do NOT add explanation.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content

    # 🔥 Safe JSON extraction
    start = text.find("{")
    end = text.rfind("}") + 1

    if start == -1 or end == -1:
        return {"intent": "general", "order_id": ""}

    json_str = text[start:end]

    try:
        return json.loads(json_str)
    except:
        return {"intent": "general", "order_id": ""}


# 🔹 Reply Generator
def generate_reply(intent, order_id, message):
    if intent == "order_tracking":
        if order_id in orders:
            data = orders[order_id]
            return f"Hey! Your order {order_id} is {data['status']} 🚚 and will reach you by {data['delivery']}."
        else:
            return "Sorry, I couldn’t find your order. Please check your order ID."

    elif intent == "return":
        return "You can initiate a return within 7 days from delivery. Let me know if you need help!"

    else:
        return "Thanks for reaching out! Our team will assist you shortly 😊"


# 🔹 Main Loop (simulate chat)
while True:
    user_input = input("\nEnter customer message: ")

    result = detect_intent(user_input)
    intent = result.get("intent")
    order_id = result.get("order_id")

    reply = generate_reply(intent, order_id, user_input)

    print("Bot:", reply)