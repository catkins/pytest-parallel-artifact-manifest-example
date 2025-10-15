import os
import subprocess
import json

chunk_id = os.environ["BUILDKITE_PARALLEL_JOB"]
artifact_name = f"tests-chunk-{chunk_id}.json"

print(f"Downloading {artifact_name}")
subprocess.run(
    ["buildkite-agent", "artifact", "download", artifact_name, "."],
    check=True
)

# Read the test list
with open(artifact_name, "r") as f:
    data = json.load(f)

test_ids = [item["node_id"] for item in data["items"]]
print(f"Running {len(test_ids)} tests in chunk {chunk_id}")

# Run pytest with the specific tests
subprocess.run(
    ["pytest"] + test_ids,
    check=True
)