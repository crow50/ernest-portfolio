---
title: "astro check: type or content-schema error"
labels: ci
assignees: crow50
---

`astro check` failed on `{{ env.GITHUB_REF_NAME }}`.

- Run: {{ env.GITHUB_SERVER_URL }}/{{ env.GITHUB_REPOSITORY }}/actions/runs/{{ env.GITHUB_RUN_ID }}
- Commit: `{{ env.GITHUB_SHA }}`

Usually a content collection that no longer matches its Zod schema in
`src/content.config.ts`, or a TypeScript error in a component.
