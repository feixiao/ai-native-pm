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

// Display-width convention (modern terminals): CJK full-width chars = 2 cols,
// emoji/symbols = 2 cols, everything else = 1, ANSI escape codes = 0.
// padEnd is length-based and makes CJK/emoji cells ragged; use these instead.
const WIDE_RANGES = [
  [0x1100, 0x115f], [0x2e80, 0xa4cf], [0xac00, 0xd7a3], [0xf900, 0xfaff],
  [0xfe30, 0xfe4f], [0xff00, 0xff60], [0xffe0, 0xffe6], [0x1f300, 0x1f64f],
  [0x1f680, 0x1f6ff], [0x1f900, 0x1f9ff], [0x2600, 0x26ff], [0x2700, 0x27bf],
  [0x2b00, 0x2bff],
];

function codePointWidth(cp) {
  return WIDE_RANGES.some(([lo, hi]) => cp >= lo && cp <= hi) ? 2 : 1;
}

function displayWidth(s) {
  let w = 0;
  for (const ch of String(s).replace(/\u001b\[[0-9;]*m/g, '')) {
    w += codePointWidth(ch.codePointAt(0));
  }
  return w;
}

function padDisplay(s, width) {
  const pad = width - displayWidth(s);
  return String(s) + (pad > 0 ? ' '.repeat(pad) : '');
}

// Fit text into exactly `width` display columns: pad if short, truncate with a
// 2-col ellipsis if long. ANSI-safe (escape sequences are preserved, not cut).
function fitDisplay(s, width) {
  const str = String(s);
  if (displayWidth(str) <= width) return padDisplay(str, width);
  let w = 0;
  let i = 0;
  let cut = str.length;
  while (i < str.length) {
    const ch = str[i];
    if (ch === '\u001b') {
      const m = /\u001b\[[0-9;]*m/.exec(str.slice(i));
      if (m) { i += m[0].length; continue; }
    }
    const cp = ch.codePointAt(0);
    const cw = codePointWidth(cp);
    if (w + cw > width - 2) { cut = i; break; }
    w += cw;
    i += cp > 0xffff ? 2 : 1;
  }
  return str.slice(0, cut) + '…';
}

export function printQuickStartCard(skill, targetPath) {
  const line = '─'.repeat(66);
  // Every bordered row = │(1) + margin(2) + content(63) + margin(1) + │(1) = 68.
  console.log(`
${c.cyan('┌' + line + '┐')}
${c.cyan('│')}  ${c.bold(c.green('⚡ 技能就绪 (Skill Ready):'))} ${c.bold(fitDisplay(skill.name, 36))} ${c.cyan('│')}
${c.cyan('│')}  ${c.dim(fitDisplay(skill.title, 63))} ${c.cyan('│')}
${c.cyan('├' + line + '┤')}
${c.cyan('│')}  ${c.bold('📂 安装路径:')} ${c.gray(fitDisplay(targetPath, 50))}  ${c.cyan('│')}
${c.cyan('│')}                                                                  ${c.cyan('│')}
${c.cyan('│')}  ${c.bold(c.yellow('💡 黄金唤醒词 (Golden Trigger Prompt):'))}                          ${c.cyan('│')}
${c.cyan('│')}  ${c.cyan('“' + skill.goldenTrigger + '”')}
${c.cyan('│')}                                                                  ${c.cyan('│')}
${c.cyan('│')}  ${c.bold('⚡ 快捷指令速查:')} ${c.magenta(fitDisplay(skill.slashCommands.join('  '), 46))} ${c.cyan('│')}
${c.cyan('│')}  ${c.dim(padDisplay('已落盘 .claude/commands 与 .cursor/commands,斜杠触发', 63))} ${c.cyan('│')}
${c.cyan('└' + line + '┘')}
`);
}

export function printTable(headers, rows) {
  // Columns sized by display width (CJK/emoji = 2 cols), so CJK cells never
  // push adjacent columns off; over-long cells are ellipsis-truncated.
  const colWidths = headers.map((h, i) =>
    Math.max(displayWidth(h), ...rows.map((r) => displayWidth(String(r[i] ?? '')))));

  const headerLine = headers.map((h, i) => c.bold(fitDisplay(h, colWidths[i]))).join('   ');
  const divider = colWidths.map((w) => '─'.repeat(w)).join('   ');

  console.log(headerLine);
  console.log(c.gray(divider));
  for (const row of rows) {
    console.log(row.map((cell, i) => fitDisplay(String(cell ?? ''), colWidths[i])).join('   '));
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
