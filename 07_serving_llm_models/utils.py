# =============================================================================
# utils.py — BMI & Obesity Helper Functions
# =============================================================================
# Pure utility functions shared across schema.py and the API layer.
# Kept separate so they can be tested or reused independently.
# =============================================================================


def calculate_bmi(weight: float | None, height: float | None) -> float | None:
    """
    Calculate Body Mass Index (BMI) from weight and height.

    Formula: weight (kg) / (height (m))²
    Height is stored in cm, so it is divided by 100 before squaring.

    Returns None if either value is missing or height is 0 (avoid ZeroDivisionError).

    Args:
        weight: Body weight in kilograms.
        height: Body height in centimeters.

    Returns:
        Rounded BMI as a float, or None if inputs are incomplete.
    """
    if weight is None or height is None or height == 0:
        return None

    # Convert height from cm → m, then apply the BMI formula.
    return round(weight / (height / 100) ** 2, 2)


def calculate_obesity(bmi: float | None) -> str | None:
    """
    Classify BMI into a WHO obesity category.

    WHO classification:
        < 18.5  → Underweight
        18.5–24.9 → Normal weight
        25–29.9 → Overweight
        ≥ 30    → Obese

    Args:
        bmi: Calculated BMI value, or None if BMI could not be computed.

    Returns:
        Obesity category as a string, or None if BMI is unavailable.
    """
    if bmi is None:
        return None

    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"
