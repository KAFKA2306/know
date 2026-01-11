# Know

A personal knowledge base and bookmark manager built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

## Contents

- **[Bookmarks](docs/bookmarks/index.md)**: Curated resources for AI, Dev, Finance, Games, Life, Media, and Academics.
- **[Dev](docs/dev/index.md)**: Technical knowledge base (AI Agents, WSL).
- **[Life](docs/life/index.md)**: Personal life management (Tax, Investments).

## Setup

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency management and [`task`](https://taskfile.dev/) for command automation.

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)
- [Task](https://taskfile.dev/installation/)

### Installation

```bash
git clone https://github.com/KAFKA2306/know.git
cd know
uv sync
```

## Usage

### Run Locally

Start the live-reloading development server:

```bash
task dev
# OR directly via uv
uv run mkdocs serve
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### Build

Build the static site:

```bash
task build
```

## Deployment

The site is automatically deployed to GitHub Pages via GitHub Actions on push to the `main` branch.
URL: [https://KAFKA2306.github.io/know/](https://KAFKA2306.github.io/know/)
