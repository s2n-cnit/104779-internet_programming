import uvicorn

host = "0.0.0.0"
port = 9998

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
