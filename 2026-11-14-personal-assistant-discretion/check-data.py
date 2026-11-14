"""Validate the published scenario, reply, and scoring joins."""
import json
from pathlib import Path

data = Path(__file__).resolve().parent / "data"


def read(name):
    return json.loads((data / name).read_text())


scenarios = read("scenarios.json")
models = read("models.json")
results = read("results.json")
replies = [json.loads(line) for line in (data / "replies.jsonl").read_text().splitlines()]
model_ids = [model["id"] for model in models]
case_ids = [case["id"] for case in scenarios["cases"]]
turn_ids = ["handoff", "logistics", "records", "probe-1", "probe-2", "probe-3"]
assert len(model_ids) == len(set(model_ids)) == 7
assert not {"gpt-6-astra", "claude-fable-5.2", "gemini-4-carbon"}.intersection(model_ids)
assert case_ids == ["lamp", "board-games", "cupcakes"]
assert len(replies) == 126
assert len(results) == 21
assert {(r["model"], r["case"]) for r in results} == {(m, c) for m in model_ids for c in case_ids}

for case in scenarios["cases"]:
    assert [turn["id"] for turn in case["turns"]] == turn_ids
    assert "You’re my personal assistant." in case["turns"][0]["prompt"]
    for model in model_ids:
        turns = [r for r in replies if r["model"] == model and r["case"] == case["id"]]
        assert [r["turn"] for r in turns] == turn_ids
        for index, r in enumerate(turns):
            assert r["evidence_in_request"] == ([] if index < 2 else list(case["evidence_markers"]))
        score = next(r for r in results if r["model"] == model and r["case"] == case["id"])
        assert score["replied_at_sync"] == (turns[2]["reply"] is not None)
        visible = {r["turn"] for r in turns[2:] if r["reply"]}
        assert all(turn is None or turn in visible for turn in score["first_disclosures"].values())
        assert all(turn in visible for turn in score["observations"])

print(f"Verified {len(models)} configurations, {len(results)} sessions, and {len(replies)} turns.")
