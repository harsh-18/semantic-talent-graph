from preprocess import load_candidates
from config import DATASET_PATH

from honeypot import (
    calculate_honeypot_score,
    is_honeypot
)

candidates = load_candidates(DATASET_PATH)

candidate = candidates[0]

print(calculate_honeypot_score(candidate))
print(is_honeypot(candidate))