# Security reports / 安全报告

This repository is the shared private-report intake for Taku OS and its plugins while the system source repository remains private.

Report a suspected vulnerability using [Report a vulnerability](https://github.com/Taku-OS/taku-os-plugins/security/advisories/new). GitHub sign-in is required. Reports are private to the reporter and the authorized advisory collaborators; do not open a public issue containing an exploit, credential or private user data.

Include the affected component, exact version/build, caller privileges, reproduction steps, expected boundary and observed impact. Use synthetic data and redact unrelated information. Repository maintainers route core/ROM reports to the relevant module maintainer; @programmerguys coordinates triage. No response-time or bug-bounty commitment is made.

Plugins execute with their host Agent's privileges. Permission declarations are not a sandbox. God Mode is a privileged development host for trusted plugins. Report a demonstrated boundary bypass; describe the starting permissions rather than assuming per-plugin isolation.

系统源码保持私有期间，本仓库同时承接 Taku OS 与插件的私密漏洞报告。使用上方 GitHub 私密报告入口，注明组件、版本、调用方权限、复现步骤和实际影响。维护者负责转交相关模块；不要把漏洞详情、密钥或私人数据写进公开 Issue。
