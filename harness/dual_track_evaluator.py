#!/usr/bin/env python3
"""
Dual-Track Comprehensive Evaluation Harness for:
1. Corporate / Industrial TPM Track (Feasibility Research & Enterprise PRD in harness/evaluator.py)
2. Solo Builder Track (AI-Native Solo PM Workflow & Guide in harness/solo_workflow_evaluator.py)

Outputs:
METRIC score=<float 0.0-100.0> (Harmonic/Composite score across both tracks)
METRIC corporate_tpm_score=<float 0.0-100.0>
METRIC solo_builder_score=<float 0.0-100.0>
METRIC research_score=<float 0.0-40.0>
METRIC prd_score=<float 0.0-60.0>
METRIC workflow_completeness=<float 0.0-30.0>
METRIC ai_native_score=<float 0.0-30.0>
"""

import os
import sys

# Import both evaluators
from evaluator import read_file as read_file_corp, evaluate_research, evaluate_prd, RESEARCH_FILE, PRD_FILE
from solo_workflow_evaluator import (
    read_file as read_file_solo,
    evaluate_solo_skill,
    SKILL_FILE,
    HANDBOOK_FILE,
    WORKFLOW_FILE,
    BASE_HANDBOOK_FILE,
    AGENTS_FILE,
)
def main():
    # 1. Run Corporate TPM evaluation
    r_content = read_file_corp(RESEARCH_FILE)
    p_content = read_file_corp(PRD_FILE)
    
    if not r_content or not p_content:
        print(f"ERROR: Corporate files missing: {RESEARCH_FILE} or {PRD_FILE}", file=sys.stderr)
        sys.exit(1)

    r_score, r_details = evaluate_research(r_content)
    p_score, p_details = evaluate_prd(p_content)
    corp_score = round(r_score + p_score, 2)

    # 2. Run Solo Builder evaluation
    skill_content = read_file_solo(SKILL_FILE)
    handbook_content = read_file_solo(HANDBOOK_FILE)
    workflow_content = read_file_solo(WORKFLOW_FILE)
    base_content = read_file_solo(BASE_HANDBOOK_FILE)
    agents_content = read_file_solo(AGENTS_FILE)
    
    if not skill_content or not handbook_content:
        print(f"ERROR: Solo files missing: {SKILL_FILE} or {HANDBOOK_FILE}", file=sys.stderr)
        sys.exit(1)

    solo_score, solo_details = evaluate_solo_skill(
        skill_content, handbook_content, workflow_content, base_content, agents_content
    )

    # 3. Calculate composite dual-track score (equal weight 50% / 50%)
    composite_score = round((corp_score + solo_score) / 2.0, 2)

    print(f"METRIC score={composite_score:.2f}")
    print(f"METRIC corporate_tpm_score={corp_score:.2f}")
    print(f"METRIC solo_builder_score={solo_score:.2f}")
    print(f"METRIC research_score={r_score:.2f}")
    print(f"METRIC prd_score={p_score:.2f}")
    print(f"METRIC workflow_completeness={solo_details['workflow_completeness']:.2f}")
    print(f"METRIC ai_native_score={solo_details['ai_native_score']:.2f}")
    print(f"METRIC red_team_rigor={solo_details['red_team_rigor']:.2f}")
    print(f"METRIC guardrails_score={solo_details['guardrails_score']:.2f}")
    print(f"METRIC templates_score={solo_details['templates_score']:.2f}")

    sys.exit(0)
if __name__ == "__main__":
    main()
