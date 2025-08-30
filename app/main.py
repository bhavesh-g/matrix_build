# app/main.py — Minimal FastAPI illustrating version-based break only on Python <3.10

import sys
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Python Compatibility Demo", version="1.0.0")

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
    # Pattern matching works for Python ≥3.10, fails on <3.10
    version_info = sys.version_info
    match version_info:
        case (3, v, *_) if v >= 10:
            detail = "Pattern matching supported"
        case _:
            detail = "Incompatible Python version"
    return {
        "detail": detail,
        "python_version": f"{version_info.major}.{version_info.minor}"
    }
