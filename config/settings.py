# Configuration settings for the profile number generator

# You can add any settings specific to the environment here.

import os

# Load environment variables if any
MIN_PROFILE_NUMBER = os.environ.get("MIN_PROFILE_NUMBER", 100000000)
MAX_PROFILE_NUMBER = os.environ.get("MAX_PROFILE_NUMBER", 999999999)
