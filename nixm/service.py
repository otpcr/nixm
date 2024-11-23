# This file is in the Public Domain.
# pylint: disable=C0116,E0402


"service"


from .daemon  import service
from .runtime import errors, wrap


def wrapped():
    wrap(service)
    for line in errors():
        print(line)


if __name__ == "__main__":
    wrapped()
