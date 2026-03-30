# Research Repo Template — Claude Code Guide

## Project Structure

```
src/mypackage/          # Python package
tests/                  # pytest tests, coverage with pytest-cov
paper/                  # NeurIPS 2025 LaTeX template
slides/                 # Beamer LaTeX slides
slides-js/              # Next.js presentation decks
scripts/                # Training/evaluation scripts
configs/                # Hydra config files
```

## Essential Commands

```bash
make install            # uv sync --all-groups + pre-commit install
make check              # ruff format/check, ty, pre-commit hooks
make test               # pytest --cov=src tests/
```

## Development

```bash
make install   # uv sync --all-extras
make check     # pre-commit run --all-files (ruff, ty, typos, pyproject-fmt, mdformat, etc.)
make test      # pytest --cov=src tests/
make clean     # remove build artifacts
```

## Paper (`paper/`)

NeurIPS 2025 template. Requires TeX Live + tex-fmt.

```bash
cd paper
make install   # tlmgr install required LaTeX packages
make check     # tex-fmt --check on .tex files
make build     # latexmk -pdf (produces main.pdf)
make watch     # latexmk -pvc (live rebuild on save)
make clean     # remove build artifacts
```

## Slides (`slides/`)

Beamer presentation template.

```bash
cd slides
make install   # tlmgr install required LaTeX packages
make check     # tex-fmt --check on .tex files
make build     # latexmk -pdf (produces main.pdf)
make watch     # latexmk -pvc (live rebuild on save)
make clean     # remove build artifacts
```

## CI

GitHub Actions runs `make check` and `make test` on push/PR to `main`. Release to PyPI on version tags (`v*`).

## Key Conventions

- **Python 3.13+** required. Package manager: uv
- **Linting**: ruff (line-length=100), type-check: ty
- **Testing**: pytest in `tests/`, coverage measured
- **Pre-commit**: enforces format, types, imports before commit
- **Package name**: Replace `mypackage` with actual name in code and CLAUDE.md rules
- **Type annotations**: Required on public APIs (ruff rule ANN)

## Development Workflow

1. Edit code in `src/mypackage/` or `tests/`
2. Run `make check` before committing (formats, lints, type-checks)
3. Run `make test` to verify tests pass with coverage
4. Use `/commit` for enriched commits with WHY-focused bodies
5. Use `/plan-feature` to spec complex features; `/execute` to implement from spec

## Paths and Tools

- Path-scoped rules load auto when touching `src/`, `tests/`, `paper/`, `slides-js/`
- Use `/prime` to load full codebase overview
- Spawn sub-agents for research with `/plan-feature` — keeps main context clean
- On long sessions, use `/handoff` to write progress and switch fresh

## References

- WISC Framework: context tiers, slash commands, enriched commits
- Configuration: see `.claude/rules/` for domain-specific conventions
- Detailed docs: `.claude/docs/` (loaded on-demand by sub-agents)
