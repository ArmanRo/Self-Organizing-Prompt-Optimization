import random

from ga.prompt_candidate import PromptCandidate
from llm.llm_client import LLMClient
from utils.prompt import build_improvement_prompt, build_mutation_prompt


class PromptPopulation:
    def __init__(self, prompts, question: str, llm: LLMClient = None):
        self.prompts = [
            p if isinstance(p, PromptCandidate) else PromptCandidate(p)
            for p in prompts
        ]
        self.question = question
        self.llm = llm


    def sort(self, scores):    
        for candidate, score in zip(self.prompts, scores):
            candidate.score = score

        self.prompts.sort(key=lambda c: c.score, reverse=True)

    
    def improve_prompt(self, prompt: str) -> str:
        improvement_prompt = build_improvement_prompt(self.question, prompt)
        return self.llm.generate(improvement_prompt)


    def mutate_prompt(self, prompt: str) -> str:
        mutation_prompt = build_mutation_prompt(self.question, prompt)
        return self.llm.generate(mutation_prompt)

    

    def generate_next_population(self):
        generation_size = len(self.prompts)
        elite_ratio = 0.2
        improve_ratio = 0.4
        mutate_ratio = 0.4

        parents = self.prompts

        new_population = []

        n_elites   = max(1, int(generation_size * elite_ratio))
        n_improves = max(1, int(generation_size * improve_ratio))
        n_mutates  = max(1, int(generation_size * mutate_ratio))

        for _ in range(n_improves):
            parent = random.choice(parents)
            improved = self.improve_prompt(parent.text)
            new_population.append(PromptCandidate(improved))

        for _ in range(n_mutates):
            parent = random.choice(parents)
            mutated = self.mutate_prompt(parent.text)
            new_population.append(PromptCandidate(mutated))

        elites = parents[:n_elites]
        for e in elites:
            print(e.text)
            new_population.append(PromptCandidate(e.text))

        new_population = new_population[:generation_size]
        self.prompts = new_population

        return self.prompts