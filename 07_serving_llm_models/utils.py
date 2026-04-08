def calculate_bmi(weight, height):
    if weight is None or height is None or height == 0:
        return None
    return round(weight / (height / 100) ** 2, 2)

def calculate_obesity(bmi):
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