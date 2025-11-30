import json
import statistics

from ga.evaluation_llm import LLMEvaluator
from llm.llm_client import LLMClient
from utils.prompt import build_initial_prompts
from .prompt_population import PromptPopulation


class GeneticAlgorithm:
    def __init__(self, llm_provider: str, question: str, prompts_amount: int, evaluation_criteria, evaluator: str, max_generations: int):
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
    def save_prompts_to_json(prompts, filename: str = "initial_prompts.json") -> None:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(prompts, f, ensure_ascii=False, indent=4)


    def generate_initial_prompts(self):
        final_prompt = build_initial_prompts(self.question, amount=self.prompts_amount)
        initial_prompts = self.llm.generate_prompts(final_prompt, amount=self.prompts_amount)
        self.save_prompts_to_json(initial_prompts)
        return initial_prompts


    def evaluate_population(self, population: PromptPopulation, n_samples=2, n_judgments=2):
        final_scores = []
        evaluation_details = []

        for candidate in population.prompts:
            prompt_text = candidate.text
            prompt_responses = []
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

                avg_answer_score = statistics.mean(scores_for_answer)
                all_scores.append(avg_answer_score)

                prompt_responses.append({
                    "response": answer,
                    "scores": scores_for_answer,
                    "average_score": avg_answer_score
                })

            final_score = statistics.mean(all_scores)
            final_scores.append(final_score)

            evaluation_details.append({
                "prompt": prompt_text,
                "responses": prompt_responses,
                "final_score": final_score
            })

        return final_scores, evaluation_details


    def run(self):
        initial_prompts = self.generate_initial_prompts()
        population = PromptPopulation(initial_prompts, self.question, self.llm)

        for gen in range(self.max_generations):
            scores, evaluation_details = self.evaluate_population(
                population,
                n_samples=2,
                n_judgments=2
            )

            filename = f"gen_{gen}.json"
            self.save_prompts_to_json(evaluation_details, filename)

            population.sort(scores)
            population.generate_next_population()

        return population