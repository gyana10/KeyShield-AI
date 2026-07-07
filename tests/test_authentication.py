from backend.ml.comparison.authenticate import authenticate

profile = {

    "avg_hold_time": 110,

    "avg_flight_time": 145,

    "avg_duration": 15000,

    "avg_backspaces": 2

}

sample = {

    "avg_hold_time": 112,

    "avg_flight_time": 148,

    "avg_duration": 15120,

    "avg_backspaces": 1

}

print(

    authenticate(

        profile,

        sample

    )

)