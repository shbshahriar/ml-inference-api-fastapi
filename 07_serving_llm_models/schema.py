from pydantic import BaseModel, Field, computed_field
from typing import Optional, Annotated,Literal
from utils import calculate_bmi, calculate_obesity

class ChatMessage(BaseModel):

    name: Annotated[str, Field(..., description="The name of the person sending the message", max_length=50 , min_length=5,json_schema_extra={"example": "Alice"})]

    age: Annotated[int, Field(description="The age of the person sending the message", ge=0, le=120, json_schema_extra={"example": 30})]

    gender: Annotated[Literal["male", "female"], Field(description="The gender of the person sending the message", json_schema_extra={"example": "male"})]

    city: Annotated[Optional[str], Field(description="The city where the person is located", max_length=100, json_schema_extra={"example": "New York"})]

    height: Annotated[Optional[float], Field(description="The height of the person in centimeters", ge=0, le=300, json_schema_extra={"example": 175.5})]

    weight: Annotated[Optional[float], Field(description="The weight of the person in kilograms", ge=0, le=500, json_schema_extra={"example": 70.2})]

    message: Annotated[str, Field(..., description="The message content", max_length=500, min_length=10, json_schema_extra={"example": "Hello, how are you?"})]

    exercise: Annotated[Literal["none", "light", "moderate", "heavy"], Field(description="The level of exercise the person does", json_schema_extra={"example": "moderate"})]

    sleep_hours: Annotated[Optional[float], Field(description="The number of hours the person sleeps per day", ge=0, le=24, json_schema_extra={"example": 7.5})]

    smooking: Annotated[Literal["yes", "no"], Field(description="Whether the person smokes or not", json_schema_extra={"example": "no"})]

    text: Annotated[str, Field(..., description="Current concern of the patient", max_length=1000, min_length=10, json_schema_extra={"example": "This is a sample message for testing the schema validation."})]

    @computed_field
    @property
    def bmi(self) -> float:
        return calculate_bmi(self.weight, self.height)

    @computed_field
    @property
    def obesity(self) -> str:
        return calculate_obesity(self.bmi)
