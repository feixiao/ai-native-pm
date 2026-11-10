#!/usr/bin/env bash
set -euo pipefail

# Canonical benchmark entrypoint for autoresearch
# Goal: grow the agent skill ecosystem so the FULL product-operations
# lifecycle is covered ("产品运营不分家").
#
# Quality gates (must all pass; non-zero exit on failure):
# 1. CLI E2E sandbox: install/update/list mechanics (count scales with registry)
# 2. Dual-track content quality: Corporate TPM + Solo Builder gates
# 3. Skill ecosystem: lifecycle coverage, operations focus, craft, three-surface sync
#
# Metrics emitted by the ecosystem evaluator:
#   METRIC ecosystem_score      (PRIMARY, 0-100 composite)
#   METRIC lifecycle_coverage   (0-1)
#   METRIC ops_coverage         (0-1)
#   METRIC avg_skill_quality    (0-1)
#   METRIC cli_sync             (0-1)
#   METRIC skill_count / registered_count / bundle_count

python3 harness/test_cli_e2e.py
python3 harness/dual_track_evaluator.py
python3 harness/skill_ecosystem_evaluator.py
