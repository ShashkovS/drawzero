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
    command.append('--text')
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
