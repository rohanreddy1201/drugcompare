# app/model/explain.py

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"  # Or another local model you've pulled


def generate_explanation(drug1: str, drug2: str, comparison_data: dict) -> str:
    # Build detailed context for the prompt from comparison
    comparison_text = f"Compare the following two medications: {drug1} and {drug2}.\n\n"
    comparison_text += "Here are their attributes:\n\n"

    for field, values in comparison_data.items():
        field_name = field.replace("_", " ").title()
        val1 = values["drug1"] or "No data available"
        val2 = values["drug2"] or "No data available"

        comparison_text += f"🔹 {field_name}:\n- {drug1}: {val1}\n- {drug2}: {val2}\n\n"

    comparison_text += (
        "Now, based on the above data, generate a clear, concise medical summary comparing these two drugs. "
        "Explain their uses, differences, safety notes, and any meaningful insights that could help a healthcare provider or informed patient choose between them."
    )

    try:
        res = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": comparison_text, "stream": False},
            timeout=300  # You can increase if needed
        )
        res.raise_for_status()
        return res.json().get("response", "").strip()

    except Exception as e:
        return f"⚠️ Explanation failed: {str(e)}"
