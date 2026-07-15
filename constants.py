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

# Each access code below may be used to generate at most this many profile numbers
ACCESS_CODE_LIMIT = 5

# Access codes handed out to players; each is good for ACCESS_CODE_LIMIT profile numbers
ACCESS_CODES = [
    "2EHW-QAW2",
    "2QNC-KQPL",
    "2W29-6NT9",
    "3PG4-HS7Y",
    "3WCW-E5KW",
    "78KS-LSYZ",
    "8AN8-57ZK",
    "8HRR-6F4Q",
    "8P67-AVBD",
    "9KKG-KJN4",
    "ATMM-7ARS",
    "BYW3-59MM",
    "CS59-WKA3",
    "DLFF-NWF6",
    "ESZQ-89JZ",
    "EYC9-UG4Y",
    "G3RR-BJV4",
    "H9YT-ZY8M",
    "LSFN-6UD6",
    "MEKX-VJCF",
]

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
