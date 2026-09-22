"""Automated checks for Lab 4: LED Light Show.

Every check reads the show log at the end of the run, or looks at which lights
came on and in what order, never the narrative lines, so the story is the
student's to word. Log values are matched loosely: any amount of whitespace,
any letter case, and the colon is optional, so `print("Lights:", n)`,
`print("Lights: " + str(n))`, and `print(f"Lights: {n}")` all read the same.

The lights are told apart by the GPIO number each `Pin(...)` was made with,
in the order they were made, so the checks call them the first, second and
third light and never depend on the actual pin numbers. Checks that count
flashes compare two runs that differ in one answer, so a fixed extra flash
somewhere else does not fail anyone: only the change has to match.

When a check fails, the assertion message says which log line came out wrong,
what it said, what was expected, and the answers that were typed. gatorgrade
does not show that message itself; it prints the pytest command to run.
"""

import re
from unittest.mock import patch

import mockro

from main import main

# The order the starter asks its questions. `pattern` is a list of the light
# numbers typed for Stage Four; the count typed first is its length.
QUESTIONS = ["name", "choice", "rounds", "pattern"]

# A quiet run. Individual checks change exactly the answers they are about.
SAFE = dict(name="JJ", choice=1, rounds=1, pattern=[1])


def run(capsys, **changes):
    """Run main() once with the SAFE answers plus `changes`.

    Returns what it printed, the answers used, and the sequence of lights that
    came on, as positions 1, 2, 3 in the order the program made its Pins.
    """
    answers = {**SAFE, **changes}
    typed = [str(answers["name"]), str(answers["choice"]), str(answers["rounds"])]
    typed.append(str(len(answers["pattern"])))
    typed.extend(str(number) for number in answers["pattern"])
    recorder = mockro.get_recorder()
    recorder.clear()
    # time.sleep is real here (mockro only mocks it under `import utime`), so
    # it is patched directly to keep the checks instant.
    with patch("builtins.input", side_effect=typed), patch("time.sleep", return_value=None):
        main()
    out, err = capsys.readouterr()
    assert err == "", "the program wrote to the error stream:\n" + err
    return out, answers, lit_sequence(recorder)


def lit_sequence(recorder):
    """The lights that came on, in order, numbered 1, 2, 3 by construction order.

    mockro binds the Pin instance twice when it records, so a construction
    call looks like (pin, pin, gpio, mode, ...) and an on() call like
    (pin, pin). Pins made with a number are the external lights.
    """
    position = {}
    for args, _ in recorder.calls("machine.Pin.init"):
        if len(args) > 2 and isinstance(args[2], int) and id(args[0]) not in position:
            position[id(args[0])] = len(position) + 1
    sequence = []
    for args, _ in recorder.calls("machine.Pin.on"):
        sequence.append(position.get(id(args[0])))
    for args, _ in recorder.calls("machine.Pin.value"):
        if len(args) > 2 and args[2]:
            sequence.append(position.get(id(args[0])))
    return sequence


def counts(sequence):
    """How many times each light came on, as {position: count}."""
    return {light: sequence.count(light) for light in (1, 2, 3)}


def log_value(out, label):
    """Return the value printed after `label` in the show log, normalized.

    Only the part of the output from `SHOW LOG` onward is searched. Whitespace
    is collapsed inside the label and the value, case is folded to upper, a
    trailing period is dropped, and the colon after the label is optional.
    Returns None when the log, or the label, was never printed.
    """
    start = out.upper().find("SHOW LOG")
    if start < 0:
        return None
    words = r"\s+".join(re.escape(word) for word in label.split())
    match = re.search(rf"{words}\s*:?\s*([^\n]*)", out[start:], re.IGNORECASE)
    if match is None:
        return None
    return " ".join(match.group(1).split()).upper().rstrip(".! ")


def describe(answers):
    return ", ".join(f"{q}={answers[q]}" for q in QUESTIONS)


def expect(capsys, label, want, **changes):
    """Run once and check that the show log line `label` says `want`."""
    out, answers, _ = run(capsys, **changes)
    typed = describe(answers)
    if "SHOW LOG" not in out.upper():
        raise AssertionError(f'no "SHOW LOG" line was printed (answers typed: {typed})')
    got = log_value(out, label)
    if got is None:
        raise AssertionError(f'no "{label}" line was printed after SHOW LOG (answers typed: {typed})')
    assert got == str(want), f'the "{label}" line said {got}, expected {want} (answers typed: {typed})'
    return out


def difference(capsys, **pair):
    """Run twice, changing one answer, and return how many more times each light came on."""
    (question, (low, high)), = pair.items()
    _, _, seq_low = run(capsys, **{question: low})
    _, _, seq_high = run(capsys, **{question: high})
    low_counts, high_counts = counts(seq_low), counts(seq_high)
    return {light: high_counts[light] - low_counts[light] for light in (1, 2, 3)}


def test_program_runs_and_log_names_you(capsys):
    # An untouched starter prints its provided framing text either way, so
    # checking for the user's own name in the log is what actually requires
    # Stage One and the show log to be done.
    expect(capsys, "SHOW LOG", "JJ")


def test_lights_counts_the_list(capsys):
    expect(capsys, "Lights", 3)


def test_spotlight_picks_the_chosen_light(capsys):
    expect(capsys, "Spotlight", 3, choice=3)
    expect(capsys, "Spotlight", 3, choice=7)
    expect(capsys, "Spotlight", 1, choice=0)
    # Choosing 3 instead of 1 moves the spotlight flashes from the first light
    # to the third, and leaves the second alone.
    moved = difference(capsys, choice=(1, 3))
    assert moved[2] == 0, f"changing the spotlight from 1 to 3 changed the second light by {moved[2]}, expected no change"
    assert moved[3] > 0, f"changing the spotlight from 1 to 3 did not light the third light any more often (change: {moved[3]})"
    assert moved[1] == -moved[3], f"the first light lost {-moved[1]} flashes but the third gained {moved[3]}: the same light should blink either way, chosen by leds[choice - 1]"


def test_chase_visits_every_light_once_per_round(capsys):
    expect(capsys, "Chase rounds", 2, rounds=2)
    more = difference(capsys, rounds=(1, 3))
    assert more == {1: 2, 2: 2, 3: 2}, f"two more rounds lit the lights {more} more times (first, second, third), expected 2 each: the loop over leds goes inside the loop over range(rounds)"


def test_pattern_plays_the_steps_in_order(capsys):
    _, answers, sequence = run(capsys, pattern=[3, 3, 2, 1])
    window = [3, 3, 2, 1]
    found = any(sequence[i:i + 4] == window for i in range(len(sequence) - 3))
    assert found, f"typing 3, 3, 2, 1 should light the third light twice, then the second, then the first, in that order; the lights came on in this order: {sequence} (answers typed: {describe(answers)})"
    expect(capsys, "Pattern steps", 4, pattern=[3, 3, 2, 1])


def test_pattern_skips_a_number_with_no_light(capsys):
    # 5 has no light behind it, so it is skipped rather than crashing, and
    # only the two valid steps are kept.
    expect(capsys, "Pattern steps", 2, pattern=[2, 5, 1])
