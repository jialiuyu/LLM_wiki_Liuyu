# Workflows

These workflows are the human-facing version of `AGENTS.md`.

## Ingest A Source

1. Add the source to `raw/inbox/`.
2. Ask the agent to ingest the specific file.
3. The agent creates a source page under `wiki/sources/`.
4. The agent updates related concept, entity, synthesis, comparison, or question
   pages.
5. The agent updates `wiki/index.md`.
6. The agent appends `wiki/log.md`.
7. The agent runs `make check`.
8. You review the diff.

## Ask A Question

Ask the agent to answer from the wiki first. If the answer produces durable
knowledge, ask the agent to file it under `wiki/questions/`,
`wiki/syntheses/`, or `wiki/comparisons/`.

## Run A Health Check

Ask the agent to run a lint pass. The output should become a page under
`wiki/lints/` when it contains useful findings.

## Evolve The Schema

When you notice repeated maintenance mistakes, update `AGENTS.md`. This is how
the wiki becomes easier for future agent sessions to maintain.

