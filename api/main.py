from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from nba_processor import NBAProcessor

app = FastAPI()
nba_processor = NBAProcessor()

origins = [
    # Front-End App
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/nba/live_scoreboard")
async def live_scoreboard():
    return NBAProcessor.get_live_scoreboard()


@app.get("/nba/standings")
async def standings():
    return NBAProcessor.get_league_standings()


@app.get("/nba/schedule/{date}")
async def schedule(date):
    return nba_processor.get_schedule(date)
