import re


class LLMEvaluator:
    def __init__(self, llm_client):
        self.llm = llm_client

    def evaluate(self, question, answer, criteria) -> float:
        eval_prompt = f"""
        You are an impartial evaluator.
        You will receive a question and an answer.
        Please rate it from 0 to 10 based on the following criteria:
        {criteria}

        Question: {question}

        Here is the answer:
        {answer}

        Return a number only, no text, no comment, no explanation.
        Example: 9.2
        """
        response = self.llm.generate(eval_prompt)
        print("eval respond : " + response)
        match = re.search(r"\d+(?:\.\d+)?", response)
        if match:
            number = float(match.group())
        return number
