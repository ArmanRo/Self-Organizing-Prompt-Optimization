import random

from ga.prompt_candidate import PromptCandidate
from llm.llm_client import LLMClient
from utils.prompt import build_improvement_prompt, build_mutation_prompt, build_crossover_prompt


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
    
    def crossover_prompts(self, prompt_a: str, prompt_b: str) -> str:
        crossover_prompt = build_crossover_prompt(self.question, prompt_a, prompt_b)
        return self.llm.generate(crossover_prompt)

    

    def generate_next_population(self):
        generation_size = len(self.prompts)
        elite_ratio = 0.2
        improve_ratio = 0.35
        mutate_ratio = 0.35
        crossover_ratio = 0.1
        

        parents = self.prompts

        new_population = []

        n_elites   = max(1, int(generation_size * elite_ratio))
        n_improves = max(1, int(generation_size * improve_ratio))
        n_mutates  = max(1, int(generation_size * mutate_ratio))
        n_crossovers = max(1, int(generation_size * crossover_ratio))

        if len(parents) < 2:
            n_crossovers = 0
            n_improves = generation_size - n_elites - n_mutates

        for _ in range(n_improves):
            parent = random.choice(parents)
            improved = self.improve_prompt(parent.text)
            new_population.append(PromptCandidate(improved))

        for _ in range(n_mutates):
            parent = random.choice(parents)
            mutated = self.mutate_prompt(parent.text)
            new_population.append(PromptCandidate(mutated))

        for _ in range(n_crossovers):
            parent_a, parent_b = random.choices(parents, k=2)
            crossed = self.crossover_prompts(parent_a.text, parent_b.text)
            new_population.append(PromptCandidate(crossed))

        elites = parents[:n_elites]
        for e in elites:
            print(e.text)
            new_population.append(PromptCandidate(e.text))

        new_population = new_population[:generation_size]
        self.prompts = new_population

        return self.prompts