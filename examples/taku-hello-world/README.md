# Hello World / 第一个插件

This is a community Skill/MCP plugin, not a God Mode package. It returns `Hello from Taku!` locally without network access or user-data reads. It runs with the Agent host's privileges; the empty permission declaration is not a sandbox.

这是社区 Skill/MCP 格式。完整文件都在本目录，无需私有源码权限。它只返回一句问候；不会联网或读取用户资料。它不是 God Mode 格式，不要混用安装命令。

## Install / 安装

Download the ZIP from `packages/` and compare SHA-256 with `index/taku-hello-world/1.0.1.json`. Unzip it, then copy the `taku-hello-world` directory to your own Taku device. Replace `SERIAL` with the selected device:

Only supported Taku userdebug development images can use the root ADB route below. If `adb root` is refused, stop; do not apply it to a stock production image. The plugin work directory is root-owned.

以下电脑安装路径需要支持 root ADB 的 Taku userdebug 开发镜像。若 `adb root` 被拒绝就停止，不适用于原厂生产系统。

```sh
adb -s SERIAL root
adb -s SERIAL wait-for-device
adb -s SERIAL shell id
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
