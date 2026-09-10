<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="oil-tone：让 AI 文案保持真实、平实、完整和易读">
</p>

`oil-tone` 是一份给 AI 使用的个人文风 Skill。它帮助模型在事实边界内完成中文或英文成稿，减少空泛总结、刻意转折、含糊动作和没有信息的文案感。

它适用于博客、演讲稿、PPT 文案、网站与产品介绍、个人简介、公众号和社交帖子。规则有明确倾向，但不会要求所有内容套用同一种结构。

## 修改效果

| 常见写法 | oil-tone 的处理 |
| --- | --- |
| `主流 AI Coding Agent：先选工作方式` | `主流 AI Coding Agent 的工作方式` |
| `单文件 HTML 的结构：简单，但不随意` | `单文件 HTML 的基本结构` |
| `先把流程搞顺` | 说明需要检查、修改或确认的具体对象 |
| `真正重要的是，我们理解了工具的边界` | 内容说明完成后直接结束 |

这些修改不是为了把句子统一改短，而是删除材料没有支持的态度、节奏和升华，让标题与正文继续提供有效信息。

## 它会检查什么

- 事实是否来自现有材料，第一人称内容是否有依据。
- 面向读者时，是否根据情况自然使用“我们”或“大家”。
- 动词和对象是否准确，是否存在 `搞顺`、`跑起来` 等含糊动作。
- 句子语法、因果关系和操作过程是否完整。
- 段落、换行和列表是否真正提升可读性。
- 标题是否直接说明内容，而不是自行制造文案感。
- 结尾是否添加了没有新信息的感悟或价值总结。
- 是否出现固定开场、空泛重要性、模糊归因、聊天残留和通用乐观结尾等常见 AI 表达。

## 安装

仓库中的 Skill 位于 `skills/oil-tone/`。

在 Codex 中，可以使用内置安装脚本：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo oil-oil/oil-tone \
  --path skills/oil-tone
```

也可以手动安装：

```bash
git clone https://github.com/oil-oil/oil-tone.git
cp -R oil-tone/skills/oil-tone ~/.codex/skills/oil-tone
```

安装后，在下一轮任务中使用 `$oil-tone` 调用。

## 使用

直接把 Skill 和写作任务放在一起：

```text
使用 $oil-tone，把这份产品介绍改成可以直接发布的中文成稿。
```

```text
使用 $oil-tone，检查这份 PPT 文案。保留技术细节，删除空泛标题和总结。
```

```text
使用 $oil-tone，按照我的材料写一篇博客。不要编造个人经历。
```

如果我们准备把它改成自己的文风，可以 fork 仓库，再调整 `skills/oil-tone/SKILL.md` 中的叙述身份、称呼习惯和禁用表达。

## 脚本检查

Skill 附带一个只使用 Python 标准库的检查脚本。`FAIL` 表示已经确认的问题，会让脚本返回失败；`WARN` 表示需要结合上下文判断的常见 AI 表达，不会单独让脚本失败：

```bash
python3 ~/.codex/skills/oil-tone/scripts/tone_lint.py draft.md
```

运行脚本自检：

```bash
python3 ~/.codex/skills/oil-tone/scripts/tone_lint.py --self-test
```

合理表达命中 `WARN` 时可以保留。脚本只能发现已知模式，不能判断事实是否可靠，也不能代替通读和朗读检查。

## 仓库结构

```text
oil-tone/
├── assets/readme/hero.svg
├── skills/oil-tone/
│   ├── agents/openai.yaml
│   ├── scripts/tone_lint.py
│   └── SKILL.md
├── LICENSE
└── README.md
```

## 贡献

如果你发现一类稳定出现的 AI 文案问题，可以提交 Issue 或 PR。请同时提供：

1. 原句。
2. 问题在哪里。
3. 更自然、准确的改法。
4. 这条规则适用和不适用的情况。

这样可以避免为了修复一个例句，增加一条会伤害其他内容的机械规则。

## License

[MIT](./LICENSE)

## 配置、依赖与使用边界

纯文本规范，无脚本安装、外部账号或 API Key 配置；支持能够读取 Markdown Skill 的 Agent。

文风规则不提供事实依据；未确认经历不能写成事实。来源数值与计算矛盾时先核对，不因保留原文而延续错误。

使用示例：

```text
用 oil-tone 润色这篇文章，保留事实和限制。
```

## GitHub 安装

把 [仓库地址](https://github.com/oil-oil/oil-tone) 交给 Agent，要求按 README 安装；也可运行：

```bash
npx skills add oil-oil/oil-tone
```

安装后由宿主重新加载 Skill。
