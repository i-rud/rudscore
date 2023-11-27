import pandas as pd

from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import LeagueStandingsV3, ScoreboardV2, BoxScoreTraditionalV2, TeamDetails

import const

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

        stripped_df = df[[
            const.TEAM_ID_STANDING, const.TEAM_CITY_STANDING,
            const.TEAM_NAME_STANDING, const.WINS_STANDING,
            const.LOSSES_STANDING, const.LAST_10_STANDING,
            const.CONFERENCE_STANDING]]

        return [
            TeamStanding(**standing).model_dump(by_alias=True, mode="json")
            for standing in stripped_df.to_dict("records")
        ]

    def get_schedule(self, date: str):
        day = date[0:2]
        month = date[2:4]
        year = date[4:8]

        iso_date = year + "-" + month + "-" + day
        scoreboard_for_day = ScoreboardV2(game_date=iso_date).get_dict()
        data_sets = scoreboard_for_day["resultSets"][:2]

        game_header = pd.DataFrame(columns=data_sets[0]["headers"], data=data_sets[0]["rowSet"])[
            ["GAME_DATE_EST", "GAME_ID", "GAME_STATUS_ID", "GAME_STATUS_TEXT",]
        ]
        line_score = pd.DataFrame(columns=data_sets[1]["headers"], data=data_sets[1]["rowSet"])[
            ["GAME_ID", "TEAM_ID", "TEAM_CITY_NAME", "TEAM_NAME", "PTS"]
        ].fillna(value=0)

        schedule = []
        if line_score.empty:
            return schedule
        for index, row in game_header.iterrows():
            teams = line_score[line_score["GAME_ID"] == row["GAME_ID"]]

            game_summary = {
                const.GAME_ID: row["GAME_ID"],
                const.GAME_STATUS: row["GAME_STATUS_ID"],
                const.GAME_STATUS_TEXT: row["GAME_STATUS_TEXT"],
                const.GAME_ET: row["GAME_DATE_EST"],
                const.HOME_TEAM: {
                    const.TEAM_ID: teams.at[teams.index[0], "TEAM_ID"],
                    const.TEAM_CITY: teams.at[teams.index[0], "TEAM_CITY_NAME"],
                    const.TEAM_NAME: teams.at[teams.index[0], "TEAM_NAME"],
                    const.SCORE: teams.at[teams.index[0], "PTS"]
                },
                const.AWAY_TEAM: {
                    const.TEAM_ID: teams.at[teams.index[1], "TEAM_ID"],
                    const.TEAM_CITY: teams.at[teams.index[1], "TEAM_CITY_NAME"],
                    const.TEAM_NAME: teams.at[teams.index[1], "TEAM_NAME"],
                    const.SCORE: teams.at[teams.index[1], "PTS"]
                },
            }

            schedule.append(GameShortSummary(**game_summary).model_dump(by_alias=True, mode="json"))

        return schedule

    @staticmethod
    def get_game_boxscore(game_id):
        game_box_score = BoxScoreTraditionalV2(game_id=game_id).get_dict()

        data_set = game_box_score["resultSets"][1]

        boxscore_df = pd.DataFrame(columns=data_set["headers"], data=data_set["rowSet"])
        boxscore = boxscore_df[
            [const.TEAM_ID_SCHEDULE, const.TEAM_CITY_SCHEDULE, const.TEAM_NAME_SCHEDULE, const.PTS_SCHEDULE]
        ].to_dict("records")

        return boxscore

    @staticmethod
    def get_team_name_and_city(team_id) -> tuple[str, str]:
        team1_name = TeamDetails(team_id=team_id).get_dict()
        data_set = team1_name["resultSets"][0]

        team_info_df = pd.DataFrame(columns=data_set["headers"], data=data_set["rowSet"])
        team_info = team_info_df[
            [const.TEAM_INFO_CITY_SCHEDULE, const.TEAM_INFO_NICKNAME_SCHEDULE]
        ].to_dict("records")

        return team_info[0][const.TEAM_INFO_CITY_SCHEDULE], team_info[0][const.TEAM_INFO_NICKNAME_SCHEDULE]
