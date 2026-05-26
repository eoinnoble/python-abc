import json
from dataclasses import dataclass
from typing import List, Optional

from python_abc import vector


@dataclass
class AnalysisResult:
    path: str
    vector: Optional[vector.Vector]
    sort_magnitude: float

    @property
    def status(self) -> str:
        if self.vector is None:
            return "syntax_error"

        return "ok"


def render_text(results: List[AnalysisResult]) -> str:
    max_path_length = max((len(result.path) for result in results), default=0)
    lines = []

    for result in results:
        if result.vector is None:
            lines.append(f"{result.path:<{max_path_length}} {'Unable to parse AST':>26}")
        else:
            lines.append(f"{result.path:<{max_path_length}} {result.vector.magnitude:>26}")

    return "\n".join(lines)


def render_json(path: str, results: List[AnalysisResult]) -> str:
    files = []

    for result in results:
        if result.vector is None:
            files.append(
                {
                    "path": result.path,
                    "status": result.status,
                    "vector": None,
                    "magnitude": None,
                    "error": "Unable to parse AST",
                }
            )
        else:
            files.append(
                {
                    "path": result.path,
                    "status": result.status,
                    "vector": {
                        "assignment": result.vector.assignment,
                        "branch": result.vector.branch,
                        "condition": result.vector.condition,
                    },
                    "magnitude": result.vector.get_magnitude_value(),
                    "error": None,
                }
            )

    syntax_errors = sum(1 for result in results if result.vector is None)
    payload = {
        "path": path,
        "files": files,
        "summary": {
            "files": len(results),
            "parsed": len(results) - syntax_errors,
            "syntax_errors": syntax_errors,
        },
    }

    return json.dumps(payload, indent=2)
