import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import readline from 'node:readline';
import { fileURLToPath } from 'node:url';
import { c } from './ui.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export function getSourceSkillsDir() {
  // First check bundled skills/ in cli package
  const bundled = path.resolve(__dirname, '../skills');
  if (fs.existsSync(bundled)) {
    return bundled;
  }
  // Fallback to repo root .agents/skills during development
  const repoRootSkills = path.resolve(__dirname, '../../../.agents/skills');
  if (fs.existsSync(repoRootSkills)) {
    return repoRootSkills;
  }
  throw new Error('Skills source directory not found. Please run npm run sync-skills.');
}

export function resolveTargetDirs(options = {}) {
  const isGlobal = Boolean(options.global);
  const baseDir = isGlobal ? os.homedir() : (options.dir ? path.resolve(options.dir) : process.cwd());

  return {
    isGlobal,
    baseDir,
    agentsSkillsDir: path.join(baseDir, '.agents', 'skills'),
    cursorSkillsDir: path.join(baseDir, '.cursor', 'skills'),
  };
}

export function isSkillInstalled(skillId, options = {}) {
  const { agentsSkillsDir, cursorSkillsDir } = resolveTargetDirs(options);
  const inAgents = fs.existsSync(path.join(agentsSkillsDir, skillId, 'SKILL.md'));
  const inCursor = fs.existsSync(path.join(cursorSkillsDir, skillId, 'SKILL.md'));
  return inAgents || inCursor;
}

async function promptOverwrite(skillId) {
  if (!process.stdin.isTTY) {
    return false;
  }
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  return new Promise((resolve) => {
    rl.question(c.yellow(`⚠️  技能 ${skillId} 已存在，是否覆盖? (y/N): `), (answer) => {
      rl.close();
      resolve(answer.trim().toLowerCase() === 'y');
    });
  });
}

export async function installSkill(skill, options = {}) {
  const sourceDir = getSourceSkillsDir();
  const skillSourcePath = path.join(sourceDir, skill.id);

  if (!fs.existsSync(skillSourcePath)) {
    throw new Error(`Skill source not found: ${skillSourcePath}`);
  }

  const { agentsSkillsDir, cursorSkillsDir, isGlobal, baseDir } = resolveTargetDirs(options);
  const targetAgentsSkillPath = path.join(agentsSkillsDir, skill.id);
  const targetCursorSkillPath = path.join(cursorSkillsDir, skill.id);

  // Check existing
  if (fs.existsSync(targetAgentsSkillPath) && !options.force) {
    const overwrite = await promptOverwrite(skill.id);
    if (!overwrite) {
      return { skill, status: 'skipped', path: targetAgentsSkillPath };
    }
  }

  // 1. Ensure target directory and copy to .agents/skills/<id>
  fs.mkdirSync(targetAgentsSkillPath, { recursive: true });
  fs.cpSync(skillSourcePath, targetAgentsSkillPath, { recursive: true });

  // 2. Ensure .cursor/skills/ compatibility
  fs.mkdirSync(cursorSkillsDir, { recursive: true });
  try {
    if (fs.existsSync(targetCursorSkillPath)) {
      // Remove existing symlink or folder
      fs.rmSync(targetCursorSkillPath, { recursive: true, force: true });
    }

    // Try relative symlink first (standard on Unix/macOS)
    const relativeTarget = path.relative(cursorSkillsDir, targetAgentsSkillPath);
    fs.symlinkSync(relativeTarget, targetCursorSkillPath, 'junction');
  } catch {
    // If symlink fails (e.g. Windows non-admin permissions), fallback to physical copy
    try {
      fs.mkdirSync(targetCursorSkillPath, { recursive: true });
      fs.cpSync(skillSourcePath, targetCursorSkillPath, { recursive: true });
    } catch (e) {
      // Non-fatal warning
      console.warn(c.yellow(`⚠️  Warning: Unable to link cursor skills: ${e.message}`));
    }
  }

  return {
    skill,
    status: 'installed',
    path: targetAgentsSkillPath,
    isGlobal,
    baseDir,
  };
}

export async function updateSkill(skill, options = {}) {
  // Update forces overwrite
  return installSkill(skill, { ...options, force: true });
}
