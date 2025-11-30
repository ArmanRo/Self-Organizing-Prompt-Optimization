PROMPT_PART1 = """
You are an expert prompt generator.
Your task is to create {amount} highly diverse prompts for a large language model (LLM).

Each prompt you create must:
- Focus on the following subject or question:
"""

PROMPT_PART2 = """
- Be written with a unique tone, style, or perspective
- Avoid repeating structure or phrasing from other prompts
- Be clear, natural, and self-contained
- Be useful as a standalone request to another LLM

Output format requirements:
- Return the prompts as a clean list of {amount} prompts
- No commentary or explanation outside the list
- No extra quotes or punctuation 
"""

def build_initial_prompts(subject: str, amount: int = 10) -> str:
    return (
        PROMPT_PART1.format(amount=amount)
        + f"\n{subject}\n"
        + PROMPT_PART2.format(amount=amount)
    )



#####
EVALUATION_PROMPT_TEMPLATE = """
You are an impartial evaluator.
Rate the following answer from 0 to 10 based on these criteria:
{criteria}

Question: {question}
Answer: {answer}

Respond with ONLY a single float number between 0 and 10.
Do NOT add text, comments, or punctuation.
"""


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



# Others
PROMPT1 = """
You are a prompt generator.
Create 10 different prompts that ask a large language model (LLM) to describe a rabbit.
Each prompt should have a different style, level of detail, or perspective.
Output them as a numbered list.
"""


PROMPT2 = """
You are a creative prompt designer.
Generate 10 diverse prompts for asking an LLM to describe a rabbit.
Vary tone and style (scientific, poetic, humorous, child-friendly, etc.)
Some prompts should ask for short descriptions, others detailed explanations.
Avoid repeating phrasing.
Return the list clearly numbered from 1 to 10.
"""


"""

Describe a rabbit. bicycle sunflower


Explain how rainbows form.
Vérifier présence de mots-clés : “light”, “refraction”, “droplets”


If Alice is older than Bob and Bob is older than Carol, who is youngest?
What is the sum of all even numbers between 1 and 10?

"""