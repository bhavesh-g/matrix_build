# app/main.py — Minimal version-breaking FastAPI for CI matrix demo

import sys
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Python Compatibility Demo",
    version="1.0.0"
)

class Status(BaseModel):
    python_version: str
    compatible: bool

@app.get("/", response_model=Status)
def root():
    return {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "compatible": sys.version_info >= (3, 10)
    }

@app.get("/pattern-match", response_model=dict)
def pattern_match():
    # This match/case block breaks on Python < 3.10
    match sys.version_info.minor:
        case v if v >= 12:
            detail = "Latest features available"
        case v if v >= 10:
            detail = "Core pattern matching supported"
        case _:
            detail = "Incompatible Python version"
    return {"detail": detail, "python_version": f"{sys.version_info.major}.{sys.version_info.minor}"}
