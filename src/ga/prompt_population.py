import random

from ga.prompt_candidate import PromptCandidate
from llm.llm_client import LLMClient


class PromptPopulation:
    def __init__(self, prompts, llm: LLMClient = None):
        self.prompts = [
            p if isinstance(p, PromptCandidate) else PromptCandidate(p)
            for p in prompts
        ]
        self.llm = llm


    def sort(self, scores):    
        for candidate, score in zip(self.prompts, scores):
            candidate.score = score

        self.prompts.sort(key=lambda c: c.score, reverse=True)

    
    def improve_prompt(self, prompt: str) -> str:
        system_msg = (
            "You are a prompt optimizer. "
            "Given a prompt, you generate a slightly improved version of it. "
            "Your modifications must be small, preserve the original intent, "
            "and increase clarity, precision, or usefulness. "
            "Never change the topic. Never invent new sub-tasks."
        )

        user_msg = f"Here is the prompt to improve:\n\n{prompt}"

        return self.llm.generate(system_msg + user_msg)


    def mutate_prompt(self, prompt: str) -> str:
        system_msg = (
            "You are a mutation operator for a genetic algorithm. "
            "You only apply a *small local mutation* to the prompt: "
            "replace a word, rephrase a clause, or add minor clarification. "
            "Keep the meaning and structure unchanged."
        )

        user_msg = f"Mutate this prompt:\n{prompt}"

        return self.llm.generate(system_msg + user_msg)
    

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