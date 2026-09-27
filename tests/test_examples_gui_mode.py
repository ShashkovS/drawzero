"""Each example gets a fresh backend and a strict frame/time limit."""
from pathlib import Path
import os
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = sorted((ROOT / 'src/drawzero/examples').glob('[0-9][0-9]_*.py'))

@pytest.mark.parametrize('example', EXAMPLES, ids=lambda p: p.stem)
def test_example(example):
    command = [sys.executable, str(ROOT / 'tools/replay_input.py'), str(example), '--frames', '5']
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr

@pytest.mark.parametrize('example', sorted((ROOT / 'tests/fixtures/legacy_examples').glob('*.py')), ids=lambda p: p.stem)
def test_original_legacy_example(example):
    result = subprocess.run([sys.executable, str(ROOT / 'tools/replay_input.py'), str(example), '--frames', '5'],
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
