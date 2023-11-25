from pydantic import BaseModel, Field, computed_field

import const


class TeamData(BaseModel):
    team_id: int = Field(alias=const.TEAM_ID)
    team_name: str = Field(alias=const.TEAM_NAME, exclude=True)
    team_city: str = Field(alias=const.TEAM_CITY, exclude=True)
    score: int
    wins: int
    losses: int

    @computed_field
    def team(self) -> str:
        return self.team_city + " " + self.team_name


class GameShortSummarize(BaseModel):
    game_id: str = Field(alias=const.GAME_ID)
    game_status: int = Field(alias=const.GAME_STATUS)
    game_et: str = Field(alias=const.GAME_ET)
    home_team: TeamData = Field(alias=const.HOME_TEAM)
    away_team: TeamData = Field(alias=const.AWAY_TEAM)
