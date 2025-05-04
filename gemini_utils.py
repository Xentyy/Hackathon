import os, httpx, asyncio
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY .env dosyasında tanımlı değil.")


async def get_conversion_idea(clothing_item: str) -> str:
    prompt = (
        f"Eski bir {clothing_item} için yaratıcı bir geri dönüşüm fikri ver. "
        "Bu kıyafeti işlevsel bir ürüne dönüştür. Gerekli malzemeleri ve adımları listele."
    )
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    url = ("https://generativelanguage.googleapis.com/v1beta/models/"
           "gemini-pro-1.0:generateContent?key=" + GEMINI_API_KEY)

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


# Senkron test için:
def quick_test():
    print(asyncio.run(get_conversion_idea("eski tişört")))


if __name__ == "__main__":
    quick_test()
