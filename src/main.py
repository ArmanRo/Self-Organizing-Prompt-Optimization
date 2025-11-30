import json

from ga.genetic_algorithm import GeneticAlgorithm


def main():
    with open("config.json", "r") as f:
        config = json.load(f)

    llm_provider = config["llm_provider"]
    question = config["question"]
    prompts_amount = config["prompts_amount"]
    evaluation_criteria = config["evaluation_criteria"]
    evaluator = config["evaluator"]
    max_generations = config["max_generations"]
    
    
    ga = GeneticAlgorithm(
        llm_provider=llm_provider,
        question=question,
        prompts_amount=prompts_amount,
        evaluation_criteria=evaluation_criteria,
        evaluator=evaluator,
        max_generations=max_generations
    )
    ga.run()


if __name__ == "__main__":
    main()