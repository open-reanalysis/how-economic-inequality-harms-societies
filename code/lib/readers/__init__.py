"""Explicit source reader registry; readers use stored bytes only."""

from lib.readers.census_historical import read as census_historical
from lib.readers.census_statab import read as census_statab
from lib.readers.equality_trust import read as equality_trust
from lib.readers.fbi_historical import read as fbi_historical
from lib.readers.long_csv import read as long_csv
from lib.readers.worldbank import read as worldbank

READERS = {
    "equality_trust": equality_trust,
    "long_csv": long_csv,
    "worldbank": worldbank,
    "census_historical": census_historical,
    "census_statab": census_statab,
    "fbi_historical": fbi_historical,
}
