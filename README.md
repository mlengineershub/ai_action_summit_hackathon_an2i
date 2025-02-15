# ai_action_summit_hackathon_an2i


# Development

## Notes
- commit messages should follow conventional commits spec: https://www.conventionalcommits.org/en/v1.0.0/ (see sections: Summary, Examples)
- work must be merged from feature branches into main branch using Pull Requests. Once your code is ready to be reviewed, please mark me as a reviewer, which will notify me you're ready fir code review 

## How-to's 

### Install 

1. install uv: https://docs.astral.sh/uv/getting-started/installation/#standalone-installer
2. run
   ```shell
   uv sync --all-extras --dev
   ```



### Lint (check & fix)
1. open a new terminal in the root of this repo and run:

```shell
uv run ruff check --fix
uv run ruff format
uv run mypy .
```

### Run tests 
1. open a new terminal in the root of this repo and run:
```shell
uv run pytest
```