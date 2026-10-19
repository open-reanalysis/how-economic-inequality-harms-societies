# SPDX-License-Identifier: MIT
# Offline transcript conversion; also usable before the shared scaffold exists.
TED_TRANSCRIPT_DIR := sources/supporting/original-authors/wilkinson-2011-ted
PIXI ?= pixi
REPLAY_TARGETS += $(TED_TRANSCRIPT_DIR)/transcript.en.csv

$(TED_TRANSCRIPT_DIR)/transcript.en.csv: code/00_prepare_ted_transcript.py $(TED_TRANSCRIPT_DIR)/captions.en.json3
	$(PIXI) run --locked python code/00_prepare_ted_transcript.py
