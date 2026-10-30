# Contributing / 贡献

1. Create and test a plugin with `taku-plugin validate`, `pack`, installation, actual behavior, and uninstall. Submit one plugin version per PR; do not overwrite a released version.
2. Include the pack-generated ZIP in `packages/` and index record in `index/<name>/<version>.json`; preserve the SHA-256 and executable bits. Use a descriptive title, summary, test results, and any known limitations.
3. Declare all capabilities and permissions honestly in `taku.capabilities` and `taku.permissions`. Never include credentials, tokens, private keys, personal data, build caches, or unrelated files. Explain external network access and dependencies.
4. Reviewers check schema and package structure, hash, provenance, useful behavior, test evidence, declared permissions, dependencies and security. Passing CI is necessary but not sufficient for acceptance. Maintainers may request changes or reject unsafe submissions.

请每个 PR 提交一个版本，不覆盖已发布版本，附功能说明、测试结果和限制。必须如实声明能力、权限、网络访问和依赖；严禁提交凭据、密钥、个人数据或无关文件。审核包括结构、哈希、来源、实际行为、测试及安全；CI 通过不等于审核通过。
