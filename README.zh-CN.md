# Agent Control Plane

[English](./README.md) | [简体中文](./README.zh-CN.md)

面向多智能体本地协作的文件化控制平面，核心强调团队管理、可进化记忆体系，以及多设备控制。

难的从来不是 prompt，本项目真正解决的是 prompt 之外的那一层基础设施：

- 稳定的 worker 身份
- 清晰的任务交接
- 可持续的记忆管理
- 可审计的协作流程
- 上下文丢失后的恢复能力
- 跨机器迁移时无需重建全部环境

Agent Control Plane 是一个轻量、文件驱动的框架，用来解决这些问题，而不是再堆一个笨重的后端。

<p align="center">
  <img src="./docs/assets/dashboard-preview.png" alt="桌面管理面板截图" width="92%">
</p>

<p align="center">
  <img src="./docs/assets/desktop-chat-preview.png" alt="桌面控制聊天截图" width="92%">
</p>

<p align="center">
  <img src="./docs/assets/mobile-chat-preview.png" alt="移动端控制聊天截图" width="52%">
</p>

> 这三张截图来自建立在当前文件化控制核心之上的高保真静态原型：桌面管理面板、桌面控制聊天、记忆管理中心，以及移动端运营聊天界面。

## 项目亮点

### 1. 多 Agent 团队管理

这个项目把 agent 当成真实协作团队来管理，而不是一堆彼此割裂的聊天窗口。

- 明确的 worker 身份与角色
- 可发现的 worker registry
- 可视化的队列与 handoff 状态
- 可跨本地与项目作用域迁移的监督结构

### 2. 可进化的记忆管理体系

这里的记忆不是临时缓存，而是能够增长、恢复、迭代的系统能力。

- session memory 保存当前工作上下文
- rule-linked governance material 固化长期规则
- 可移植 `_agent_profile` snapshots 用于恢复与迁移
- durable audit/recovery 路径支撑长期演化

### 3. 多设备同步与移动端远程沟通

同一套控制平面可以同时支撑桌面面板、桌面聊天和移动端远程操作。

- 一套 durable state model 贯穿所有设备
- 支持手机上的远程审批与状态查看
- 记忆、handoff、队列状态跨设备同步
- 离开主工作站时也能安全沟通和决策

## 你会得到什么

- 具备明确身份、记忆、状态和通信文件的 worker body 目录
- 根据 `worker-profile.json` 自动生成的 worker registry
- 用于迁移、恢复与审计的可移植 `_agent_profile` 快照
- 支持项目级 worker 与下级 worker 的分层结构
- 易于 diff、检查和自动化处理的纯文本协作模型
- 一套基于 durable worker files 的内建记忆管理系统，而不是依赖易失聊天上下文
- 在不改变底层数据模型的前提下，平滑扩展到桌面面板、桌面聊天和移动端控制界面

## 产品支柱

### 1. 多 Agent 团队管理

整个系统天然适合承载一个密集型 controller 视图，集中展示：

- 活跃 workers
- 任务队列
- 交接状态
- 监督结构
- 快照覆盖率

### 2. 可进化的记忆管理系统

在这里，记忆不是附属品，而是一等公民。

Agent Control Plane 已经通过这些文件组织起完整的记忆体系：

- `memory/session_memory.md`
- 与治理规则绑定的 references
- `_agent_profile` snapshots
- 可移植的审计与恢复文件

这也意味着后续可以自然长出：

- 记忆审查面板
- retention 健康检查
- worker 恢复流程
- 面向不同角色的记忆视图

### 3. 多设备同步与移动端沟通

长期来看，这个项目会扩展到一组同步的 operator 界面，用于：

- 桌面管理面板
- 桌面控制聊天
- 手机状态检查
- 手机审批与告警
- 随时随地查看 handoff

## 适合谁

- 在本地运行多个编码 agent 的团队
- 想要可审计、文件化 agent 运维方式的维护者
- 需要可复现 worker 配置的研究者和构建者
- 厌倦把协作状态困在聊天记录里的人

## 为什么做这个项目

大多数多智能体系统失败的方式，其实都很朴素：

- 一个 worker 只存在于某个聊天标签页
- 没人知道哪些文件才是它的正式定义
- handoff 存在脑子里，而不是可追踪记录里
- 迁移机器时只能手动重建 prompt、上下文和规则

这个项目把 worker 运维当成真正的基础设施：

- 身份显式
- 记忆落盘
- 治理可检查
- 快照可迁移

## 为什么文件化记忆更强

很多 agent 系统丢失有价值的记忆，是因为记忆被困在会话里。

本项目把记忆推进到一组可持续、可检查、可迁移的工件中：

- 当前工作上下文通过 session memory 保存
- 长期规则通过 governance references 固化
- 迁移与恢复通过 snapshots 兜底
- 角色与监督关系通过 registry 表达

这让你拥有了一样在 agent tooling 里非常稀缺的能力：真正的记忆管理系统，而不是脆弱的聊天缓存。

## 快速开始

### 1. 创建环境

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e .
```

### 2. 构建 worker registry

```powershell
.venv\Scripts\agent-control-plane sync-registry `
  --coord-root coordination `
  --workers-root examples/local-workers `
  --scan-root examples/projects
```

### 3. 生成可移植 worker profiles

```powershell
.venv\Scripts\agent-control-plane snapshot-profiles `
  --coord-root coordination `
  --workers-root examples/local-workers `
  --scan-root examples/projects
```

### 4. 查看结果

- `coordination/registry.json` 会保存自动发现的 workers
- 每个示例 worker body 都会生成一层 `_agent_profile/` 快照

## 示例目录结构

```text
agent-control-plane-oss/
  coordination/
    registry.json
    prompts/
  examples/
    local-workers/
    projects/
  src/
    agent_control_plane/
  templates/
  tests/
```

示例 worker body：

```text
worker-body/
  worker-profile.json
  status/
    controller-link.md
  memory/
    session_memory.md
  inbox/
  outbox/
  reports/
  _agent_profile/
```

## 命令

- `agent-control-plane sync-registry`
  自动发现 workers 并重建共享 registry

- `agent-control-plane snapshot-profiles`
  根据 worker body 文件生成可移植 `_agent_profile` 快照

## 界面方向

当前仓库已经提供了支撑更丰富产品表面的后端脚手架。

后续计划中的界面层包括：

- 桌面管理面板
- 桌面控制聊天界面
- 记忆管理中心
- 移动端运营聊天界面
- 多设备同步视图
- 任务与审批面板

上面的截图来自高保真静态原型，而本仓库中的代码已经实现了它们背后的文件化协调模型。

## 设计原则

- Files first
  协作状态应该能穿越聊天重置和工具切换。

- Lightweight bodies
  Worker body 应该保存治理资料，而不是变成项目杂物间。

- Generated registries
  既然真实来源已经在 worker profile 里，就不应该手工维护 registry。

- Portable snapshots
  恢复与迁移应该是日常操作，而不是英雄主义。

## 通用角色命名

示例工作区故意使用了中性角色名：

- `controller`
- `profile-manager`
- `ops-manager`
- `worker-a`
- `worker-b`

克隆后你可以替换成自己的命名体系。

## 文档

- [Architecture](./docs/architecture.md)
- [Worker Profile](./docs/worker-profile.md)
- [Governance Model](./docs/governance.md)
- [Contributing](./CONTRIBUTING.md)
- [Security Policy](./SECURITY.md)

## 项目状态

`v0.1.0` 是第一个公开骨架版本。

它已经包含：

- 可用的 CLI
- 示例 worker bodies
- registry generation
- profile snapshot generation
- tests and CI
- durable memory management model
- 面向桌面与移动端控制表面的视觉方向
- 围绕团队管理、可进化记忆与远程沟通构建的产品叙事

下一波很可能聚焦于：

- 更强的 validation
- task/result 文件辅助工具
- 真正可交互的管理面板
- 手机版控制页与聊天界面
- 更严格的 schema tooling

## License

MIT
