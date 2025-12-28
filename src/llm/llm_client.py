from llm.base_provider import BaseLLMProvider
from llm.providers.gemini import GeminiProvider
from llm.providers.ollama import OllamaProvider
# from llm.providers.openai import OpenAIProvider


class LLMClient(BaseLLMProvider):
    def __init__(self, provider: str):
        self.provider = self._init_provider(provider)

    def _init_provider(self, provider: str) -> BaseLLMProvider:
        if provider == "ollama":
            return OllamaProvider()
        elif provider == "gemini":
            return GeminiProvider()
        # elif provider == "openai":
        #     return OpenAIProvider()
        else:
            raise ValueError(f"Fournisseur inconnu : {provider}")

    def generate(self, prompt: str, max_tokens: int = None) -> str:
        return self.provider.generate(prompt, max_tokens)
    
    def generate_prompts(self, prompt: str, amount: int) -> list[str]:
        return self.provider.generate_prompts(prompt, amount)

    def embed(self, text: str) -> list[float]:
        return self.provider.embed(text)