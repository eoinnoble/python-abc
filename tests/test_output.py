import json

from python_abc import vector
from python_abc.output import AnalysisResult, render_json, render_text


def test_render_text():
    results = [
        AnalysisResult("file.py", vector.Vector(1, 2, 3), 3.7),
        AnalysisResult("bad.py", None, 0.0),
    ]

    assert render_text(results) == "\n".join(
        [
            "file.py            <1, 2, 3> (3.7)",
            "bad.py         Unable to parse AST",
        ]
    )


def test_render_json():
    results = [
        AnalysisResult("file.py", vector.Vector(1, 2, 3), 3.7),
        AnalysisResult("bad.py", None, 0.0),
    ]

    payload = json.loads(render_json("src", results))

    assert payload == {
        "path": "src",
        "files": [
            {
                "path": "file.py",
                "status": "ok",
                "vector": {
                    "assignment": 1,
                    "branch": 2,
                    "condition": 3,
                },
                "magnitude": 3.7,
                "error": None,
            },
            {
                "path": "bad.py",
                "status": "syntax_error",
                "vector": None,
                "magnitude": None,
                "error": "Unable to parse AST",
            },
        ],
        "summary": {
            "files": 2,
            "parsed": 1,
            "syntax_errors": 1,
        },
    }

    assert "display" not in payload["files"][0]
