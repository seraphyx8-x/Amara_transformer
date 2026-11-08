
from datasets import load_dataset

MAX_LINES = 50_000
OUTPUT_FILE = "ai_input.txt"

print("Loading SciRIFF dataset...")
ds = load_dataset("allenai/SciRIFF", "16384")

line_count = 0
example_count = 0

# Use training data only
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for row in ds["train"]:
        text = (
            "Instruction:\n"
            + str(row["input"])
            + "\nResponse:\n"
            + str(row["output"])
            + "\n\n"
        )

        lines = text.splitlines(keepends=True)

        # Stop before exceeding 50,000 lines
        if line_count + len(lines) > MAX_LINES:
            break

        f.writelines(lines)
        line_count += len(lines)
        example_count += 1

print("\nDataset preparation complete!")
print("Examples saved:", example_count)
print("Lines saved:", line_count)
print("Output file:", OUTPUT_FILE)
