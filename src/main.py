import json
from pathlib import Path

from ga.genetic_algorithm import GeneticAlgorithm


def main():
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    llm_provider = config["llm_provider"]
    model = config.get("model")
    question = config["question"]
    prompts_amount = config["prompts_amount"]
    evaluation_criteria = config["evaluation_criteria"]
    evaluator_model = config.get("evaluator_model")
    max_generations = config["max_generations"]
    output_version = config.get("output_version", "v1")
    n_samples = config.get("evaluation_n_samples", 2)
    n_judgments = config.get("evaluation_n_judgments", 2)
    ga_ratios = config.get("genetic_algorithm")

    ga = GeneticAlgorithm(
        llm_provider=llm_provider,
        model=model,
        question=question,
        prompts_amount=prompts_amount,
        evaluation_criteria=evaluation_criteria,
        max_generations=max_generations,
        output_version=output_version,
        n_samples=n_samples,
        n_judgments=n_judgments,
        ga_ratios=ga_ratios,
        evaluator_model=evaluator_model
    )
    ga.run()


if __name__ == "__main__":
    main()