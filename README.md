# Taku OS Community Plugins / Taku OS 社区插件

An independently reviewed community registry of Taku plugin packages. Plugins run with the runtime's privileges; declarations are **not** a security sandbox. Review code and permissions before installation.

这里收录经社区审核的 Taku 插件包。插件以运行时的权限运行；声明的能力与权限**不是**安全隔离。安装前请审阅代码及权限。

## Install / 安装

Download a version's ZIP from `packages/`, verify its SHA-256 against `index/<name>/<version>.json`, and extract it into a trusted workspace. Run `taku-plugin validate <extracted-plugin>`, then `taku-plugin pack <extracted-plugin> <new-workspace-output>`, `taku-plugin catalog-add <new-workspace-output>`, and `taku-plugin install <returned-marketplace-path> <name>`. Install only after reviewing its contents. Commands run on Taku OS; `catalog-add` requires the output inside `/data/local/agentos/work`.

从 `packages/` 下载版本 ZIP，与 `index/<名称>/<版本>.json` 核对 SHA-256；在可信工作区解压并审核。依次运行 `taku-plugin validate <解压目录>`、`taku-plugin pack <解压目录> <新的工作区输出目录>`、`taku-plugin catalog-add <输出目录>`，再用返回的 marketplace 路径和名称执行 `taku-plugin install`。这些命令在 Taku OS 上运行，输出目录须位于 `/data/local/agentos/work`。

## Publish with an Agent / 一句话发布

Tell the Agent: “Turn the case we just completed into a plugin, test it, and publish it to the Taku OS community.”

对 Agent 说：“把刚才这个案例做成插件，测试后发布到 Taku OS 社区。”

The Agent should validate and test locally, produce a package and index, then submit a pull request using an authenticated host; offline submissions remain local until submitted. See [CONTRIBUTING.md](CONTRIBUTING.md) and [the manifest guide](plugins/README.md). Never include credentials or private data.

Agent 应先本地验证和测试，生成包及索引，再通过已登录的宿主机提交 PR；离线时保留本地结果。详见[贡献指南](CONTRIBUTING.md)和[清单格式](plugins/README.md)。严禁包含凭据或私人数据。
