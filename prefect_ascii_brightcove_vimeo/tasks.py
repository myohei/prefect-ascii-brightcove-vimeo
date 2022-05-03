"""This is an example tasks module"""
from prefect import task


@task
def hello_prefect_ascii_brightcove_vimeo() -> str:
    """
    Sample task that says hello!

    Returns:
        A greeting for your collection
    """
    return "Hello, prefect-ascii-brightcove-vimeo!"


@task
def goodbye_prefect_ascii_brightcove_vimeo() -> str:
    """
    Sample task that says goodbye!

    Returns:
        A farewell for your collection
    """
    return "Goodbye, prefect-ascii-brightcove-vimeo!"
