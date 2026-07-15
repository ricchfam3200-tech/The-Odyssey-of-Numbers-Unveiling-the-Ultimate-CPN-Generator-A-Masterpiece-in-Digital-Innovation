# Constants related to profile number generation and validation

# The exact length that a valid profile number should have
PROFILE_NUMBER_LENGTH = 9

# Base player ID prefixes (7 digits each). A generated profile number is one of these
# prefixes plus a random 2-digit suffix.
PLAYER_ID_PREFIXES = [
    "0144100",
    "7649500",
    "5749100",
    "4169300",
]

# The minimum age (in years) required to generate a profile number
MIN_AGE = 18

# US states (and DC) offered as an option when generating a profile number
US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming",
]
