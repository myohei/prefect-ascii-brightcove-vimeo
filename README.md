# prefect-ascii-brightcove-vimeo

## Welcome!

Prefect Collection for ascii.jp

## Getting Started

### Python setup

Requires an installation of Python 3.7+.

We recommend using a Python virtual environment manager such as pipenv, conda or virtualenv.

These tasks are designed to work with Prefect 2.0. For more information about how to use Prefect, please refer to the [Prefect documentation](https://orion-docs.prefect.io/).

### Installation

Install `prefect-ascii-brightcove-vimeo` with `pip`:

```bash
pip install prefect-ascii-brightcove-vimeo
```

### Write and run a flow

```python
from prefect import flow
from prefect_ascii_brightcove_vimeo.tasks import (
    goodbye_prefect_ascii_brightcove_vimeo,
    hello_prefect_ascii_brightcove_vimeo,
)


@flow
def example_flow():
    hello_prefect_ascii_brightcove_vimeo
    goodbye_prefect_ascii_brightcove_vimeo

example_flow()
```

## Resources

If you encounter any bugs while using `prefect-ascii-brightcove-vimeo`, feel free to open an issue in the [prefect-ascii-brightcove-vimeo](https://github.com/myohei/prefect-ascii-brightcove-vimeo) repository.

If you have any questions or issues while using `prefect-ascii-brightcove-vimeo`, you can find help in either the [Prefect Discourse forum](https://discourse.prefect.io/) or the [Prefect Slack community](https://prefect.io/slack).

## Development

If you'd like to install a version of `prefect-ascii-brightcove-vimeo` for development, clone the repository and perform an editable install with `pip`:

```bash
git clone https://github.com/myohei/prefect-ascii-brightcove-vimeo.git

cd prefect-ascii-brightcove-vimeo/

pip install -e ".[dev]"

# Install linting pre-commit hooks
pre-commit install
```
