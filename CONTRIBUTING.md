# Contributing / 贡献指南

Thanks for sharing a plugin! The easiest path is to let your TakuOS Agent publish it for you — it follows everything below automatically. This page is for people who want to do it by hand, and for reviewers.

感谢你分享插件！最省事的办法是让 TakuOS 上的 Agent 帮你发布，下面这些它会自动照做。这一页写给想手动提交的人，以及审核者。

## Before you open a PR / 提交前

- **Test it for real.** Run `taku-plugin validate` and `pack`, install it, actually use it, then uninstall it.
  **真跑一遍**：`validate`、`pack`，装上、真用一下、再卸掉。
- **One version per PR.** Never overwrite a version that's already been released — bump the version instead.
  **一个 PR 一个版本**。已发布的版本不要覆盖，改版本号。
- **Commit what `pack` produced, unchanged:** `packages/<name>-<version>.zip` and `index/<name>/<version>.json`. Don't edit the hash or strip executable bits.
  **原样提交 `pack` 的产物**：ZIP 和 index 记录，不要改哈希、不要丢可执行位。

## Be honest about what it does / 如实声明

- List every capability in `taku.capabilities` and every permission in `taku.permissions`.
  在 `taku.capabilities`、`taku.permissions` 里写全它能做的事和要用的权限。
- If it talks to the network or depends on something external, say so in the PR.
  会联网、依赖外部服务的，在 PR 里写明。
- **Never** include credentials, tokens, private keys, personal data, build caches, or unrelated files.
  **绝对不要**带凭据、token、私钥、个人数据、构建缓存或无关文件。

## What reviewers look at / 审核看什么

1. Package structure and manifest pass CI. / 包结构和清单通过 CI。
2. The hash matches and the origin is clear. / 哈希对得上，来源清楚。
3. It does something useful, and the test evidence shows it. / 确实有用，有测试证据。
4. Declared permissions match what the code does; dependencies are reasonable and safe. / 声明的权限和代码实际行为一致，依赖合理安全。

Passing CI is required, but it isn't the same as approval. Maintainers may ask for changes or decline submissions that look unsafe.

CI 通过是必要条件，但不等于审核通过。看起来不安全的提交，维护者会要求修改或拒绝。
