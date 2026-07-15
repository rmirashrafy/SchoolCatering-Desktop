import base64
from openai import OpenAI

# کلاینت را با کلید خودتان بسازید (توصیه می‌شود کلید خود را در محیط امن نگه دارید)
client = OpenAI(api_key="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")

def encode_image(image_path):
    """تبدیل عکس محلی به فرمت Base64 برای ارسال به API"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# ۱. مسیر عکس فیش خود را اینجا وارد کنید
image_path = "im1.jpeg" 
base64_image = encode_image(image_path)

# ۲. ارسال درخواست به مدل gpt-4o-mini
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Extract all texts, numbers, items, and information from this receipt image with high accuracy. Provide the extracted data in a structured, clean, and highly readable format in English (translate any non-English text to English)."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
)


# ۳. چاپ خروجی دریافت شده از مدل
print(response.choices[0].message.content)
