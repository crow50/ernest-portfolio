---
title: "npm audit: high-severity advisory in production dependencies"
labels: security, dependencies, ci
assignees: crow50
---

`npm audit --audit-level=high --omit=dev` failed on `{{ env.GITHUB_REF_NAME }}`.

- Run: {{ env.GITHUB_SERVER_URL }}/{{ env.GITHUB_REPOSITORY }}/actions/runs/{{ env.GITHUB_RUN_ID }}
- Commit: `{{ env.GITHUB_SHA }}`

This is a high-severity advisory impacting production dependencies. Please triage and remediate as soon as possible.
