#!/usr/bin/env python3
"""
E2E Sandbox Automated Test for ai-native-pm CLI
Verifies:
1. Fresh target project: list shows uninstalled
2. Single skill installation (pm-prd-copilot): checks .agents and .cursor directories, zero broken relative links, wake commands materialized into BOTH .claude/commands/*.md and .cursor/commands/*.md pointing back at the skill
3. Batch installation (--all): all 7 skills installed
4. Safe conflict handling and --force update
5. Global mode (-g) with isolated HOME environment
6. CJK-aware layout: rendered quick-start card and skill table have uniform
   display widths (CJK/emoji = 2 cols) — ragged borders are a visible defect
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

# Mirrors the CLI's display-width convention (cli/src/ui.mjs): CJK = 2 cols,
# emoji/symbols = 2 cols, ANSI escapes = 0.
WIDE_RANGES = [
    (0x1100, 0x115F), (0x2E80, 0xA4CF), (0xAC00, 0xD7A3), (0xF900, 0xFAFF),
    (0xFE30, 0xFE4F), (0xFF00, 0xFF60), (0xFFE0, 0xFFE6), (0x1F300, 0x1F64F),
    (0x1F680, 0x1F6FF), (0x1F900, 0x1F9FF), (0x2600, 0x26FF), (0x2700, 0x27BF),
    (0x2B00, 0x2BFF),
]

def display_width(s):
    s = re.sub(r"\x1b\[[0-9;]*m", "", s)
    return sum(2 if any(lo <= ord(ch) <= hi for lo, hi in WIDE_RANGES) else 1
               for ch in s)

def assert_uniform_lines(lines, what):
    widths = {display_width(l.rstrip()) for l in lines if l.strip()}
    assert len(widths) == 1, f"{what} rows have ragged widths: {sorted(widths)} -> {lines[:4]}"
    return widths

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
    print("🧪 [Test 1/7] CLI --help & --version basic check...")
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
        print(f"🧪 [Test 2/7] Fresh sandbox project check: {sandbox}")

        # List in empty sandbox
        res = run_cli(["list", "-d", str(sandbox)])
        assert res.returncode == 0
        assert "未安装" in res.stdout
        print("  ✔ Empty sandbox correctly reports uninstalled.")

        # Single install: pm-prd-copilot
        print("🧪 [Test 3/7] Single skill installation: pm-prd-copilot...")
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

        # Dual-runtime parity: same command also materialized for Cursor
        cursor_cmd_file = sandbox / ".cursor" / "commands" / "prd.md"
        assert cursor_cmd_file.exists(), "Wake command .cursor/commands/prd.md not materialized!"
        cursor_cmd = cursor_cmd_file.read_text(encoding="utf-8")
        assert "pm-prd-copilot" in cursor_cmd, "Cursor command file must point back at its skill!"
        print("  ✔ Wake commands materialized in BOTH runtimes: .claude/commands + .cursor/commands")

        # Batch install: --all
        print("🧪 [Test 4/7] Batch skill installation: --all...")
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
        cursor_cmd_files = sorted(p.name for p in (sandbox / ".cursor" / "commands").glob("*.md"))
        assert len(cursor_cmd_files) == total_cmds, f"Expected {total_cmds} Cursor command files, got {len(cursor_cmd_files)}: {cursor_cmd_files}"
        print(f"  ✔ All {total_cmds} advertised wake commands materialized across {n} skills (both runtimes).")

        # Update test
        print("🧪 [Test 5/7] Skill update verification...")
        res = run_cli(["update", "-d", str(sandbox), "-f"])
        assert res.returncode == 0
        assert f"更新完成！共更新 {n} 款技能" in res.stdout
        print(f"  ✔ Update command successfully updated all {n} skills.")

    # Global mode test
    with tempfile.TemporaryDirectory() as temp_home_dir:
        temp_home = Path(temp_home_dir)
        print(f"🧪 [Test 6/7] Global mode (-g) verification in isolated HOME: {temp_home}")
        res = run_cli(["add", "pm-solo-builder", "-g", "-f"], env={"HOME": str(temp_home)})
        assert res.returncode == 0
        global_skill = temp_home / ".agents" / "skills" / "pm-solo-builder" / "SKILL.md"
        assert global_skill.exists(), "Global skill not found in custom HOME!"
        claude_cmds = sorted(p.name for p in (temp_home / ".claude" / "commands").glob("*.md"))
        cursor_cmds = sorted(p.name for p in (temp_home / ".cursor" / "commands").glob("*.md"))
        assert len(claude_cmds) == len(cursor_cmds) > 0, \
            f"Global wake commands must be materialized for BOTH runtimes: claude={claude_cmds} cursor={cursor_cmds}"
        print(f"  ✔ Global mode (-g) wrote skill + {len(claude_cmds)} wake commands to BOTH ~/.claude/commands and ~/.cursor/commands")

    # CJK-aware layout: rendered card + table must have uniform display widths
    with tempfile.TemporaryDirectory() as temp_project_dir:
        sandbox = Path(temp_project_dir)
        print("🧪 [Test 7/7] CJK-aware layout: rendered card + table width uniformity...")
        res = run_cli(["add", "pm-operations", "-d", str(sandbox), "-f"])
        assert res.returncode == 0
        card_rows, box = [], False
        for l in res.stdout.split("\n"):
            t = re.sub(r"\x1b\[[0-9;]*m", "", l).rstrip()
            if "┌" in t:
                box = True
            if box:
                card_rows.append(t)
                if "└" in t:
                    box = False
        bordered = [r for r in card_rows if r and r[-1] in "│┤├┌└┐┘"]
        assert len(bordered) >= 8, f"Expected 8 bordered card rows, got {len(bordered)}"
        assert_uniform_lines(bordered, "quick-start card")
        res = run_cli(["list", "-d", str(sandbox)])
        assert res.returncode == 0
        tbl, collecting = [], False
        for l in res.stdout.split("\n"):
            t = re.sub(r"\x1b\[[0-9;]*m", "", l)
            if "本地状态" in t:
                collecting = True
            if collecting:
                if not t.strip():
                    break
                tbl.append(t)
        assert len(tbl) >= n + 2, f"Skill table too short: {len(tbl)} rows"
        assert_uniform_lines(tbl, "skill table")
        print("  ✔ Quick-start card + skill table render at uniform display width (CJK/emoji-aware).")

    print("\n🎉 ALL 7 CLI E2E TESTS PASSED 100%! ZERO FAILURES.")

if __name__ == "__main__":
    test_cli()
