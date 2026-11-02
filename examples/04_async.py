# Step 4: async endpoints and background tasks.
# Run:  fastapi dev examples/04_async.py
# /dashboard waits for three slow "services" at the same time: about 1 second, not 3.
import asyncio
import time

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


async def fetch(service: str, seconds: float) -> dict:
    await asyncio.sleep(seconds)  # stands in for a database query or an HTTP call
    return {"service": service, "took": seconds}


@app.get("/dashboard")
async def dashboard():
    start = time.perf_counter()
    results = await asyncio.gather(fetch("orders", 1), fetch("payments", 1), fetch("profile", 1))
    return {"results": results, "total_seconds": round(time.perf_counter() - start, 1)}


def send_welcome_email(email: str) -> None:
    time.sleep(2)  # pretend this is slow
    print(f"Welcome email sent to {email}")


@app.post("/signup")
def signup(email: str, background: BackgroundTasks):
    background.add_task(send_welcome_email, email)
    return {"message": "Signed up! Check your inbox."}  # returned immediately, email sent afterwards
