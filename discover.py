import subprocess
import json
import argparse


def upload_pipeline(pipeline_yaml: str):
    subprocess.run(
        ["buildkite-agent", "pipeline", "upload"],
        input=pipeline_yaml,
        text=True,
        check=True,
    )


def pipeline_json(number_of_jobs):
    steps = {
        "steps": [
            {
                "command": "uv run run_chunk.py $$BUILDKITE_PARALLEL_JOB",
                "image": "astral/uv:python3.14-bookworm",
                "parallelism": number_of_jobs,
            }
        ]
    }

    return json.dumps(steps)


def discover_tests():
    subprocess.run(
        ["pytest", "--collect-only", "--collect-report=tests.json"], capture_output=True
    )

    with open("tests.json", "r") as f:
        return json.load(f)


def chunk_tests(tests, num_chunks):
    chunk_size = len(tests) // num_chunks
    remainder = len(tests) % num_chunks

    chunks = []
    start = 0
    for i in range(num_chunks):
        size = chunk_size + (1 if i < remainder else 0)
        chunks.append(tests[start : start + size])
        start += size

    return chunks


def write_chunks(data, chunks):
    for i, chunk in enumerate(chunks):
        chunk_data = {**data, "items": chunk}
        with open(f"tests-chunk-{i}.json", "w") as f:
            json.dump(chunk_data, f, indent=2)
        print(f"tests-chunk-{i}.json: {len(chunk)} tests")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--number-of-jobs", type=int, required=True)
    args = parser.parse_args()

    data = discover_tests()
    chunks = chunk_tests(data["items"], args.number_of_jobs)
    write_chunks(data, chunks)

    pipeline = pipeline_json(args.number_of_jobs)
    upload_pipeline(pipeline)

    return chunks


if __name__ == "__main__":
    main()

