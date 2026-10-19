"""Explicit source reader registry; readers use stored bytes only."""

from lib.readers.equality_trust import read as equality_trust
from lib.readers.long_csv import read as long_csv
from lib.readers.worldbank import read as worldbank

READERS = {"equality_trust": equality_trust, "long_csv": long_csv, "worldbank": worldbank}
