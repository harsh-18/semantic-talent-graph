from preprocess import load_candidates
from config import DATASET_PATH
from behavior import extract_behavior


candidates = load_candidates(DATASET_PATH)

result = extract_behavior(candidates[0])

print(result)