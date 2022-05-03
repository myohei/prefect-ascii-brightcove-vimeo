from prefect_ascii_brightcove_vimeo.flows import hello_and_goodbye


def test_hello_and_goodbye_flow():
    flow_state = hello_and_goodbye()
    assert flow_state.is_completed
