from pydantic import BaseModel, Field, computed_field, field_serializer
from dateutil import parser

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
    game_et: str = Field(alias=const.GAME_ET, exclude=True)
    game_status_text: str = Field(alias="gameStatusText")
    home_team: TeamData = Field(alias=const.HOME_TEAM)
    away_team: TeamData = Field(alias=const.AWAY_TEAM)

    @computed_field(alias="gameTimestamp")
    def game_timestamp(self) -> str:
        dt = parser.parse(self.game_et)
        return dt.strftime("%d/%m/%Y %H:%M (ET)")
