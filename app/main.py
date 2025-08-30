# app/main.py - Simple but shows version compatibility
import sys
from fastapi import FastAPI

app = FastAPI(
    title=f"Python {sys.version_info.major}.{sys.version_info.minor} Build Demo",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "message": "Multi-Python Version Build Demo",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "build_status": "success",
        "features": get_version_features()
    }

@app.get("/build-info")  
def build_info():
    return {
        "python_version": sys.version,
        "platform": sys.platform,
        "build_compatible": True,
        "version_specific_features": get_version_features()
    }

def get_version_features():
    """Show which Python features are available in this version"""
    features = ["fastapi", "async-await", "type-hints"]
    
    if sys.version_info >= (3, 10):
        features.extend(["pattern-matching", "union-types"])
    if sys.version_info >= (3, 11):
        features.extend(["exception-groups", "tomllib"])
    if sys.version_info >= (3, 12):
        features.extend(["f-string-debug", "type-params"])
    
    return features

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
