import json
from pathlib import Path

manifest = json.loads(Path("manifest.json").read_text())
assert manifest["schemaVersion"] == 1
assert manifest["questionCount"] >= 450
ids = set()
total = 0
for entry in manifest["packs"]:
    path = Path(entry["path"])
    assert path.exists(), path
    data = json.loads(path.read_text())
    if entry["type"] != "questions":
        continue
    questions = data["questions"]
    assert len(questions) >= 50, path
    total += len(questions)
    prompts = set()
    levels = set()
    concepts = set()
    for question in questions:
        assert question["id"] not in ids
        ids.add(question["id"])
        assert question["prompt"] not in prompts
        prompts.add(question["prompt"])
        assert len(question["options"]) >= 3
        assert 0 <= question["correctIndex"] < len(question["options"])
        assert question["explanation"].strip()
        assert question["difficulty"] in {"easy", "medium", "hard"}
        levels.add(question["difficulty"])
        concepts.add(question["conceptId"])
    assert levels == {"easy", "medium", "hard"}
    assert len(concepts) >= 10
assert total == manifest["questionCount"]
print(f"Validated {total} questions across {len(manifest['packs']) - 1} topic packs")
