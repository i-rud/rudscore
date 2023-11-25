from nba_api.live.nba.endpoints import scoreboard

from nba_model import GameShortSummarize


class NBAProcessor:
    @staticmethod
    def get_live_scoreboard():
        sb = scoreboard.ScoreBoard()
        games = sb.games.get_dict()
        return [
            GameShortSummarize(**game).model_dump(by_alias=True, mode="json")
            for game in games
        ]
