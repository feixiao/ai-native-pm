import path from 'node:path';
import { SKILLS, SKILL_MAP } from './skills-meta.mjs';
import { c, printBanner, printQuickStartCard, printTable, selectSkillsInteractive } from './ui.mjs';
import { installSkill, updateSkill, isSkillInstalled, resolveTargetDirs } from './installer.mjs';

function parseArgs(args) {
  const result = {
    command: '',
    params: [],
    flags: {
      all: false,
      global: false,
      force: false,
      dir: '',
      help: false,
      version: false,
    },
  };

  let i = 0;
  while (i < args.length) {
    const arg = args[i];
    if (arg === '--all' || arg === '-a') {
      result.flags.all = true;
    } else if (arg === '--global' || arg === '-g') {
      result.flags.global = true;
    } else if (arg === '--force' || arg === '-f') {
      result.flags.force = true;
    } else if (arg === '--dir' || arg === '-d') {
      result.flags.dir = args[++i];
    } else if (arg === '--help' || arg === '-h') {
      result.flags.help = true;
    } else if (arg === '--version' || arg === '-v') {
      result.flags.version = true;
    } else if (!result.command && !arg.startsWith('-')) {
      result.command = arg;
    } else if (!arg.startsWith('-')) {
      result.params.push(arg);
    }
    i++;
  }

  return result;
}

function printHelp() {
  printBanner();
  console.log(`
${c.bold('用法 (Usage):')}
  ${c.cyan('npx ai-native-pm')} ${c.yellow('<command>')} ${c.gray('[options]')}

${c.bold('核心命令 (Commands):')}
  ${c.green('add [skills...]')}      安装指定技能（默认交互式多选，支持 --all）
  ${c.green('list, ls')}             列出所有官方技能及本地工程安装状态
  ${c.green('info <skill>')}         查看指定技能的详细卡片与黄金唤醒词
  ${c.green('update [skills...]')}   检查并更新本地已安装的技能至最新版本

${c.bold('常用选项 (Options):')}
  ${c.yellow('--all, -a')}           一键安装/更新全部 ${SKILLS.length} 大 PM 技能
  ${c.yellow('--global, -g')}        安装到个人用户全局目录 (~/.agents/skills, ~/.claude/commands, ~/.cursor/commands)
  ${c.yellow('--force, -f')}         覆盖已有技能而不提示确认
  ${c.yellow('--dir, -d <path>')}    指定目标工程根目录 (默认当前工作区)
  ${c.yellow('--help, -h')}          查看命令帮助
  ${c.yellow('--version, -v')}       查看当前版本

${c.bold('极速示例 (Quick Examples):')}
  ${c.dim('# 交互式选择安装到当前工程')}
  ${c.cyan('npx ai-native-pm add')}

  ${c.dim('# 一键全量安装到当前项目')}
  ${c.cyan('npx ai-native-pm add --all')}

  ${c.dim('# 按需单独安装 PRD 审查技能')}
  ${c.cyan('npx ai-native-pm add pm-prd-copilot')}

  ${c.dim('# 全局安装独立开发闭环技能')}
  ${c.cyan('npx ai-native-pm add pm-solo-builder -g')}

  ${c.dim('# 查看当前工程中已安装的技能')}
  ${c.cyan('npx ai-native-pm list')}
`);
}

async function handleList(flags) {
  printBanner();
  const { isGlobal, baseDir } = resolveTargetDirs(flags);
  console.log(`${c.bold('📍 目标工作区:')} ${c.cyan(baseDir)} ${isGlobal ? c.yellow('(全局模式)') : ''}\n`);

  const headers = ['技能名称 (ID)', '中文分类与核心职能', '本地状态'];
  const rows = SKILLS.map((s) => {
    const installed = isSkillInstalled(s.id, flags);
    const statusText = installed ? c.green('✔ 已安装') : c.gray('未安装');
    return [c.bold(s.name), `${s.title}`, statusText];
  });

  printTable(headers, rows);
  console.log(c.dim(`💡 安装技能请执行: npx ai-native-pm add <skill-name> 或 npx ai-native-pm add --all`));
}

async function handleInfo(skillId) {
  if (!skillId) {
    console.error(c.red('❌ 请提供技能名称，例如: npx ai-native-pm info pm-prd-copilot'));
    process.exit(1);
  }

  const skill = SKILL_MAP.get(skillId);
  if (!skill) {
    console.error(c.red(`❌ 未找到技能: ${skillId}。可运行 npx ai-native-pm list 查看可用列表。`));
    process.exit(1);
  }

  printBanner();
  console.log(`${c.bold('📦 技能详情:')} ${c.cyan(skill.name)} - ${c.bold(skill.title)}`);
  console.log(`${c.bold('📝 核心职能:')} ${skill.desc}`);
  console.log(`${c.bold('🏷️ 类别:')} ${c.magenta(skill.category)}`);
  console.log(`${c.bold('⚡ 唤醒指令:')} ${c.yellow(skill.slashCommands.join('  '))}\n`);
  printQuickStartCard(skill, './.agents/skills/' + skill.id);
}

async function handleAdd(params, flags) {
  printBanner();
  let selectedSkillIds = [];

  if (flags.all) {
    selectedSkillIds = SKILLS.map((s) => s.id);
  } else if (params.length > 0) {
    // Validate provided params
    for (const p of params) {
      if (!SKILL_MAP.has(p)) {
        console.error(c.red(`❌ 未知技能: ${p}。请运行 npx ai-native-pm list 查看支持的技能清单。`));
        process.exit(1);
      }
    }
    selectedSkillIds = params;
  } else {
    // Interactive multi-select
    selectedSkillIds = await selectSkillsInteractive(SKILLS);
  }

  if (selectedSkillIds.length === 0) {
    console.log(c.yellow('⚠️ 未选择任何技能，安装流程结束。'));
    return;
  }

  const { baseDir, isGlobal } = resolveTargetDirs(flags);
  console.log(`${c.bold('🚀 开始注入技能至:')} ${c.cyan(baseDir)} ${isGlobal ? c.yellow('(全局模式)') : ''}\n`);

  const installedResults = [];

  for (const id of selectedSkillIds) {
    const skill = SKILL_MAP.get(id);
    try {
      const res = await installSkill(skill, flags);
      if (res.status === 'skipped') {
        console.log(`  ${c.gray('◯')} ${c.dim(skill.name)} ${c.yellow('[已跳过/已存在]')}`);
      } else {
        console.log(`  ${c.green('✔')} ${c.bold(skill.name)} ➔ ${c.gray(res.path)}`);
        if (res.commands && res.commands.length > 0) {
          const names = [...new Set(res.commands.map((f) => path.basename(f, '.md')))]
            .map((nm) => c.cyan(`/${nm}`)).join('  ');
          console.log(`      ${c.yellow('⚡ 唤醒指令:')} ${names} ${c.gray('→ .claude/commands + .cursor/commands')}`);
        }
        installedResults.push(res);
      }
    } catch (err) {
      console.error(`  ${c.red('✖')} ${skill.name} 安装失败: ${err.message}`);
    }
  }

  console.log(`\n${c.bold(c.green(`✨ 安装完成！成功写入 ${installedResults.length} 款技能。`))}`);

  // Print Quick-Start Cards for newly installed skills
  if (installedResults.length > 0) {
    console.log(c.bold('\n' + '═'.repeat(68)));
    console.log(c.bold(c.yellow('  🎯 10秒秒懂卡片：复制以下【黄金唤醒词】在 Cursor/Claude 中即刻体验！')));
    console.log(c.bold('═'.repeat(68)));
    for (const res of installedResults) {
      printQuickStartCard(res.skill, res.path);
    }
  }
}

async function handleUpdate(params, flags) {
  printBanner();
  const { baseDir, isGlobal } = resolveTargetDirs(flags);
  console.log(`${c.bold('🔄 正在检查并更新技能:')} ${c.cyan(baseDir)} ${isGlobal ? c.yellow('(全局模式)') : ''}\n`);

  let targetSkillIds = [];
  if (params.length > 0) {
    targetSkillIds = params;
  } else {
    // Find all currently installed skills
    targetSkillIds = SKILLS.filter((s) => isSkillInstalled(s.id, flags)).map((s) => s.id);
  }

  if (targetSkillIds.length === 0) {
    console.log(c.yellow('⚠️ 本地尚未安装任何 ai-native-pm 技能。请先使用 npx ai-native-pm add 安装。'));
    return;
  }

  let updatedCount = 0;
  for (const id of targetSkillIds) {
    const skill = SKILL_MAP.get(id);
    if (!skill) continue;
    try {
      const res = await updateSkill(skill, flags);
      console.log(`  ${c.green('✔')} 已更新 ${c.bold(skill.name)} ➔ ${c.gray(res.path)}`);
      updatedCount++;
    } catch (err) {
      console.error(`  ${c.red('✖')} 更新 ${skill.name} 失败: ${err.message}`);
    }
  }

  console.log(`\n${c.bold(c.green(`✨ 更新完成！共更新 ${updatedCount} 款技能至最新版本。`))}`);
}

export async function run(args = process.argv.slice(2)) {
  const parsed = parseArgs(args);

  if (parsed.flags.version) {
    console.log('ai-native-pm v0.1.0');
    return;
  }

  if (parsed.flags.help || (!parsed.command && parsed.params.length === 0 && !parsed.flags.all)) {
    printHelp();
    return;
  }

  switch (parsed.command) {
    case 'add':
    case 'install':
      await handleAdd(parsed.params, parsed.flags);
      break;
    case 'list':
    case 'ls':
      await handleList(parsed.flags);
      break;
    case 'info':
      await handleInfo(parsed.params[0]);
      break;
    case 'update':
    case 'upgrade':
      await handleUpdate(parsed.params, parsed.flags);
      break;
    default:
      console.error(c.red(`❌ 未知命令: "${parsed.command}"\n`));
      printHelp();
      process.exit(1);
  }
}
