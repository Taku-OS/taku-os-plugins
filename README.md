# TakuOS Community Plugins

**English** · [简体中文](README.zh-CN.md)

Plugins teach the Agent on your TakuOS phone new tricks. This repository is where the community shares them.

The idea is simple: if you've solved something useful on your phone — a reminder, a workflow, a connection to a service you love — you shouldn't have to keep it to yourself. Tell your Agent:

> "Turn what we just did into a plugin and publish it to the community."

A compatible Agent can prepare and test the package. Submitting a PR requires authenticated git/gh on the device or the documented host-side publishing helper. A PR URL confirms submission; a local package alone does not. Maintainers review contributions before users install them.

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
3. Submit through authenticated git/gh, or keep the package locally and use the host-side publishing helper. A network connection alone does not configure publishing credentials.

Want to do it yourself, or curious what reviewers look for? See [CONTRIBUTING.md](CONTRIBUTING.md) and the [manifest format](plugins/README.md).

## First example

[Hello World source](examples/taku-hello-world/) includes every file needed; no private repository access is required. [Download the ZIP](packages/taku-hello-world-1.0.1.zip) and [verify its SHA-256](index/taku-hello-world/1.0.1.json), then follow the example's installation, Agent-call and uninstall steps. Host protocol and package checks are automated; device/Agent acceptance is a separate step.

## Security

Use the [private reporting instructions](SECURITY.md) for Taku OS or plugin vulnerabilities.

## License

[Apache-2.0](LICENSE). Each plugin is contributed under the same license unless its folder says otherwise.
