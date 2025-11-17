from utils.text_similarity import cosine_similarity

def evaluate_responses(responses, reference_text):
    return [cosine_similarity(r, reference_text) for r in responses]

def has_converged(scores, tolerance=0.001):
    return max(scores) - min(scores) < tolerance
