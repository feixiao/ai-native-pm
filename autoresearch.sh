#!/usr/bin/env bash
set -euo pipefail

# Canonical benchmark entrypoint for autoresearch
# Evaluates Dual-Track Quality Gates:
# 1. Corporate / Industrial TPM Track (Research & PRD)
# 2. Solo Builder Track (AI-Native Workflow & Handbook)
# 3. CLI Sandbox & E2E Installation Gate

python3 harness/test_cli_e2e.py
python3 harness/dual_track_evaluator.py
