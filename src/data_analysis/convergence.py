import argparse
import json
import os
import matplotlib.pyplot as plt


def compute_best_score_curve(version_path, num_generations=30, top_k=3):
    best_scores = []

    for gen in range(num_generations):
        gen_file = os.path.join(version_path, f"gen_{gen}.json")

        if not os.path.exists(gen_file):
            raise FileNotFoundError(f"Missing file: {gen_file}")

        with open(gen_file, "r", encoding="utf-8") as f:
            population = json.load(f)

        scores = sorted(
            [individual["final_score"] for individual in population],
            reverse=True
        )

        k = min(top_k, len(scores))
        top_k_avg = sum(scores[:k]) / k

        best_scores.append(top_k_avg)

    return best_scores



def compute_convergence_curve(version_path, num_generations=30):
    convergence_scores = []

    for gen in range(num_generations):
        gen_file = os.path.join(version_path, f"gen_{gen}.json")

        if not os.path.exists(gen_file):
            raise FileNotFoundError(f"Missing file: {gen_file}")

        with open(gen_file, "r", encoding="utf-8") as f:
            population = json.load(f)

        scores = [individual["final_score"] for individual in population]

        avg_score = sum(scores) / len(scores)
        convergence_scores.append(avg_score)

    return convergence_scores


def plot_convergence_curve(scores_dict, title=None, ylabel="Fitness score"):
    plt.figure()

    for label, scores in scores_dict.items():
        generations = list(range(len(scores)))
        plt.plot(generations, scores, label=label)

    plt.xlabel("Generation")
    plt.ylabel(ylabel)

    if title:
        plt.title(title)

    plt.legend()
    plt.grid(True)
    plt.show()



def save_convergence_curve(scores, output_path, title=None):
    generations = list(range(len(scores)))

    plt.figure()
    plt.plot(generations, scores)
    plt.xlabel("Generation")
    plt.ylabel("Average fitness score")

    if title:
        plt.title(title)

    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="Plot the convergence curve of a genetic algorithm run."
    )
    parser.add_argument(
        "results_path",
        nargs="?",
        default="../results/v1",
        help="Path to a results folder containing gen_*.json files "
             "(default: ../results/v1, relative to this script).",
    )
    parser.add_argument(
        "--generations",
        type=int,
        default=30,
        help="Number of generations to read (default: 30).",
    )
    parser.add_argument(
        "--title",
        default="Convergence Curve",
        help="Title for the plot.",
    )
    parser.add_argument(
        "--save",
        metavar="OUTPUT_PNG",
        default=None,
        help="If set, save the curve to this path instead of showing it.",
    )
    args = parser.parse_args()

    scores = compute_convergence_curve(args.results_path, args.generations)

    if args.save:
        os.makedirs(os.path.dirname(args.save) or ".", exist_ok=True)
        save_convergence_curve(scores, output_path=args.save, title=args.title)
        print(f"Saved convergence curve to {args.save}")
    else:
        plot_convergence_curve(
            {"Average population": scores},
            title=args.title,
        )


if __name__ == "__main__":
    main()
