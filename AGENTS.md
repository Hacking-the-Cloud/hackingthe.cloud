# Repository Guidelines

## Project Structure & Module Organization
- `content/` holds all site content (Markdown pages plus `assets/`, `images/`, `stylesheets/`, and `javascripts/`).
- `layouts/`, `overrides/`, and `mkdocs.yml` define the MkDocs Material theme, navigation, and plugins.
- Root files like `Dockerfile` and `dev.Dockerfile` support local preview and CI/build workflows.

## Build, Test, and Development Commands
- `docker build -t mkdocs-material .` builds a local MkDocs Material image for previewing the site.
- `docker run --rm -it -p 8000:8000 -v ${PWD}:/docs mkdocs-material` runs a local preview server at `http://localhost:8000`.
- No dedicated test suite is defined; validation is typically done by building/previewing the site.

## Coding Style & Naming Conventions
- Content is Markdown with YAML front matter. New pages should start with:
  ```
  ---
  author_name: <Your Name>
  title: <Page Title>
  description: <A description of the page>
  ---
  ```
- File names should be descriptive and lowercase with underscores (e.g., `get_account_id_from_keys.md`).
- Cite primary sources and credit original researchers; avoid plagiarism per `CONTRIBUTING.md`.

## Testing Guidelines
- There is no automated test framework in this repo.
- Use the Docker preview workflow to verify rendering and navigation changes before opening a PR.

## Commit & Pull Request Guidelines
- Commit history shows short, imperative subjects, often lowercase and occasionally prefixed (`add`, `fix`, `update`, `new`). Example: `add new post exploitation technique`.
- PRs should describe the change, include references for sourced content, and note any new assets or screenshots added to `content/images/`.
- If you are the original author of imported content, state that clearly in the PR.

## Security & Content Policies
- If you need to remove content or references, open a GitHub issue as described in `CONTRIBUTING.md`.

## Evaluating Content Proposals
- Hacking the Cloud primarily documents concrete attack paths and techniques. Evaluate proposals against that purpose before recommending a draft or acceptance.
- Identify the specific technique actually described or explicitly referenced in the submission. Broad topics such as prompt injection, overprivileged agents, or audit logging do not establish a concrete attack path by themselves. Look for the attack's prerequisites, attacker actions, and resulting security impact; a brief explanation is sufficient at the outline stage.
- Defensive guidance should explain or reference a concrete technique and connect its recommendations to detecting, investigating, or mitigating that technique. Generic logging, observability, or security recommendations are insufficient without that foundation. The technique need not be novel, but existing research must be credited.
- Keep the contributor's proposal separate from your suggestions. Do not invent a hypothetical attack example and then treat it as evidence that the submitted proposal meets the site's scope.
- If the proposal does not identify a concrete technique, state that clearly and ask the contributor to identify the technique the article would cover before encouraging a draft. General statements that defensive or AI/LLM content is welcome do not waive this requirement.

## Writing Style
When writing articles for the website you must use the $writing skill. This ensures the proper tone is used.
