import sys


def main(*, name):
    message = f"Hello, {name}"
    print("New message:")
    print(message, file=sys.stderr)
    return {
        "message": message,
    }
