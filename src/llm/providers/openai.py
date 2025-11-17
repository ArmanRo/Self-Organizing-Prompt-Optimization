# from openai import OpenAI

# from llm.base_provider import BaseLLMProvider


# class OpenAIProvider(BaseLLMProvider):
#     def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
#         self.client = OpenAI(api_key=api_key)
#         self.model = model

#     def generate(self, prompt: str) -> str:
#         response = self.client.chat.completions.create(
#             model=self.model,
#             messages=[{"role": "user", "content": prompt}],
#         )
#         return response.choices[0].message.content
    
#     def generate_prompts(self, prompt: str, amount: int) -> list[str]:
#         response = self.client.chat.completions.create(
#             model=self.model,
#             messages=[{"role": "user", "content": prompt}],
#         )
#         raw_prompts = response.choices[0].message.content
#         prompts = raw_prompts.split("\n")
#         if len(prompts) == amount:
#             return prompts
#         else:
#             print(prompts)
        
#     def embed(self, text: str) -> list[float]:
#         response = self.client.embeddings.create(
#             model="text-embedding-3-small",
#             input=text,
#         )
#         return response.data[0].embedding
