import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def test_every_numbered_example_runs_offline() -> None:
    examples = sorted((ROOT / "examples").glob("[0-9][0-9]_*.py"))
    assert len(examples) == 41
    environment = os.environ | {"OPENAI_API_KEY": ""}
    for example in examples:
        result = subprocess.run(
            [sys.executable, str(example)],
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            timeout=15,
            check=False,
        )
        assert result.returncode == 0, f"{example.name}: {result.stderr}"
        assert "OK:" in result.stdout or "SKIP:" in result.stdout


def test_eval_matrix_targets_exist() -> None:
    example = (ROOT / "examples" / "37_eval_matrix.py").read_text()
    tests_source = (ROOT / "tests" / "test_workflow.py").read_text()
    names = re.findall(r"test_[a-z0-9_]+", example)
    assert names
    for name in names:
        assert f"def {name}(" in tests_source, name
