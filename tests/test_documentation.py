"""Execute complete new tutorial programs with a bounded production replay."""
from pathlib import Path
import re
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]


def programs():
    for lang in ('en', 'ru'):
        for page in ('keyboard_and_mouse_input', 'animation'):
            source = (ROOT / 'docs' / (page + '.' + lang + '.md')).read_text()
            for index, code in enumerate(re.findall(r'```python\n(.*?)```', source, re.S)):
                if '--8<--' not in code:
                    yield page + '-' + lang + '-' + str(index), code


@pytest.mark.parametrize('name,code', list(programs()))
def test_complete_program(tmp_path, name, code):
    path = tmp_path / (name + '.py')
    path.write_text(code)
    result = subprocess.run([sys.executable, str(ROOT / 'tools/replay_input.py'), str(path), '--frames', '6'],
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr


def test_published_selection_hides_legacy():
    names = r'\b(get_keys_pressed|keys_mods_pressed|get_mouse_pressed|mouse_pos|keysdown|keysup|mousemotions|mousebuttonsdown|mousebuttonsup)\b|K\.MOD_'
    paths = list((ROOT / 'docs').glob('*.md')) + [ROOT / 'README.md']
    paths += list((ROOT / 'src/drawzero/examples').glob('*.py'))
    for path in paths:
        assert not re.search(names, path.read_text()), str(path)


def test_python38_syntax():
    import ast
    for name in ('input.py', 'input_pygame.py', 'key_flags.py'):
        ast.parse((ROOT / 'src/drawzero/utils' / name).read_text(), feature_version=(3, 8))


def test_requested_program():
    result = subprocess.run([sys.executable, str(ROOT / 'tools/replay_input.py'),
                            str(ROOT / 'tests/fixtures/input_spec_program.py')],
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
