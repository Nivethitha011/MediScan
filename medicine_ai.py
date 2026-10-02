import os
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN
)


def analyze_medicine(ocr_text):

    prompt = f"""
You are MediScan, an AI medicine information assistant.

The following text was extracted from a medicine package using OCR.

OCR TEXT:
{ocr_text}

Identify the medicine and provide simple, clear information
that a normal user can understand.

Return ONLY valid JSON in exactly this format:

{{
    "medicine_name": "",
    "ingredients": "",
    "strength": "",
    "uses": [],
    "side_effects": [],
    "precautions": "",
    "food_information": "",
    "health_tip": ""
}}

IMPORTANT RULES:

1. MEDICINE NAME
Identify the medicine/brand name from the OCR text.

2. INGREDIENTS
Identify the active ingredient or composition.

3. STRENGTH
Identify the medicine strength such as 500 mg.

4. USES
Explain what this medicine is commonly used for.
Give 2 or 3 simple points.

5. SIDE EFFECTS
Give common possible side effects associated with
this medicine.

Mention serious side effects only when medically relevant.
Do not exaggerate or invent side effects.

6. PRECAUTIONS
Give important safety precautions for this medicine.
Keep it short and easy to understand.

7. FOOD INFORMATION
If reliable medical knowledge indicates whether the medicine
can be taken with or without food, mention it.

If food information is uncertain, say:
"Check the medicine leaflet or ask a pharmacist."

8. HEALTH TIP
Give ONE short general health tip related to safe medicine use
or general wellness.

Make the health tip different when possible.

9. DOSAGE
Do NOT create or recommend a dosage.

If dosage information appears in the OCR text, do not change it.
However, dosage should NOT be included in the JSON because this
feature is only for medicine information.

10. MEDICAL SAFETY
Do not diagnose the user.
Do not tell the user to start, stop, or change a medicine.
Do not claim that the medicine will cure a disease.
Use phrases such as "commonly used for" where appropriate.

11. UNKNOWN MEDICINE
If the medicine cannot be identified confidently, return:

"medicine_name": "Medicine could not be identified reliably"

and avoid making specific claims about uses or side effects.

12. JSON
Return valid JSON only.
Do not use markdown.
Do not add explanations outside the JSON.

OCR TEXT:
{ocr_text}
"""

    try:

        response = client.chat_completion(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=700
        )

        result = response.choices[0].message.content

        # Remove markdown code blocks if the model adds them
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        return json.loads(result)

    except Exception as e:

        return {
            "medicine_name": "Unable to identify",
            "ingredients": "Not available",
            "strength": "Not available",
            "uses": [],
            "side_effects": [],
            "precautions": "Please check the medicine package or consult a pharmacist.",
            "food_information": "Check the medicine leaflet or ask a pharmacist.",
            "health_tip": "Always verify medicine information before taking it."
        }
