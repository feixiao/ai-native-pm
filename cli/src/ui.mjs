import readline from 'node:readline';

// ANSI styling helpers (zero dependency, pure terminal escape codes)
export const c = {
  reset: (s) => `\x1b[0m${s}\x1b[0m`,
  bold: (s) => `\x1b[1m${s}\x1b[22m`,
  dim: (s) => `\x1b[2m${s}\x1b[22m`,
  cyan: (s) => `\x1b[36m${s}\x1b[39m`,
  green: (s) => `\x1b[32m${s}\x1b[39m`,
  yellow: (s) => `\x1b[33m${s}\x1b[39m`,
  red: (s) => `\x1b[31m${s}\x1b[39m`,
  magenta: (s) => `\x1b[35m${s}\x1b[39m`,
  gray: (s) => `\x1b[90m${s}\x1b[39m`,
  blue: (s) => `\x1b[34m${s}\x1b[39m`,
  bgBlue: (s) => `\x1b[44m\x1b[37m${s}\x1b[0m`,
  bgCyan: (s) => `\x1b[46m\x1b[30m${s}\x1b[0m`,
};

export function printBanner() {
  console.log(`
${c.cyan(c.bold('🚀 ai-native-pm'))} ${c.dim('v0.1.0')}
${c.gray('AI-Native PM Skills Toolkit for Cursor, Claude Code, Antigravity & Codex')}
`);
}

export function printQuickStartCard(skill, targetPath) {
  const line = '─'.repeat(66);
  console.log(`
${c.cyan('┌' + line + '┐')}
${c.cyan('│')}  ${c.bold(c.green('⚡ 技能就绪 (Skill Ready):'))} ${c.bold(skill.name.padEnd(41))} ${c.cyan('│')}
${c.cyan('│')}  ${c.dim(skill.title.padEnd(52))} ${c.cyan('│')}
${c.cyan('├' + line + '┤')}
${c.cyan('│')}  ${c.bold('📂 安装路径:')} ${c.gray(targetPath.slice(0, 52).padEnd(52))} ${c.cyan('│')}
${c.cyan('│')}                                                                    ${c.cyan('│')}
${c.cyan('│')}  ${c.bold(c.yellow('💡 黄金唤醒词 (Golden Trigger Prompt):'))}                            ${c.cyan('│')}
${c.cyan('│')}  ${c.cyan('“' + skill.goldenTrigger + '”')}
${c.cyan('│')}                                                                    ${c.cyan('│')}
${c.cyan('│')}  ${c.bold('⚡ 快捷指令速查:')} ${c.magenta(skill.slashCommands.join('  ')).padEnd(52)} ${c.cyan('│')}
${c.cyan('│')}  ${c.dim('在 Cursor / Claude Code / Codex 对话框直接粘贴上述唤醒词即可触发。')} ${c.cyan('│')}
${c.cyan('└' + line + '┘')}
`);
}

export function printTable(headers, rows) {
  const colWidths = headers.map((h, i) => {
    return Math.max(h.length, ...rows.map((r) => (r[i] ? String(r[i]).length : 0)));
  });

  const headerLine = headers.map((h, i) => c.bold(h.padEnd(colWidths[i]))).join('   ');
  const divider = colWidths.map((w) => '─'.repeat(w)).join('   ');

  console.log(headerLine);
  console.log(c.gray(divider));
  for (const row of rows) {
    console.log(row.map((cell, i) => String(cell || '').padEnd(colWidths[i])).join('   '));
  }
  console.log();
}

/**
 * Interactive multi-select prompt for terminal
 */
export async function selectSkillsInteractive(skills, defaultSelectedIds = []) {
  if (!process.stdin.isTTY) {
    // Non-interactive fallback: select all
    return skills.map((s) => s.id);
  }

  return new Promise((resolve) => {
    let cursor = 0;
    const selected = new Set(defaultSelectedIds.length > 0 ? defaultSelectedIds : skills.map((s) => s.id));

    readline.emitKeypressEvents(process.stdin);
    process.stdin.setRawMode(true);
    process.stdout.write('\x1b[?25l'); // Hide cursor

    function render(firstTime = false) {
      if (!firstTime) {
        process.stdout.write(`\x1b[${skills.length + 2}A`); // Move cursor up
      }

      console.log(c.bold(c.cyan('? 选择要安装到当前项目的 Agent Skills (按空格切换，按回车确认):')));
      skills.forEach((skill, index) => {
        const isCursor = index === cursor;
        const isChecked = selected.has(skill.id);
        const pointer = isCursor ? c.cyan('❯') : ' ';
        const box = isChecked ? c.green('◉') : c.gray('◯');
        const name = isCursor ? c.bold(c.cyan(skill.name)) : c.bold(skill.name);
        const title = c.dim(`(${skill.title})`);
        console.log(` ${pointer} ${box} ${name} ${title}`);
      });
      console.log(c.dim('  (a: 全选 / 全不选, Enter: 确认安装, q: 退出)'));
    }

    render(true);

    function onKeyPress(_, key) {
      if (key.name === 'q' || (key.ctrl && key.name === 'c')) {
        cleanup();
        console.log('\n' + c.yellow('操作已取消。'));
        process.exit(0);
      } else if (key.name === 'up') {
        cursor = (cursor - 1 + skills.length) % skills.length;
        render();
      } else if (key.name === 'down') {
        cursor = (cursor + 1) % skills.length;
        render();
      } else if (key.name === 'space') {
        const id = skills[cursor].id;
        if (selected.has(id)) {
          selected.delete(id);
        } else {
          selected.add(id);
        }
        render();
      } else if (key.name === 'a') {
        if (selected.size === skills.length) {
          selected.clear();
        } else {
          skills.forEach((s) => selected.add(s.id));
        }
        render();
      } else if (key.name === 'return') {
        cleanup();
        console.log();
        resolve(Array.from(selected));
      }
    }

    function cleanup() {
      process.stdin.removeListener('keypress', onKeyPress);
      process.stdin.setRawMode(false);
      process.stdout.write('\x1b[?25h'); // Restore cursor
    }

    process.stdin.on('keypress', onKeyPress);
  });
}
