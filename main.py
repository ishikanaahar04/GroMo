import re
import unicodedata
from mistralai import Mistral

api_key_mistral = "aKFEMuDwJOvtphHDDOrh2qbfRP7jEA1L"

def clean_message(message):
    # Normalize unicode
    message = unicodedata.normalize('NFKC', message)

    # Remove zero-width and invisible unicode chars
    message = re.sub(r'[\u200B-\u200D\uFEFF]', '', message)

    # Replace non-breaking spaces with normal spaces
    message = message.replace('\u00A0', ' ')

    # Normalize line breaks
    lines = message.splitlines()
    cleaned_lines = []
    for i, line in enumerate(lines):
        line = re.sub(r'[ \t]+', ' ', line)
        line = re.sub(r'\s+([.,!?])', r'\1', line)
        line = re.sub(r'\s+([📈📊📱📉📌🔒💸🙏])', r'\1', line)
        line = line.strip()

        if line.startswith("-"):
            # Ensure a blank line before first bullet point
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")
            cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)

    # Rebuild cleaned message
    cleaned_text = []
    prev_line = ""
    for line in cleaned_lines:
        if line == "" and prev_line == "":
            continue
        cleaned_text.append(line)
        prev_line = line

    final_text = "\n".join(cleaned_text)

    # Ensure one blank line before GP name (ends with comma)
    final_text = re.sub(r"(?<!\n)\n([^\n]+,)\n(GroMo Team)", r"\n\n\1\n\2", final_text)

    # Ensure exactly one blank line before Apply Now
    final_text = re.sub(r"\n{2,}Apply Now", r"\n\nApply Now", final_text)

    return final_text.strip()

def generate_message(name, profession, interest, service, language, gp_name):
    model = "mistral-large-latest"

    prompt = (
        f"You are a creative, fluent copywriter writing on behalf of a GroMo Partner named {gp_name}.\n"
        f"The message should be written as if it's coming from ONE PERSON (the GP), not a company.\n"
        f"Tone should be polite, warm, respectful, and in fluent {language}.\n"
        f"Focus on customer benefit. Avoid clichés or generic references to interest unless very relevant.\n\n"

        f"Customer Name: {name}\n"
        f"Customer Profession: {profession}\n"
        f"Customer Interest: {interest}\n"
        f"Service to Pitch: {service}\n"
        f"Preferred Language: {language}\n"
        f"GroMo Partner Name: {gp_name}\n\n"

        "📝 Message Format (strictly follow this):\n"
        "1. Greet the customer warmly using proper name formatting (e.g., 'नमस्ते Geeta जी 🙏')\n"
        "2. Mention their profession respectfully\n"
        "3. List 3–4 benefits using bullet points, each with a relevant emoji\n"
        "4. Mention GroMo APP 📱 for applying\n"
        "5. Highlight GroMo's ease and trust\n"
        "6. Offer help politely: 'मैं आपको पूरी प्रोसेस समझा सकती हूँ।'\n"
        f"7. End with '{gp_name}, and in the next line GroMo Team'\n"
        "8. Use 2–4 emojis meaningfully spread out\n\n"
        "9. Use gender words properly based on the GP name don't make mistake while generating message."
        "10.Message should be short and sweet"

        "📌 Style Rules:\n"
        "- Do not translate words like APP, Credit Card, Loan\n"
        "- Do not mix scripts — use only the selected language\n"
        "- Do not add extra line breaks or large spaces between sentences or words\n"
        f"- Always include the GP name correctly at the end: '{gp_name}, and in the next line GroMo Partner'\n"
    )

    prompt = unicodedata.normalize('NFKC', prompt)

    client = Mistral(api_key=api_key_mistral)
    try:
        completion = client.chat.complete(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        message = completion.choices[0].message.content.strip()
        message = clean_message(message)
        message += "\n\nApply Now: sales.gromo.in/hd/4idZikMK7k"
        return message
    except Exception as e:
        return f"❌ Error generating message: {e}"

if __name__ == "__main__":
    print("Enter customer details to generate a personalized message:\n")
    name = input("Customer Name: ").strip()
    profession = input("Customer Profession: ").strip()
    interest = input("Customer Interest (e.g., CRICKET, Cooking): ").strip()
    service = input("Service to Pitch (e.g., Loan, Credit Card): ").strip()
    language = input("Preferred Language (e.g., Hindi, English, Marathi): ").strip().capitalize()
    gp_name = input("Your (GroMo Partner) Name: ").strip()

    print("\n📝 Generating message...\n")
    message = generate_message(name, profession, interest, service, language, gp_name)
    print("Generated Message:\n")
    print(message)
