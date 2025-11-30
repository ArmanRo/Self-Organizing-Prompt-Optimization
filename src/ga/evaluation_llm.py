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
        cleaned_response = response.strip().replace('"', '').replace("'", "")
        match = re.search(r"(\d+(?:\.\d+)?)", cleaned_response) 
        if match:
            return float(match.group(1)) 
        print(f"ATTENTION: Aucun score valide trouvé dans la réponse LLM. Score par défaut de 0.0.")
        return 0.0 
