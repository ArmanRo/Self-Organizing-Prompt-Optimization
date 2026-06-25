import os
import requests

from llm.base_provider import BaseLLMProvider

gemini_api_key = os.environ.get("GEMINI_API_KEY", "")


class GeminiProvider(BaseLLMProvider):
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1/models/{model}:generateContent"   
        self.full_api_url = f"{self.API_URL_TEMPLATE.format(model=model)}?key={gemini_api_key}"

    def generate(self, prompt: str, max_tokens: int = None) -> str:
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {}
        }

        if max_tokens is not None:
            payload["generationConfig"]["maxOutputTokens"] = max_tokens

        #print(payload)
        try:
            response = requests.post(self.full_api_url, json=payload)            
            response.raise_for_status()
            response_data = response.json()
            #print(response_data)

            generated_text = (
                response_data.get("candidates", [])[0]
                .get("content", {})
                .get("parts", [])[0]
                .get("text", "")
            )
            
            return generated_text

        except requests.exceptions.RequestException as e:
            print(f"HTTP request error: {e}")
            if 'response' in locals() and response.text:
                print(f"API error response: {response.text}")
            return ""


    def generate_prompts(self, prompt: str, amount: int) -> list[str]:
        raw_prompts = self.generate(prompt)
        prompts = raw_prompts.split("\n")
        prompts = [p for p in prompts if p.strip()]
        if len(prompts) == amount:
            return prompts
        else:
            print(prompts)


    def embed(self, text: str) -> list[float]:
        pass
