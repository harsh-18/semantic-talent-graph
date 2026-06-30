from preprocess import preprocess_candidates, load_candidates
from config import DATASET_PATH

raw_candidates = load_candidates(DATASET_PATH)
processed = preprocess_candidates(raw_candidates)

print("Total Processed Candidates:", len(processed))

print("\nFirst Processed Candidate:\n")

print(processed[0])