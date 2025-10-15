# Pytest Parallel test splitting with artifacts

A quick demo pipeline to demonstrate using Buildkite artifacts and parallel command steps to split a test suite.

[View in Buildkite](https://buildkite.com/catkins-test/pytest-parallel-artifact-manifest-example)

## Components

`discover.py --number-of-chunks N`

- use `pytest-discover` to create a manifest of tests in a suite
-  split it up into N chunks
-  upload chunked manifests to artifacts

`run_chunk.py`

- download chunk from buildkite artifacts
- run pytest test examples from the uploaded chunk

