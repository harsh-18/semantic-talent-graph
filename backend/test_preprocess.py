from preprocess import preprocess_candidates
from config import DATASET_PATH

processed = preprocess_candidates(DATASET_PATH)

print("Total Processed Candidates:", len(processed))

print("\nFirst Processed Candidate:\n")

print(processed[0])