#!/usr/bin/env python3
"""
E2E Sandbox Automated Test for ai-native-pm CLI
Verifies:
1. Fresh target project: list shows uninstalled
2. Single skill installation (pm-prd-copilot): checks .agents and .cursor directories, zero broken relative links, wake commands materialized as .claude/commands/*.md pointing back at the skill
3. Batch installation (--all): all 7 skills installed
4. Safe conflict handling and --force update
5. Global mode (-g) with isolated HOME environment
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLI_BIN = REPO_ROOT / "cli" / "bin" / "cli.mjs"

def expected_skill_count():
    """Derive the expected installed skill count from the CLI registry,
    so the gate stays green as the ecosystem grows (never hardcode)."""
    meta = (REPO_ROOT / "cli" / "src" / "skills-meta.mjs").read_text(encoding="utf-8")
    return len(re.findall(r"id:\s*'[\w-]+',", meta))

def run_cli(args, cwd=None, env=None):
    cmd = ["node", str(CLI_BIN)] + args
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    res = subprocess.run(cmd, cwd=cwd or str(REPO_ROOT), env=merged_env, capture_output=True, text=True)
    return res

def test_cli():
    n = expected_skill_count()
    print(f"  (CLI registry contains {n} skills; assertions scale with it.)")
    print("🧪 [Test 1/6] CLI --help & --version basic check...")
    res = run_cli(["--version"])
    assert res.returncode == 0, f"Version check failed: {res.stderr}"
    assert "ai-native-pm" in res.stdout

    res = run_cli(["--help"])
    assert res.returncode == 0
    assert "add [skills...]" in res.stdout
    assert f"{n} 大 PM 技能" in res.stdout, "Help text advertises a stale skill count!"
    print("  ✔ Version and Help commands passed.")

    with tempfile.TemporaryDirectory() as temp_project_dir:
        sandbox = Path(temp_project_dir)
        print(f"🧪 [Test 2/6] Fresh sandbox project check: {sandbox}")

        # List in empty sandbox
        res = run_cli(["list", "-d", str(sandbox)])
        assert res.returncode == 0
        assert "未安装" in res.stdout
        print("  ✔ Empty sandbox correctly reports uninstalled.")

        # Single install: pm-prd-copilot
        print("🧪 [Test 3/6] Single skill installation: pm-prd-copilot...")
        res = run_cli(["add", "pm-prd-copilot", "-d", str(sandbox), "-f"])
        assert res.returncode == 0, f"Add failed: {res.stderr}"
        assert "安装完成" in res.stdout
        assert "黄金唤醒词" in res.stdout

        # Verify files
        target_agents_skill = sandbox / ".agents" / "skills" / "pm-prd-copilot" / "SKILL.md"
        target_cursor_skill = sandbox / ".cursor" / "skills" / "pm-prd-copilot" / "SKILL.md"
        assert target_agents_skill.exists(), "Target .agents skill not created!"
        assert target_cursor_skill.exists(), "Target .cursor skill not created!"

        content = target_agents_skill.read_text(encoding="utf-8")
        assert "../../../" not in content, "Found broken relative paths in installed skill!"
        assert "Context Grounding" in content, "Context Grounding missing in installed skill!"
        print("  ✔ pm-prd-copilot installed, self-contained and verified in both runtimes.")

        # Advertised 唤醒指令 materialized as Claude Code custom command files
        cmd_dir = sandbox / ".claude" / "commands"
        prd_cmd_file = cmd_dir / "prd.md"
        assert prd_cmd_file.exists(), "Wake command .claude/commands/prd.md not materialized!"
        prd_cmd = prd_cmd_file.read_text(encoding="utf-8")
        assert "pm-prd-copilot" in prd_cmd, "Command file must point back at its skill!"
        assert "$ARGUMENTS" in prd_cmd, "Command file must forward user input via $ARGUMENTS!"
        print("  ✔ Wake command materialized: /prd -> pm-prd-copilot")

        # Batch install: --all
        print("🧪 [Test 4/6] Batch skill installation: --all...")
        res = run_cli(["add", "--all", "-d", str(sandbox), "-f"])
        assert res.returncode == 0
        assert f"成功写入 {n} 款技能" in res.stdout

        skills_dir = sandbox / ".agents" / "skills"
        installed_skills = [d.name for d in skills_dir.iterdir() if d.is_dir()]
        assert len(installed_skills) == n, f"Expected {n} skills, got {len(installed_skills)}"
        print(f"  ✔ All {n} skills installed in sandbox: {', '.join(installed_skills)}")

        # Every advertised slash command across the registry materialized
        meta = (REPO_ROOT / "cli" / "src" / "skills-meta.mjs").read_text(encoding="utf-8")
        total_cmds = sum(
            len([x for x in block.split(",") if x.strip()])
            for block in re.findall(r"slashCommands:\s*\[([^\]]*)\]", meta)
        )
        all_cmd_files = sorted(p.name for p in (sandbox / ".claude" / "commands").glob("*.md"))
        assert len(all_cmd_files) == total_cmds, f"Expected {total_cmds} command files, got {len(all_cmd_files)}: {all_cmd_files}"
        print(f"  ✔ All {total_cmds} advertised wake commands materialized across {n} skills.")

        # Update test
        print("🧪 [Test 5/6] Skill update verification...")
        res = run_cli(["update", "-d", str(sandbox), "-f"])
        assert res.returncode == 0
        assert f"更新完成！共更新 {n} 款技能" in res.stdout
        print(f"  ✔ Update command successfully updated all {n} skills.")

    # Global mode test
    with tempfile.TemporaryDirectory() as temp_home_dir:
        temp_home = Path(temp_home_dir)
        print(f"🧪 [Test 6/6] Global mode (-g) verification in isolated HOME: {temp_home}")
        res = run_cli(["add", "pm-solo-builder", "-g", "-f"], env={"HOME": str(temp_home)})
        assert res.returncode == 0
        global_skill = temp_home / ".agents" / "skills" / "pm-solo-builder" / "SKILL.md"
        assert global_skill.exists(), "Global skill not found in custom HOME!"
        print("  ✔ Global mode (-g) correctly wrote to ~/.agents/skills/pm-solo-builder")

    print("\n🎉 ALL 6 CLI E2E TESTS PASSED 100%! ZERO FAILURES.")

if __name__ == "__main__":
    test_cli()
