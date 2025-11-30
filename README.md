# Self-Organizing-Prompt-Optimization

## Overview
S.O.S. is an experimental AI system designed to automate prompt generation and evaluation using multiple specialized agents. The system allows users to create prompts for large language models (LLMs) and test their effectiveness across different tasks, without manual intervention.

## Features
- `Generate multiple prompts automatically for LLMs.`
- `Evaluate prompt outputs across various tasks.`
- `Use multiple AI agents to handle different types of prompts.`
- `Easy scalability: add more agents to improve coverage and diversity.`

## Technologies
- `Python`
- `Large Language Models (LLMs)`
- `Multi-agent architecture`

## How It Works: The Genetic Optimization Cycle
S.O.S. uses a Genetic Algorithm to continuously refine prompts for maximum effectiveness against a specified criteria.

### 1. Initial Population (Génération 0)
The system starts by generating a set of diverse initial prompts based on the user's main question, leveraging a highly structured meta-prompt to ensure variety (tone, style, and perspective).

### 2. Evaluation
Each prompt in the current population is tested:
a.  **Response Generation:** The prompt is submitted to the target LLM (e.g., Ollama) to generate **N samples** (responses).
b.  **Scoring:** An impartial LLM Evaluator scores each response based on the defined **evaluation criteria** (e.g., "accuracy, language, and level of detail"). The prompt's final score is the average of all response scores.

### 3. Selection and Reproduction
The prompts are sorted by score. The next generation is created using high-performing prompts (parents) through the following genetic operations, determined by the configuration ratios (`elite_ratio`, `improve_ratio`, etc.):

* **Elite (Elitism):** The best prompts are copied directly to the next generation, preserving the highest performance found so far.
* **Improvement (Mutation de haut niveau):** A single parent prompt is submitted to a **Prompt Optimizer LLM** to generate a slightly *better* version.
* **Crossover:** Two high-performing parent prompts are combined by a **Crossover LLM** to create a novel child prompt, fusing their best characteristics.
* **Mutation:** A small, local change (typo fix, word replacement) is applied to a prompt to maintain diversity and explore nearby solutions.

### 4. Iteration
This cycle repeats for a specified number of generations (`max_generations`), gradually converging on the most effective prompt for the task.

## Installation
### Clone the repository:
```bash
git clone git@github.com:ArmanRo/Self-Organizing-Prompt-Optimization.git 
git clone https://github.com/ArmanRo/Self-Organizing-Prompt-Optimization.git
```
### Navigate into the project directory:
```bash
cd Self-Organizing-Prompt-Optimization
```
### Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the main program to start generating prompts:
```bash
python main.py
```
