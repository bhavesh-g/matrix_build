# app/main.py — Minimal FastAPI with a Python 3.13–only code path

import sys
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Python Compatibility Demo", version="1.0.0")

class Status(BaseModel):
    python_version: str
    compatible: bool

@app.get("/", response_model=Status)
def root():
    return {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        # Compatible for pattern matching demo (3.10+)—keep as-is if you still use that
        "compatible": sys.version_info >= (3, 10)
    }

@app.get("/pattern-match", response_model=dict)
def pattern_match():
    # This intentionally breaks on Python < 3.10 (due to match/case)
    version_info = sys.version_info
    match version_info:
        case (3, v, *_) if v >= 10:
            detail = "Pattern matching supported"
        case _:
            detail = "Incompatible Python version"
    return {"detail": detail, "python_version": f"{version_info.major}.{version_info.minor}"}

@app.get("/as13", response_model=dict)
async def as13_only():
    """
    Demonstrates Python 3.13–only behavior:
    asyncio.as_completed can be used as an ASYNC iterator starting in 3.13.
    On <=3.12, 'async for' over asyncio.as_completed will raise TypeError.
    """
    async def work(n: float) -> float:
        await asyncio.sleep(n)
        return n

    # Launch three tasks with different delays
    tasks = [asyncio.create_task(work(d)) for d in (0.03, 0.02, 0.01)]
    results = []
    try:
        # Works only on Python 3.13+ because as_completed() is async-iterable there
        async for done in asyncio.as_completed(tasks):
            results.append(await done)
    except TypeError as e:
        # Older Pythons: as_completed is not an async iterator; surface a clear error
        raise HTTPException(
            status_code=500,
            detail=f"Requires Python 3.13+: asyncio.as_completed is not an async iterator here ({e})"
        )

    return {
        "message": "asyncio.as_completed async-iterator demo (3.13+)",
        "results": results,
        "python_version": sys.version,
    }
