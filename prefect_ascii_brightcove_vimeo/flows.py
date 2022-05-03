"""This is an example flows module"""
from prefect import flow

from prefect_ascii_brightcove_vimeo.tasks import (
    goodbye_prefect_ascii_brightcove_vimeo,
    hello_prefect_ascii_brightcove_vimeo,
)

from prefect_ascii_brightcove_vimeo.file_management_service import (AwsS3Credentials,convert)


@flow
def hello_and_goodbye():
    """
    Sample flow that says hello and goodbye!
    """
    print(hello_prefect_ascii_brightcove_vimeo)
    print(goodbye_prefect_ascii_brightcove_vimeo)


if __name__ == '__main__':
    hello_and_goodbye()
