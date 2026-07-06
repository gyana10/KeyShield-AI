from etl.profile_builder import ProfileBuilder

builder = ProfileBuilder()

profiles = builder.build_profiles()

print("\nFirst 5 Profiles\n")

print(profiles.head())

print("\nShape")

print(profiles.shape)