from pydantic import BaseModel, Field, computed_field, field_serializer
from dateutil import parser

import const


class TeamData(BaseModel):
    team_id: int = Field(alias=const.TEAM_ID)
    team_name: str = Field(alias=const.TEAM_NAME, exclude=True)
    team_city: str = Field(alias=const.TEAM_CITY, exclude=True)
    score: int
    wins: int = Field(default=-1)
    losses: int = Field(default=-1)

    @computed_field
    def team(self) -> str:
        return self.team_city + " " + self.team_name


class GameShortSummary(BaseModel):
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


class TeamStanding(BaseModel):
    team_id: int = Field(alias=const.TEAM_ID_STANDING, serialization_alias=const.TEAM_ID)
    team_name: str = Field(alias=const.TEAM_NAME_STANDING, exclude=True)
    team_city: str = Field(alias=const.TEAM_CITY_STANDING, exclude=True)

    wins: int = Field(alias=const.WINS_STANDING, serialization_alias=const.WINS_OUTPUT)
    losses: int = Field(alias=const.LOSSES_STANDING, serialization_alias=const.LOSSES_OUTPUT)
    last_10: str = Field(alias=const.LAST_10_STANDING, serialization_alias=const.LAST_10_OUTPUT)
    conference: str = Field(alias=const.CONFERENCE_STANDING, serialization_alias=const.CONFERENCE_OUTPUT)

    @computed_field
    def team(self) -> str:
        return self.team_city + " " + self.team_name

    @field_serializer('last_10')
    def serialize_dt(self, last_10: str, _info):
        return last_10.strip()
