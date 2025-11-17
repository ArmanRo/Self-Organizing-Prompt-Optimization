class PromptCandidate:
    def __init__(self, text: str, score: float = None):
        self.text = text
        self.score = score