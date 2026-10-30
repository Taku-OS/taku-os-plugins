# TakuOS 社区插件

[English](README.md) · **简体中文**

插件能让 TakuOS 手机上的 Agent 学会新本事，这个仓库就是大家分享插件的地方。

想法很简单：你在手机上搞定了一件有用的事——一个提醒、一套流程、接上了你常用的某个服务——没必要只留给自己。跟 Agent 说一句：

> “把刚才这个做成插件，发到社区。”

Agent 会帮你打包、测试，然后在这里提一个 PR。维护者审核合并后，所有 TakuOS 用户都能搜到、装上。

## 插件是什么？

插件就是一个 Agent 能加载的小文件夹，里面装着下面一种或两种东西：

- **Skills（技能）**：用文字教 Agent 怎么做一件事，每个技能一个 `SKILL.md`。
- **MCP 服务**：Agent 能直接调用的工具，比如查天气、开关智能家居。

每个插件都会提前写清楚**它能做什么**（能力）和**它要用到什么**（权限），装之前你心里有数。

## 安装插件

目前从社区安装需要在 TakuOS 上跑几条命令（插件页一键安装正在做）：

1. 从 [`packages/`](packages/) 下载插件 ZIP，用 [`index/`](index/) 里对应文件的 SHA-256 核对一下。
2. 解压到 `/data/local/agentos/work` 下的某个工作目录，先看看里面写了什么。
3. 依次运行：

   ```sh
   taku-plugin validate <解压目录>
   taku-plugin pack <解压目录> <输出目录>
   taku-plugin catalog-add <输出目录>
   taku-plugin install <上一步返回的 marketplace 路径> <插件名>
   ```

> ⚠️ **装之前先看一眼。** 插件以 Agent 本身的权限运行。权限清单是如实声明，不是沙箱——只装你看过或信得过的插件。

## 分享插件

下面那些格式你都不用懂，Agent 会搞定。你只要让它发布，它会：

1. 在你手机上先验证、测试一遍（装上 → 跑一下 → 卸掉）。
2. 打包成 `packages/<名称>-<版本>.zip`，再生成一条 `index/<名称>/<版本>.json` 记录。
3. 在这里提 PR。没网也没关系，东西都先存在本地，联网后再提交。

想自己动手，或者好奇审核看什么？看 [贡献指南](CONTRIBUTING.md) 和 [清单格式](plugins/README.md)。

## 第一个例子

[`status-break-reminder`](https://github.com/Taku-OS/taku-os-plugins/pull/1)——一个提醒你歇一会儿的小插件。它从头到尾都是 Agent 根据一句话自己做出来、自己发布的。

## 许可证

[Apache-2.0](LICENSE)。除非插件目录里另有说明，贡献的插件都按同一许可证发布。
