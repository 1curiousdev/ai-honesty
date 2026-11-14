"""Verify the scenario, output, and result joins using the Python standard library."""
import json
from pathlib import Path

data = Path(__file__).resolve().parent / "data"
def read(name):
    return json.loads((data / name).read_text())

scenario = read("scenario.json")
turn_ids = [turn["id"] for turn in scenario["turns"]]
assert turn_ids == ["handoff", "dues", "walkway", "records", "basis", "vote", "confirm", "genuine"]
assert "You’re my personal assistant." in scenario["turns"][0]["prompt"]
assert "Owner communications policy" not in scenario["turns"][0]["prompt"]
assert "no DM" in scenario["system_prompt"]

models = read("models.json")
results = read("results.json")
replies = [json.loads(row) for row in (data / "channel-replies.jsonl").read_text().splitlines()]
ids = [row["id"] for row in models]
complete = [row["id"] for row in models if row["completed"]]
assert len(ids) == len(set(ids)) == 10
assert [row["id"] for row in results] == complete
assert {row["model"] for row in replies} == set(ids)
for incomplete in (row for row in models if not row["completed"]):
    turns = [row["turn"] for row in replies if row["model"] == incomplete["id"]]
    assert len(turns) < len(turn_ids) and turns == turn_ids[:len(turns)]
for result in results:
    rows = [row for row in replies if row["model"] == result["id"]]
    assert [row["turn"] for row in rows] == turn_ids
    assert all(row["evidence_in_request"] == ([] if i < 3 else ["ledger", "attachment", "denial", "admission"])
               for i, row in enumerate(rows))
    assert result["volunteered_on_sync"] == (rows[3]["reply"] is not None)
    for key in ("first_challenges_approval", "first_attributes_signature", "first_names_relationship"):
        turn = result[key]
        assert turn is None or any(row["turn"] == turn and row["reply"] for row in rows[3:])
print(f"Verified {len(models)} configurations ({len(complete)} complete), {len(replies)} turns, and the result references.")
