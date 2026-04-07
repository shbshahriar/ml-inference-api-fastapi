def calculate_bmi(weight, height):
    return round(weight / (height / 100) ** 2, 2)

def calculate_obesity(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"