# =============================================================================
# prompts.py — System Prompt & User Prompt Builder
# =============================================================================
# Contains:
#   SYSTEM_PROMPT   : defines the AI's role, tone, and guardrails
#   build_user_prompt : formats the patient's profile + concern into a prompt
#
# Separating prompts from the API keeps the codebase clean — prompt wording
# can be tuned here without touching the API routing logic.
# =============================================================================

from schema import ChatMessage


# -----------------------------------------------------------------------------
# System Prompt
# -----------------------------------------------------------------------------
# Sent as the "system" role in every conversation.
# Sets the AI persona, scope of advice, and ethical guardrails.

SYSTEM_PROMPT = """You are a professional health advisor AI assistant.
You provide personalized, evidence-based health guidance based on the patient's profile and current concern.
Always be empathetic, clear, and recommend consulting a doctor for medical decisions.
Do not diagnose conditions — only offer general lifestyle and wellness advice."""


# -----------------------------------------------------------------------------
# User Prompt Builder
# -----------------------------------------------------------------------------

def build_user_prompt(data: ChatMessage) -> str:
    """
    Build a structured prompt string from the validated ChatMessage data.

    The LLM receives this as the "user" message. It contains:
        - The patient's profile (demographics + lifestyle)
        - The computed BMI and obesity classification (if available)
        - The patient's written health concern

    Optional fields gracefully fall back to "Not provided" so the LLM
    always receives a complete, readable profile without empty or None values.

    Args:
        data: Validated ChatMessage instance from the POST /chat request body.

    Returns:
        Formatted prompt string ready to send to the LLM.
    """

    # Format BMI line — show value + classification, or indicate it's unavailable.
    bmi_info = f"{data.bmi} ({data.obesity})" if data.bmi is not None else "Not available"

    return f"""Patient Profile:
- Name          : {data.name}
- Age           : {data.age}
- Gender        : {data.gender}
- City          : {data.city or "Not provided"}
- Height        : {f"{data.height} cm" if data.height is not None else "Not provided"}
- Weight        : {f"{data.weight} kg" if data.weight is not None else "Not provided"}
- BMI           : {bmi_info}
- Exercise      : {data.exercise or "Not provided"}
- Sleep         : {f"{data.sleep_hours} hrs/day" if data.sleep_hours is not None else "Not provided"}
- Smoking       : {data.smooking or "Not provided"}

Current concern:
{data.text}

Please provide personalized, practical health advice based on the above profile and concern."""
