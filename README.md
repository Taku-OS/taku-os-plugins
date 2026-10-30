# TakuOS Community Plugins

**English** · [简体中文](README.zh-CN.md)

Plugins teach the Agent on your TakuOS phone new tricks. This repository is where the community shares them.

The idea is simple: if you've solved something useful on your phone — a reminder, a workflow, a connection to a service you love — you shouldn't have to keep it to yourself. Tell your Agent:

> "Turn what we just did into a plugin and publish it to the community."

The Agent packages it, tests it, and opens a pull request here. Once a maintainer reviews and merges it, every TakuOS user can find and install it.

## What's a plugin?

A plugin is a small folder the Agent can load. It contains one or both of:

- **Skills** — written instructions that teach the Agent how to do something (a `SKILL.md` per skill).
- **MCP servers** — tools the Agent can call, like a weather lookup or a smart-home switch.

Every plugin also says up front **what it can do** (capabilities) and **what it needs access to** (permissions), so you know what you're installing.

## Install a plugin

For now, installing from the community is a few commands on TakuOS (one-tap install from the plugin page is on the way):

1. Download the plugin's ZIP from [`packages/`](packages/) and check its SHA-256 against the matching file in [`index/`](index/).
2. Unzip it into a working folder under `/data/local/agentos/work` and read through it.
3. Run:

   ```sh
   taku-plugin validate <unzipped-folder>
   taku-plugin pack <unzipped-folder> <output-folder>
   taku-plugin catalog-add <output-folder>
   taku-plugin install <marketplace-path-from-previous-step> <plugin-name>
   ```

> ⚠️ **Read before you install.** Plugins run with the Agent's own privileges. The permission list is an honest declaration, not a sandbox — only install plugins you've reviewed or trust.

## Share a plugin

You don't need to know any of the formats below — the Agent handles them. Just ask it to publish, and it will:

1. Validate and test the plugin on your phone (install → run → uninstall).
2. Package it into `packages/<name>-<version>.zip` plus a record in `index/<name>/<version>.json`.
3. Open a pull request here. If you're offline, everything stays saved locally until you're connected.

Want to do it yourself, or curious what reviewers look for? See [CONTRIBUTING.md](CONTRIBUTING.md) and the [manifest format](plugins/README.md).

## First example

[`status-break-reminder`](https://github.com/Taku-OS/taku-os-plugins/pull/1) — a tiny plugin that reminds you to take a break. It was created and published end-to-end by the Agent from a single sentence.

## License

[Apache-2.0](LICENSE). Each plugin is contributed under the same license unless its folder says otherwise.
