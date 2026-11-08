#!/usr/bin/env bash
set -euo pipefail

# Canonical benchmark entrypoint for autoresearch
# Evaluates Dual-Track Quality Gates:
# 1. Corporate / Industrial TPM Track (Research & PRD)
# 2. Solo Builder Track (AI-Native Workflow & Handbook)

python3 harness/dual_track_evaluator.py
