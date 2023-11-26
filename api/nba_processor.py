import pandas as pd

from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import LeagueStandingsV3

from nba_model import GameShortSummary, TeamStanding


class NBAProcessor:
    @staticmethod
    def get_live_scoreboard():
        sb = scoreboard.ScoreBoard()
        games = sb.games.get_dict()
        return [
            GameShortSummary(**game).model_dump(by_alias=True, mode="json")
            for game in games
        ]

    @staticmethod
    def get_league_standings():
        standings = LeagueStandingsV3().get_dict()
        data_set = standings.get("resultSets")[0]

        df = pd.DataFrame(
            columns=data_set.get("headers"),
            data=data_set.get("rowSet")
        )

        stripped_df = df[["TeamID", "TeamCity", "TeamName", "WINS", "LOSSES", "L10", "Conference"]]

        return [
            TeamStanding(**standing).model_dump(by_alias=True, mode="json")
            for standing in stripped_df.to_dict("records")
        ]
