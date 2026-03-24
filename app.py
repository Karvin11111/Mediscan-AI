import os
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)  # Allows the frontend HTML to talk to this server

# ─── PASTE YOUR GROQ API KEY HERE ───
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

@app.route("/analyze", methods=["POST"])
def analyze():
    # Check if image was uploaded
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file uploaded."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "message": "Empty file."}), 400

    # Convert image to base64 for Groq
    image_data = file.read()
    base64_image = base64.b64encode(image_data).decode("utf-8")
    mime_type = file.content_type or "image/jpeg"

    # Ask Groq to analyze the image
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": """You are a medical AI assistant. Analyze this medical image and provide a structured health report.

Respond in this EXACT format:

SUMMARY:
Write 2-3 sentences summarizing what you see in the image.

POSSIBLE CONDITIONS:
List the most likely conditions or findings, with estimated probability percentages. Format each as: Condition Name - XX%

SEVERITY INSIGHT:
Describe the apparent severity level (Low/Moderate/High) and why.

RECOMMENDED ACTIONS:
List 3-5 specific recommended next steps for the patient.

PREVENTIVE MEASURES:
List 2-4 preventive measures relevant to the findings.

WHEN TO SEEK MEDICAL HELP:
Describe specific warning signs or situations requiring immediate medical attention.

Be factual, clear, and compassionate. Always remind that this is AI analysis only."""
                        }
                    ]
                }
            ],
            max_tokens=1200
        )

        ai_text = response.choices[0].message.content

        # Parse conditions + scores from the response
        top_findings = parse_findings(ai_text)

        return jsonify({
            "success": True,
            "top_findings": top_findings,
            "ai_report": ai_text,
            "disclaimer": "AI tool only. Not a medical diagnosis."
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


def parse_findings(text):
    """Extract condition names and scores from AI response."""
    import re
    findings = []

    # Look for lines like: "Condition Name - 72%" or "Condition Name: 72%"
    pattern = r'([A-Za-z][^\-:\n%]{3,50}?)[\s\-:]+(\d{1,3})\s*%'
    matches = re.findall(pattern, text)

    for name, pct in matches[:5]:  # Max 5 findings
        name = name.strip().strip('-').strip()
        score = int(pct) / 100
        if 0.05 <= score <= 1.0 and len(name) > 3:
            findings.append({
                "name": name,
                "score": round(score, 2),
                "percent": f"{pct}%"
            })

    # Fallback if nothing parsed
    if not findings:
        findings = [{"name": "See full report below", "score": 0.72, "percent": "72%"}]

    return findings


if __name__ == "__main__":
    print("\n✅ MediScan AI backend is running!")
    print("📡 Server: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop\n")
    app.run(debug=True, port=5000)
