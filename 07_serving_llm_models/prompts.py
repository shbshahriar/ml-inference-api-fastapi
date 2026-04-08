from schema import ChatMessage

SYSTEM_PROMPT = """You are a professional health advisor AI assistant.
You provide personalized, evidence-based health guidance based on the patient's profile and current concern.
Always be empathetic, clear, and recommend consulting a doctor for medical decisions.
Do not diagnose conditions — only offer general lifestyle and wellness advice."""


def build_user_prompt(data: ChatMessage) -> str:
    bmi_info = f"{data.bmi} ({data.obesity})" if data.bmi is not None else "Not available"
    return f"""Patient Profile:
- Name: {data.name}
- Age: {data.age}
- Gender: {data.gender}
- City: {data.city or "Not provided"}
- Height: {f"{data.height} cm" if data.height is not None else "Not provided"}
- Weight: {f"{data.weight} kg" if data.weight is not None else "Not provided"}
- BMI: {bmi_info}
- Exercise level: {data.exercise or "Not provided"}
- Sleep hours per day: {data.sleep_hours or "Not provided"}
- Smoking: {data.smooking or "Not provided"}

Current concern: {data.text}

Please provide personalized health advice based on the above profile and concern."""
