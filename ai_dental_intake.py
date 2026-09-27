import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
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

def extract_patient_intake(patient_description: str):
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

    llm_output = response.choices[0].message.content

    data = json.loads(llm_output)

    return PatientIntake.model_validate(data)


def main():
    patient_description = input("What is the issue you have: ")


    try:
        patient_intake = extract_patient_intake(patient_description)
        print(patient_intake)

    except json.JSONDecodeError as error:
        print("The AI returned invalid JSON")
        print(error)

    except ValidationError as error:
        print("The AI output did not match the PatientIntake structure.")
        print(error)




if __name__ == "__main__":
    main()