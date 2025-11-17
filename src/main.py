from ga.genetic_algorithm import GeneticAlgorithm
from ga.prompt_population import PromptPopulation
from ga.evaluation_llm import LLMEvaluator


def main():
    llm_provider = "ollama"
    question = "Describe a rabbit"
    prompts_amount = 10
    evaluation_criteria = "accuracy, language, and level of detail"
    evaluator = "llm"
    max_generations = 10


    ga = GeneticAlgorithm(llm_provider, question, prompts_amount, evaluation_criteria, evaluator, max_generations)
    ga.run()


if __name__ == "__main__":
    main()