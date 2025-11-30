INITIAL_POPULATION_PROMPT_TEMPLATE = """
You are an expert prompt generator.
Your task is to create {amount} highly diverse prompts for a large language model (LLM).

Each prompt you create must:
- Focus strictly on the following subject or question: "{subject}"
- Be written with a unique and varied style, tone, or perspective (e.g., scientific, poetic, humorous, technical, narrative).
- Be clear, natural, and self-contained, useful as a standalone request to another LLM.
- Avoid repeating structure or phrasing from other generated prompts in the list.

Output format requirements:
- Return the prompts as a clean list of {amount} distinct prompts.
- Do not use commentary, numbering, bullet points, or any explanation outside of the list itself.
- Do not use quotes or extra punctuation around the prompts.
"""

def build_initial_prompt(subject: str, amount: int = 10) -> str:
    return INITIAL_POPULATION_PROMPT_TEMPLATE.format(subject=subject, amount=amount)


IMPROVE_SYSTEM_PROMPT = (
    "You are a prompt optimizer. "
    "Given a prompt, generate a slightly improved version of it. "
    "Your modifications must be small, preserve the original intent, "
    "and increase clarity, precision, or usefulness. "
    "Always stay focused on the main topic defined by the user question. "
    "Never invent new sub-tasks."
)

IMPROVE_USER_PROMPT_TEMPLATE = (
    "User's main question: {question}\n"
    "Prompt to improve:\n{prompt}"
)

def build_improvement_prompt(question: str, prompt: str) -> str:
    system_msg = IMPROVE_SYSTEM_PROMPT
    user_msg = IMPROVE_USER_PROMPT_TEMPLATE.format(
        question=question,
        prompt=prompt
    )
    return system_msg + "\n\n" + user_msg


MUTATE_SYSTEM_PROMPT = (
    "You are a mutation operator for a genetic algorithm. "
    "Apply only a *small local mutation* to the prompt: "
    "replace a word, rephrase a clause, or add minor clarification. "
    "Keep the meaning and structure unchanged. "
    "Always ensure the mutated prompt remains closely related to the main user question."
)

MUTATE_USER_PROMPT_TEMPLATE = (
    "User's main question: {question}\n"
    "Prompt to mutate:\n{prompt}"
)

def build_mutation_prompt(question: str, prompt: str) -> str:
    system_msg = MUTATE_SYSTEM_PROMPT
    user_msg = MUTATE_USER_PROMPT_TEMPLATE.format(
        question=question,
        prompt=prompt
    )
    return system_msg + "\n\n" + user_msg


CROSSOVER_SYSTEM_PROMPT = (
    "You are a sophisticated genetic operator for prompt optimization. "
    "Your task is to perform a *crossover* operation. "
    "Combine the best structural elements, tones, and perspectives "
    "of the two provided high-performing prompts (Parent A and Parent B) "
    "into a single, novel, and highly effective prompt (Child Prompt). "
    "The new prompt must target the main user question and retain the "
    "high quality demonstrated by the parents."
)

CROSSOVER_USER_PROMPT_TEMPLATE = (
    "User's main question: {question}\n"
    "Parent A:\n{prompt_a}\n"
    "Parent B:\n{prompt_b}"
)

def build_crossover_prompt(question: str, prompt_a: str, prompt_b: str) -> str:
    system_msg = CROSSOVER_SYSTEM_PROMPT
    user_msg = CROSSOVER_USER_PROMPT_TEMPLATE.format(
        question=question,
        prompt_a=prompt_a,
        prompt_b=prompt_b
    )
    return system_msg + "\n\n" + user_msg


EVALUATION_PROMPT_TEMPLATE = """
You are an impartial evaluator.
Rate the following answer from 0 to 10 based on these criteria:
{criteria}

Question: {question}
Answer: {answer}

Respond with ONLY a single float number between 0 and 10.
Do NOT add text, comments, or punctuation.
"""



# Others
"""

Describe a rabbit. bicycle sunflower


Explain how rainbows form.
Vérifier présence de mots-clés : “light”, “refraction”, “droplets”


If Alice is older than Bob and Bob is older than Carol, who is youngest?
What is the sum of all even numbers between 1 and 10?

"""