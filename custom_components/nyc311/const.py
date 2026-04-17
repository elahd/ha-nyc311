"""Constants for the NYC 311 Calendar integration."""

from nyc311calendar import ServiceType

DOMAIN = "nyc311"
ISSUE_URL = "https://github.com/elahd/hass-nyc311/issues"
INTEGRATION_NAME = "NYC 311 Public Services Calendar"

# Using a raw string and a single variable to prevent linter confusion
LOGO = r"""
===================================================================
 @@@@   *@@@ ,@@@      @@@   ,@@@@@@@@
@@@@@@@  @@@@@@@@@@   @@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@ @@@@@@@@@@@ @@@@@
@@@@@ @@@@@@@@    @@@@@    @@@@@@@@@@@@@
@@@@@   &@@@@@    @@@@@     %@@@@@@@@@@
===================================================================
"""

STARTUP_MESSAGE = f"{LOGO}\n{DOMAIN}\nThis is a custom component\nIssues: {ISSUE_URL}"

SERVICE_ICONS = {
    ServiceType.PARKING: "mdi:car",
    ServiceType.SCHOOL: "mdi:bag-personal",
    ServiceType.SANITATION: "mdi:delete",
}

DAY_NAMES = {
    -1: "Yesterday",
    0: "Today",
    1: "Tomorrow",
    2: "in 2 Days",
    3: "in 3 Days",
    4: "in 4 Days",
    5: "in 5 Days",
    6: "in 6 Days",
}
