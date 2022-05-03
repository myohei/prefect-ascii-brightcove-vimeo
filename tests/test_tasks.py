from prefect import flow

from prefect_ascii_brightcove_vimeo.tasks import (
    goodbye_prefect_ascii_brightcove_vimeo,
    hello_prefect_ascii_brightcove_vimeo,
)


def test_hello_prefect_ascii_brightcove_vimeo():
    @flow
    def test_flow():
        return hello_prefect_ascii_brightcove_vimeo()

    flow_state = test_flow()
    task_state = flow_state.result()
    assert task_state.result() == "Hello, prefect-ascii-brightcove-vimeo!"


def goodbye_hello_prefect_ascii_brightcove_vimeo():
    @flow
    def test_flow():
        return goodbye_prefect_ascii_brightcove_vimeo()

    flow_state = test_flow()
    task_state = flow_state.result()
    assert task_state.result() == "Goodbye, prefect-ascii-brightcove-vimeo!"
