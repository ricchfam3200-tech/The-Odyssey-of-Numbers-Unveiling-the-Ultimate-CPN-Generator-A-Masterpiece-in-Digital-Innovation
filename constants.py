# Constants related to profile number generation and validation

# The minimum allowable value for a profile number
MIN_PROFILE_NUMBER = 100_000_000  # Using underscores for better readability

# The maximum allowable value for a profile number
MAX_PROFILE_NUMBER = 999_999_999  # Using underscores for better readability

# The exact length that a valid profile number should have
PROFILE_NUMBER_LENGTH = 9

# The youngest and oldest age (in years) a generated date of birth may represent
MIN_AGE = 18
MAX_AGE = 90

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
