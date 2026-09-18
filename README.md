# Rhino Architectural Reverse Modeling — Mode A

[中文](#中文说明) · [English](#english)

## 中文说明

一个面向 Codex / Claude Code 的建筑反向建模 skill：根据照片、口述或文字描述、尺寸和平立剖资料，建立**准确、精细、可编辑**的建筑模型。默认使用 Rhino MCP 并交付 `.3dm`；用户明确指定其他软件时沿用其选择。

它不是摄影测量工具，也不是固定步骤的建模教程。Skill 约定成果质量、证据边界和交付要求，同时让模型根据建筑特征自主选择几何方法、工具与执行顺序。

### 核心能力

- 从单张或多张照片中辨认主体轮廓、开口、体块、遮挡、投影和空间关系。
- 把口述设计、尺寸和混合资料转成可修改的控制几何与构件系统。
- 区分用户给定、图像量取和建筑逻辑推断，不把未知信息包装成实测结果。
- 检查主体形态、尺度、建筑装配、交通联系、材质映射、场地关系和可编辑性。
- 交付可回读的原生模型、命名视图、最终模型实际渲染的主视角与辅助视角，以及简短交接说明。
- 在高返工风险节点使用可选的独立审核与图像比较工具，避免把流程完成当成模型准确。

### 仓库结构

```text
rhino-architectural-reverse-modeling-mode-a/
├── SKILL.md
├── REVIEWER.md
├── TOOLING.md
├── references/
│   ├── application-tools.md
│   ├── architectural-construction-logic.md
│   ├── checks.md
│   ├── form-verification.md
│   ├── material-review-display.md
│   ├── strict-review.md
│   └── typological-constraints.md
└── tools/
    ├── compare_views.py
    ├── reference_prep.py
    ├── register_capture.py
    └── review_packet.py
```

- [`SKILL.md`](rhino-architectural-reverse-modeling-mode-a/SKILL.md)：任务边界、质量目标、验证原则、资源路由与交付要求。
- `references/`：按需加载的形态、尺度、构造、材质、软件接口与专项核验知识。
- `REVIEWER.md`：面向独立审核者的检查指引。
- `TOOLING.md`：Rhino MCP 的执行、显示、保存和回读注意事项。
- `tools/`：可选的参考图预处理、视图比较、捕捉配准和审核包工具。

### 安装

Codex 项目级安装：

```bash
git clone https://github.com/frankee0920-rgb/rhino-architectural-reverse-modeling.git
cp -r rhino-architectural-reverse-modeling/rhino-architectural-reverse-modeling-mode-a \
  /path/to/your-project/.agents/skills/
```

Claude Code 项目级安装：

```bash
cp -r rhino-architectural-reverse-modeling/rhino-architectural-reverse-modeling-mode-a \
  /path/to/your-project/.claude/skills/
```

也可以把该文件夹复制到宿主的用户级 skills 目录。

### 使用方式

提供以下信息中的任意组合：

- 建筑照片或平、立、剖图；
- 口述或文字设计要求；
- 已知尺寸、层高、层数或标高；
- 目标软件、建模范围、场景范围与交付要求。

示例：

> 根据这些照片，在 Rhino 中建立精细化建筑模型。总高 36 米，完成整栋外观和近场铺地；内部按资料能够判断的关系概括。保留主要形态和幕墙模块的编辑控制，交付 `.3dm`、匹配第一张照片的主视角渲染、一个互补辅助视角和简短交接说明。

### 环境与依赖

- 支持 skills 的 Codex、Claude Code 或兼容宿主。
- 使用 Rhino 路径时，需要可用的 Rhino MCP 连接；本仓库不附带 Rhino 或 MCP 服务端。
- 辅助脚本需要 Python 3；图像工具另需 Pillow 和 NumPy：

```bash
python -m pip install pillow numpy
```

`TOOLING.md` 中的经验主要来自 Rhino 8。单张照片不能唯一恢复隐藏几何或绝对尺度；Skill 会要求使用已知尺度、明确的暂定尺度，或标注合理推断。

## English

This repository contains a Codex / Claude Code skill for producing accurate, detailed, and editable architectural models from photographs, written or spoken briefs, dimensions, and mixed references. Rhino MCP and native `.3dm` delivery are the default; an explicitly requested alternative application is preserved.

The skill defines outcome quality, evidence boundaries, validation, and deliverables without forcing a rigid modeling sequence. It includes focused references for form verification, scale transfer, architectural assembly, materials, tool behavior, and independent review, plus optional Python helpers for image preparation and comparison.

Install the `rhino-architectural-reverse-modeling-mode-a` folder in your host's project-level or user-level skills directory. For the full operating contract, start with [`SKILL.md`](rhino-architectural-reverse-modeling-mode-a/SKILL.md).

## License

MIT — see [LICENSE](LICENSE).
