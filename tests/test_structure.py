"""Structure checks for Lab 4: LED Light Show.

These read `src/main.py` as Python, not as text, so the words in the story
and in comments do not count. Only real statements do. Each assertion message
says what was found and what was expected.
"""

import ast
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / "src" / "main.py"


def tree():
    return ast.parse(SOURCE.read_text(encoding="utf-8"))


def nodes(kind):
    return [n for n in ast.walk(tree()) if isinstance(n, kind)]


def is_call_to(node, name):
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == name


def test_a_list_literal():
    found = nodes(ast.List)
    assert found, "found no list: the three lights belong in one list, leds = [ ... ]"


def test_len_is_called():
    found = [n for n in nodes(ast.Call) if is_call_to(n, "len")]
    assert found, "found no call to len(...): the number of lights comes from the list, not from a 3 typed by hand"


def test_a_for_loop_over_a_list():
    # A loop over a name (`for led in leds`) rather than over a call (`range(...)`).
    found = [loop for loop in nodes(ast.For) if isinstance(loop.iter, ast.Name)]
    assert found, "found no for loop over a list: `for led in leds:` visits every light without counting them"


def test_append_is_called():
    found = [
        n for n in nodes(ast.Call)
        if isinstance(n.func, ast.Attribute) and n.func.attr == "append"
    ]
    assert found, "found no call to .append(...): Stage Four builds the pattern one step at a time"


def test_a_list_is_indexed():
    found = nodes(ast.Subscript)
    assert found, "found no indexing like leds[choice - 1]: the spotlight and the pattern both pick a light by position"
