import json
import statistics

from ga.evaluation_llm import LLMEvaluator
from llm.llm_client import LLMClient
from utils.prompt import build_prompt
from .prompt_population import PromptPopulation


class GeneticAlgorithm:
    def __init__(self, llm_provider, question, prompts_amount, evaluation_criteria, evaluator, max_generations):
        self.llm = LLMClient(provider=llm_provider)
        self.question = question
        self.prompts_amount = prompts_amount
        self.evaluation_criteria = evaluation_criteria
        if evaluator == "llm":
            self.evaluator = LLMEvaluator(LLMClient(provider=llm_provider))
        else:
            self.evaluator = LLMEvaluator(self.llm)
        self.max_generations = max_generations
        self.gen = 0


    @staticmethod
    def save_prompts_to_json(prompts: list[str], filename: str = "initial_prompts.json") -> None:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(prompts, f, ensure_ascii=False, indent=4)


    def generate_initial_prompts(self):
        final_prompt = build_prompt(self.question, amount=self.prompts_amount)
        initial_prompts = self.llm.generate_prompts(final_prompt, amount=self.prompts_amount)
        self.save_prompts_to_json(initial_prompts)
        return initial_prompts


    def evaluate_population(self, population: PromptPopulation, n_samples=2, n_judgments=2):
        final_scores = []

        for candidate in population.prompts:
            prompt_text = candidate.text
            all_scores = []

            for _ in range(n_samples):
                answer = self.llm.generate(prompt_text)

                scores_for_answer = []
                for _ in range(n_judgments):
                    score = self.evaluator.evaluate(
                        question=self.question,
                        answer=answer,
                        criteria=self.evaluation_criteria
                    )
                    scores_for_answer.append(score)

                all_scores.append(statistics.mean(scores_for_answer))

            final_scores.append(statistics.mean(all_scores))

        return final_scores


    def run(self):
        initial_prompts = self.generate_initial_prompts()
        population = PromptPopulation(initial_prompts, self.llm)

        for gen in range(self.max_generations):
            scores = self.evaluate_population(
                population,
                n_samples=2,
                n_judgments=2
            )

            population.sort(scores)
            population.generate_next_population()

        return population