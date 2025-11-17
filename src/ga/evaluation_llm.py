import re

from llm.llm_client import LLMClient


class LLMEvaluator:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def evaluate(self, question, answer, criteria) -> float:
        eval_prompt = f"""
        You are an impartial evaluator.
        Rate the following answer from 0 to 10 based on these criteria:
        {criteria}

        Question: {question}
        Answer: {answer}

        Respond with ONLY a single float number between 0 and 10.
        Do NOT add text, comments, or punctuation.
        """
        response = self.llm.generate(eval_prompt, 5)
        print("Eval response:", response)
        match = re.search(r"\d+(?:\.\d+)?", response)
        if match:
            return float(match.group())
        raise ValueError(f"No valid number found in LLM response: {response}")
