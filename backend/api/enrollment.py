profile_data = create_profile(data)

existing_profile = db.query(UserProfile).filter(
    UserProfile.user_id == user.id
).first()

if existing_profile:
    existing_profile.hold_mean = profile_data["hold_mean"]
    existing_profile.hold_std = profile_data["hold_std"]

    existing_profile.flight_mean = profile_data["flight_mean"]
    existing_profile.flight_std = profile_data["flight_std"]

    existing_profile.total_duration = profile_data["total_duration"]
    existing_profile.backspaces = profile_data["backspaces"]

else:
    profile = UserProfile(
        user_id=user.id,
        **profile_data
    )

    db.add(profile)

db.commit()