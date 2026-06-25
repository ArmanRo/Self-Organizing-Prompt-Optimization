import requests

from llm.base_provider import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    def __init__(self, model="mistral"):
        assert model in (
            "mistral",
            "ollama",
        ), "`model` argument can either be `mistral` or `ollama`"
        self.model = model

    def generate(self, prompt: str, max_tokens: int = None, temperature: float = 0.7) -> str:
        data = {
            "model": "mistral:7b-instruct-q4_K_M", 
            "prompt": prompt, 
            "stream": False, 
            "num_thread": 4,
            "options": {
                "temperature": temperature
            }
        }
        if max_tokens is not None:
            data["max_tokens"] = max_tokens
            #data["options"]["num_predict"] = max_tokens
        response = requests.post("http://localhost:11434/api/generate", json=data)
        response.raise_for_status()
        return response.json().get("response", "")

    def generate_prompts(self, prompt: str, amount: int) -> list[str]:
        raw_prompts = self.generate(prompt)
        lines = raw_prompts.split("\n")

        cleaned = []
        for line in lines:
            line = line.strip()
            
            if not line:
                continue

            if line[0].isdigit() and "." in line:
                cleaned.append(line.split(".", 1)[1].strip())
            else:
                cleaned.append(line)

        print(cleaned)

        if len(cleaned) == amount:
            return cleaned
        else:
            print(cleaned)
            return cleaned

    def embed(self):
            pass
    