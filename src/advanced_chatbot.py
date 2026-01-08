import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from src.faq_data import loan_faq_response

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

SYSTEM_PROMPT = """You are a professional financial advisor chatbot.
You ONLY answer questions related to:
- Loans and banking
- Credit score and EMI
- Personal finance
- Investments and savings
- Taxes and insurance

If the user asks anything outside finance, politely refuse.
Be accurate, safe, and explain clearly.
"""

client = InferenceClient(token=HF_API_TOKEN)

def financial_chatbot(user_message, conversation_history):
    """
    Hybrid chatbot:
    1. FAQ-based response first
    2. LLM fallback for complex queries
    """

    # 1️⃣ Try FAQ (fast & deterministic)
    faq_reply = loan_faq_response(user_message)
    if faq_reply:
        return faq_reply, conversation_history

    # 2️⃣ LLM fallback
    try:
        if len(conversation_history) == 0:
            conversation_history.append(
                {"role": "system", "content": SYSTEM_PROMPT}
            )

        conversation_history.append(
            {"role": "user", "content": user_message}
        )

        response = client.chat_completion(
            model="meta-llama/Llama-3.2-3B-Instruct",
            messages=conversation_history,
            max_tokens=400,
            temperature=0.6
        )

        bot_reply = response.choices[0].message.content
        conversation_history.append(
            {"role": "assistant", "content": bot_reply}
        )

        return bot_reply, conversation_history

    except Exception as e:
        return "⚠️ Sorry, the chatbot is temporarily unavailable.", conversation_history
