from fastapi import FastAPI
from nba_processor import NBAProcessor

app = FastAPI()


@app.get("/nba/live_scoreboard")
async def live_scoreboard():
    return NBAProcessor.get_live_scoreboard()
