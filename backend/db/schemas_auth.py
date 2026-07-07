from pydantic import BaseModel


class AuthenticationRequest(BaseModel):

    holdTimes: list[float]

    flightTimes: list[float]

    totalDuration: float

    backspaces: int