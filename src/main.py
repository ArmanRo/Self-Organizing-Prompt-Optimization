from ga.genetic_algorithm import GeneticAlgorithm


def main():
    llm_provider = "ollama"
    question = "In a few words, describe a rabbit"
    prompts_amount = 10
    evaluation_criteria = "accuracy, language, and level of detail"
    evaluator = "llm"
    max_generations = 10


    ga = GeneticAlgorithm(llm_provider, question, prompts_amount, evaluation_criteria, evaluator, max_generations)
    ga.run()


if __name__ == "__main__":
    main()