import re
import unicodedata
import os
from dotenv import load_dotenv
from mistralai import Mistral

# Load .env file variables
load_dotenv()

# DEBUG: Print the API key to verify it's loaded correctly (remove/comment after testing)
print(f"MISTRAL_API_KEY={os.getenv('MISTRAL_API_KEY')}")

# Get API key from environment
api_key_mistral = os.getenv("MISTRAL_API_KEY")

def clean_message(message):
    message = unicodedata.normalize('NFKC', message)
    message = re.sub(r'[\u200B-\u200D\uFEFF]', '', message)
    message = message.replace('\u00A0', ' ')
    lines = message.splitlines()
    cleaned_lines = []

    for line in lines:
        line = re.sub(r'[ \t]+', ' ', line)
        line = re.sub(r'\s+([.,!?])', r'\1', line)
        line = re.sub(r'\s+([📈📊📱📉📌🔒💸🙏])', r'\1', line)
        line = line.strip()
        if line.startswith("-"):
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")
            cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)

    cleaned_text = []
    prev_line = ""
    for line in cleaned_lines:
        if line == "" and prev_line == "":
            continue
        cleaned_text.append(line)
        prev_line = line

    final_text = "\n".join(cleaned_text)
    final_text = re.sub(r"(?<!\n)\n([^\n]+,)\n(GroMo Team)", r"\n\n\1\n\2", final_text)
    final_text = re.sub(r"\n{2,}Apply Now", r"\n\nApply Now", final_text)

    return final_text.strip()

def generate_message(name, profession, interest, service, language, gp_name):
    if not api_key_mistral:
        return "❌ Error: API key not found. Please set MISTRAL_API_KEY in your environment."

    model = "mistral-large-latest"
    prompt = (
        f"You are a creative, fluent copywriter writing on behalf of a GroMo Partner named {gp_name}.\n"
        f"The message should be written as if it's coming from ONE PERSON (the GP), not a company.\n"
        f"Tone should be polite, warm, respectful, and in fluent {language}.\n"
        f"Focus on customer benefit. Avoid clichés or generic references to interest unless very relevant.\n\n"
        
        # **Added gender instruction here:**
        "Please ensure that the correct gender pronouns and grammatical forms are used in the text, "
        "based on the gender associated with the person's name (GP name). Adjust the language accordingly to reflect the preferred language's rules for gender.\n\n"
        "- If the GP is male, use masculine pronouns and verb forms.\n"
        "- If the GP is female, use feminine pronouns and verb forms.\n"
        "- If the preferred language has gender-neutral options, apply them appropriately when the gender is unknown or non-binary.\n"
        "Always verify the gender from the GP name or provided information before applying grammar changes.\n\n"
        
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
        f"7. End with '{gp_name}, and in the next line GroMo Partner'\n"
        "8. Use 2–4 emojis meaningfully spread out\n"
        "9. \n"
        "10. Message should be short and sweet\n\n"
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
        # Add clickable HTML link:
        message += '\n\nApply Now: <a href="https://sales.gromo.in/hd/4idZikMK7k" target="_blank" rel="noopener noreferrer">sales.gromo.in/hd/4idZikMK7k</a>'
        return message
    except Exception as e:
        return f"❌ Error generating message: {e}"
