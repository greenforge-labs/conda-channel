# conda-channel

Public conda channel for GreenForge Labs custom packages.

Served directly from this repo via raw.githubusercontent.com:

```
https://raw.githubusercontent.com/greenforge-labs/conda-channel/main
```

Add to `pixi.toml`:

```toml
channels = ["https://raw.githubusercontent.com/greenforge-labs/conda-channel/main", ...]
```

## Packages

- `livox-sdk2`
- `robin`
- `kiss-matcher`

## Rebuild

```
task build
```

Then commit the new/updated `linux-64/*.conda`, `linux-64/repodata.json`, and `noarch/repodata.json`.

Bump `build_number` or `version` in the recipe for every rebuild — never overwrite an existing `<name>-<version>-<build>.conda`, or consumers with cached copies will hit hash-mismatch errors.

## Commit convention

Lightweight prefix scheme — keeps `git log` scannable and makes reverts surgical.

- `publish: <name> <version>-<build>` — new/updated `.conda` artifacts. Should contain only `linux-64/*.conda` + `linux-64/repodata.json` + `noarch/repodata.json`.
- `recipe: <name>: <change>` — recipe edits. Commit separately *before* the resulting `publish:`.
- `chore:` / `docs:` / `ci:` — infra, README, workflows.

Example:

```
publish: kiss-matcher 0.1.1-0
recipe: kiss-matcher: bump to 0.1.1
publish: robin 1.2.4-1
recipe: robin: fix cmake export paths
chore: add gh actions build workflow
```

Keeping recipe edits separate from publishes means reverting a bad build is just reverting the `publish:` commit — the recipe fix stays intact.
