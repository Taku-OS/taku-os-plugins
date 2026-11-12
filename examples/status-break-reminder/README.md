# Status break reminder

This minimal skill prints `Take a short break.` when the Agent invokes it. It does not schedule a reminder, send notifications, access accounts or make network requests.

Version 1.0.1 adds reviewable source and a reproducible package. The original 1.0.0 ZIP and checksum remain unchanged.

```sh
python3 scripts/package-example.py status-break-reminder
sh examples/status-break-reminder/scripts/status.sh
```

Expected output: `Take a short break.` Install using the repository README, then ask the Agent to run the status reminder skill. Host script execution is tested in CI; device installation and Agent invocation require separate acceptance.

Apache-2.0; see LICENSE.
