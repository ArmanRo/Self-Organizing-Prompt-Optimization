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


import matplotlib.pyplot as plt

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


best_version_path = "../results_darwinism/v2"
version_path = "../results_darwinism/v2"

best_scores = compute_best_score_curve(version_path)
scores = compute_convergence_curve(version_path)

plot_convergence_curve({
        # "Best prompt": best_scores,
        "Average population": scores
    }, title="Convergence Curve – Darwinism (v2)")

save_convergence_curve(
    scores,
    output_path="graphs/darwinism_v2_convergence.png",
    title="Convergence Curve – Darwinism (v2)"
)
