"""This is an example flows module"""
from prefect import flow

from prefect_ascii_brightcove_vimeo.tasks import (
    goodbye_prefect_ascii_brightcove_vimeo,
    hello_prefect_ascii_brightcove_vimeo,
)


@flow
def hello_and_goodbye():
    """
    Sample flow that says hello and goodbye!
    """
    print(hello_prefect_ascii_brightcove_vimeo)
    print(goodbye_prefect_ascii_brightcove_vimeo)
