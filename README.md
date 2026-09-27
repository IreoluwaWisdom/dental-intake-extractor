# Dental Intake Extractor

A small AI engineering project that converts a patient's natural-language description of a dental problem into validated, structured intake data.

This project is an early technical experiment for a larger dental patient-flow system. The goal is not to diagnose patients, but to explore how AI can help transform unstructured patient descriptions into structured information that software can safely work with.

## What It Does

A patient can enter a description such as:

```text
My gum dey swell since like two days now and the tooth dey pain me well well
```

The application sends the description to a Large Language Model (LLM), which extracts structured information.

The result is validated with Pydantic:

```text
complaint='gum swelling and tooth pain'
duration_days=2
symptoms=Symptoms(
    swelling=True,
    bleeding=None,
    fever=None
)
```

This allows informal human language to be converted into predictable application data.

## Architecture

```text
Patient description
        ↓
LLM API
        ↓
Structured JSON response
        ↓
JSON parsing
        ↓
Pydantic validation
        ↓
Validated PatientIntake object
```

The LLM handles interpretation of natural language.

Python handles the application logic.

Pydantic acts as a validation boundary before AI-generated data is accepted by the application.

## Data Model

The current intake model contains:

```text
PatientIntake
├── complaint
├── duration_days
└── symptoms
    ├── swelling
    ├── bleeding
    └── fever
```

Unknown information is preserved as `None` rather than automatically being treated as `False`.

For example, if a patient says:

```text
My tooth has been hurting since yesterday.
```

the system can return:

```text
complaint='tooth hurting'
duration_days=1
symptoms=Symptoms(
    swelling=None,
    bleeding=None,
    fever=None
)
```

The patient never mentioned swelling, bleeding, or fever, so the application should not invent those answers.

## Failure Cases I Tested

Building the first version exposed several useful failure cases.

### 1. Uncontrolled LLM Output

The first LLM response was semantically correct but returned its own structure:

```json
{
  "tooth_pain": true,
  "pain_duration": "3 days",
  "cheek_swelling": true
}
```

That may be understandable to a human, but it is unreliable for application code.

The prompt was changed to require a predictable JSON structure that matches the application's data contract.

### 2. Missing Information

The application was tested with complaints that did not mention every symptom.

Instead of inventing answers, missing information is represented as `None`.

### 3. Informal Nigerian English

The extractor was tested with:

```text
My gum dey swell since like two days now and the tooth dey pain me well well
```

The model successfully interpreted the meaning and mapped it into the same structured schema used for standard English input.

### 4. Irrelevant Input

Input such as:

```text
I want to watch football tonight
```

initially resulted in an empty complaint.

Because an empty string is technically still a Python string, basic type validation accepted it.

The schema was strengthened with a Pydantic minimum-length constraint so an empty complaint is rejected.

### 5. Malformed AI Output

The application was deliberately tested with:

```text
This is not JSON
```

This caused `json.loads()` to raise a `JSONDecodeError`.

JSON parsing is now handled safely so malformed model output does not produce an uncontrolled application crash.

## AI Safety Boundary

This project does **not** diagnose dental conditions, prescribe medication, or recommend treatment.

Its current responsibility is limited to:

> Natural-language patient description → structured intake information

Any future clinical use would require appropriate clinical rules, human review, evaluation, privacy safeguards, and hospital-approved workflows.

## Tech Stack

- Python
- Pydantic
- OpenAI Python SDK
- Groq OpenAI-compatible API
- GPT-OSS model
- python-dotenv

## Running Locally

Clone the repository and create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment and install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example`:

```text
GROQ_API_KEY=your_groq_api_key
```

Then run:

```bash
python ai_dental_intake.py
```

The application will ask:

```text
What is the issue you have:
```

Enter a dental complaint and the validated structured result will be displayed.

## Project Status

**v0.1 — Command-line prototype**

Current focus:

- natural-language intake;
- structured LLM output;
- JSON parsing;
- Pydantic validation;
- safe handling of invalid output.

The project intentionally remains small while these foundations are tested before adding a web interface or integrating it into a larger dental patient-flow system.