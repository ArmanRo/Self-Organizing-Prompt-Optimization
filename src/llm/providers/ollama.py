import requests

from llm.base_provider import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    def __init__(self, model="mistral"):
        assert model in (
            "mistral",
            "ollama",
        ), "`model` argument can either be `mistral` or `ollama`"
        self.model = model

    def generate(self, prompt):
        data = {"model": "mistral:7b-instruct-q4_K_M", "prompt": prompt, "stream": False, "num_thread": 4}
        response = requests.post("http://localhost:11434/api/generate", json=data)
        response.raise_for_status()
        return response.json().get("response", "")

    def generate_prompts(self, prompt: str, amount: int) -> list[str]:
        raw_prompts = self.generate(prompt)
        prompts = raw_prompts.split("\n")
        prompts = [p for p in prompts if p.strip()]
        cleaned = [s.split('.', 1)[1].lstrip() for s in prompts]
        if len(cleaned) == amount:
            return cleaned
        else:
            print(cleaned)

    def embed(self):
            pass
    