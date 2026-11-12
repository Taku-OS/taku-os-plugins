# Hello World / 第一个插件

This is a community Skill/MCP plugin, not a God Mode package. It returns `Hello from Taku!` locally without network access or user-data reads. It runs with the Agent host's privileges; the empty permission declaration is not a sandbox.

这是社区 Skill/MCP 格式。完整文件都在本目录，无需私有源码权限。它只返回一句问候；不会联网或读取用户资料。它不是 God Mode 格式，不要混用安装命令。

## Install / 安装

Download the ZIP from `packages/` and compare SHA-256 with `index/taku-hello-world/1.0.0.json`. Unzip it, then copy the `taku-hello-world` directory to your own Taku device. Replace `SERIAL` with the selected device:

```sh
adb -s SERIAL push taku-hello-world /data/local/agentos/work/
adb -s SERIAL shell
```

In the device shell / 在设备 shell：

```sh
taku-plugin validate /data/local/agentos/work/taku-hello-world
taku-plugin pack /data/local/agentos/work/taku-hello-world /data/local/agentos/work/hello-world-package
taku-plugin catalog-add /data/local/agentos/work/hello-world-package
```

Use the marketplace path returned by the previous command:

```sh
taku-plugin install MARKETPLACE_PATH taku-hello-world
taku-plugin list
taku-plugin status
```

Ask the connected Agent: **Call the Hello World plugin and show its actual greeting.** Check the tool call in the conversation; its result must be `Hello from Taku!`. An unconnected model cannot perform this step.

向已连接模型的 Agent 说：**调用 Hello World 插件，把它实际返回的问候给我。** 执行记录应有工具调用，返回 `Hello from Taku!`。

## Remove / 卸载

Use the exact ID returned by `taku-plugin list`:

```sh
taku-plugin uninstall PLUGIN_ID
```

The CLI may return exit code 2 when installation/removal succeeded but MCP reload failed. Read `status` before retrying; do not report a failed reload as an unperformed install.

## Development checks / 开发检查

From this repository root, run `python3 scripts/test-example.py` and `python3 scripts/package-example.py`, then the repository validator. Host tests cover MCP messages, archive paths and checksums; they do not replace Agent/UI acceptance on a release ROM.
