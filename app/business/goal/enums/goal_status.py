from enum import StrEnum


class GoalStatus(StrEnum):
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    OFF_TRACK = "off_track"