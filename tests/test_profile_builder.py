from etl.profile_builder import ProfileBuilder

builder = ProfileBuilder()

profiles = builder.build_profiles()

print()

print(profiles.head())