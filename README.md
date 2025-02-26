### Prerequisites:
uv package manager

```
pip install uv
or
brew install uv
```

### Local development
Create virtual env if needed
```shell
uv venv
source bin/activate
```
Install project
```shell
uv sync --all-groups
```
Run dev server
```shell
fastapi dev src/app.py
```
