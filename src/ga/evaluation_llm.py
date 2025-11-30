import re

from llm.llm_client import LLMClient
from utils.prompt import EVALUATION_PROMPT_TEMPLATE


class LLMEvaluator:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def evaluate(self, question, answer, criteria) -> float:
        eval_prompt = EVALUATION_PROMPT_TEMPLATE.format(
            criteria=criteria,
            question=question,
            answer=answer
        )
        response = self.llm.generate(eval_prompt, 5)
        print("Eval response:", response)
        match = re.search(r"\d+(?:\.\d+)?", response)
        if match:
            return float(match.group())
        raise ValueError(f"No valid number found in LLM response: {response}")
