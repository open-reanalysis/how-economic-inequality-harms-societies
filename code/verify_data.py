# SPDX-License-Identifier: MIT
# Purpose: Verify recorded file identities without downloading any input.
# Thread: scaffold
# Reads: data/metadata/ and recorded stored files
# Writes: none
# Network: none

"""Run full source-record checks; missing restricted files are reported separately."""

from check_contracts import check

if __name__ == "__main__":
    check("full")
