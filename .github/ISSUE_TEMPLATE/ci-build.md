---
title: "Build failure: the site did not compile"
labels: ci, blocker
assignees: crow50
---

`npm run build` failed on `{{ env.GITHUB_REF_NAME }}`.

- Run: {{ env.GITHUB_SERVER_URL }}/{{ env.GITHUB_REPOSITORY }}/actions/runs/{{ env.GITHUB_RUN_ID }}
- Commit: `{{ env.GITHUB_SHA }}`

Undeployable, Cloudflare will not serve the site until this is fixed.
