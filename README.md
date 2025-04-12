


# lettuce_logger

A tiny logger with a `pp()` function.

- `pp(x)` logs the variable with its name and value
- Logs are saved to a temp folder
- Optional: rotating log files by module, info, and warnings

---

## Installation

Install directly from GitHub with a version tag:

```bash
pip install git+https://github.com/yoki/lettuce_logger.git@v0.1.x
```
(fix version number)

---

Let me know if you’re planning to publish it on PyPI later—then we can include a different installation line.
## Usage for small project

```python
from lettuce_logger import pp # noqa: F401

x = 42
pp(x)  # logs "x = 42"
```

```python
from lettuce_logger import pp, show_pp, hide_pp # noqa: F401

pp("hello from pp level")
hide_pp()
pp("this will not be shown")
show_pp()
pp("this will")

from lettuce_logger import get_log_dir
print(f"Log is saved to {get_log_dir()}")
```

---

## Usage for projects with log folder
```python
from lettuce_logger import pp, show_pp, get_logger, hide_pp  # noqa: F401

# project name as string → logs to temp/mylog/project/
mylog = get_logger("worker", project="proj123")

# OR: pass a Path → logs to that folder
from pathlib import Path
mylog = get_logger("custom", project=Path("/<my-project-root>/logs/myrun"))

mylog.info('things look ok')
mylog.warn("something can be wrong")
pp(df) # => print df to the console

```

---

## Output files

If project is `"proj123"` and name is `"worker"`:

```
/tmp/mylog/proj123/worker.log
/tmp/mylog/proj123/all_info.log
/tmp/mylog/proj123/all_warning.log
```

---

## About `pp`

- Uses a log level between DEBUG and INFO ("PP")
- Can be turned on/off with `.show_pp()` and `.hide_pp()`

---


## Memo for dev

```
$ git clone git+https://github.com/yoki/lettuce_logger.git@v0.1.x
$ pip install -e .
$ python examples/sample_usage.py
$ git tag v0.1.1 -m "Bugfix"
$ git push origin v0.1.1
```