from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

    @abstractmethod
    def generate_prompts(self, prompt: str, amount: int) -> list[str]:
        pass

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        pass