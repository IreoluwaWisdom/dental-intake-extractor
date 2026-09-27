import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError, Field
import json

load_dotenv()

client = OpenAI(
    api_key = os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

class Symptoms(BaseModel):
    swelling: bool | None = None
    bleeding: bool | None = None
    fever: bool | None = None


class PatientIntake(BaseModel):
    complaint: str = Field(min_length=1)
    duration_days: int | None = None
    symptoms: Symptoms | None = None

patient =  PatientIntake(
    complaint="severe tooth pain",
    duration_days=3,
    symptoms={
        "swelling": True,
        "bleeding": True,
        "fever": None
    }
)

# print(patient)

# patient_description = """
# My tooth has been hurting badly for about three days.
# My cheek is swollen and it bleeds sometimes when I brush.
# I don't think I have a fever.
# """

patient_description = input("What is the issue you have: ")

print(patient_description)


response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages = [
        {
    "role": "system",
    "content": """
Extract information from the dental patient's description.

Return ONLY valid JSON using exactly this structure:

{
    "complaint": "string",
    "duration_days": integer or null,
    "symptoms": {
        "swelling": true, false, or null,
        "bleeding": true, false, or null,
        "fever": true, false, or null
    }
}

Do not invent information that the patient did not provide.
"""
},
        {
            "role": "user",
            "content": patient_description
        }
    ]
)

# print(response.choices[0].message.content)

llm_output = response.choices[0].message.content

# llm_output = "This is not JSON"

# data["duration_days"] = "three bananas"

try:
    data = json.loads(llm_output)

    patient_intake = PatientIntake.model_validate(data)
    print(patient_intake)

except json.JSONDecodeError as error:
    print("The AI returned invalid JSON")
    print(error)

except ValidationError as error:
    print("The AI output did not match the PatientIntake structure.")
    print(error)

# print(data)

# print(type(llm_output))
# print(type(data))

# print(data["duration_days"])