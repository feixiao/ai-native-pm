#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const sourceDir = path.resolve(__dirname, '../../.agents/skills');
const targetDir = path.resolve(__dirname, '../skills');

if (!fs.existsSync(sourceDir)) {
  console.error(`Source directory not found: ${sourceDir}`);
  process.exit(1);
}

fs.rmSync(targetDir, { recursive: true, force: true });
fs.mkdirSync(targetDir, { recursive: true });

fs.cpSync(sourceDir, targetDir, { recursive: true });
console.log(`✔ Successfully synced skills from ${sourceDir} to ${targetDir}`);
