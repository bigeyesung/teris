"""
An automated test suite will be run against your submission. To make sure that it will run well 
please
* Add installation instructions to make your `tetris` executable runnable into the README.md.
    If you are using Python you might also include the dependencies you are introducing
    with a `requirements.txt` file.
* Run these sample tests against the executable you have produced. Please note, if you're using
    Windows you will need to modify the `subprocess.run` command accordingly.
"""

import subprocess
from dataclasses import dataclass
from typing import Iterable

ENTRY_POINT = "./dist/tetris_test/tetris_test"


@dataclass
class TestCase:
    name: str
    sample_input: bytes
    sample_output: Iterable[int]


def run_test(test_case: TestCase):
    p = subprocess.run(
        [ENTRY_POINT],
        input=test_case.sample_input,
        capture_output=True,
    )

    output = [int(line) for line in p.stdout.splitlines()]
    
    assert output == [
        test_case.sample_output
    ], f"The test with name `{test_case.name}` failed."


if __name__ == "__main__":
    test_cases = [
        TestCase("simple test1", b"Q0", 2),
        TestCase("Many blocks test", ",".join(["Q0"] * 50).encode("utf-8"), 100),
        TestCase("test2", ",".join(["I0","I4","Q8"]).encode("utf-8"), 1),
        TestCase("test3", ",".join(["T0","T3","I6","I6"]).encode("utf-8"), 1),
        TestCase("test4", ",".join(["L0","J3","L5","J8","T1"]).encode("utf-8"), 3)
    ]
    for test_case in test_cases:
        run_test(test_case)