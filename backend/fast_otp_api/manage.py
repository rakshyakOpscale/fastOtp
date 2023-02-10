#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fast_otp_api.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    with open(".env") as f:
        for line in f:
            var = line.strip().split("=")
            if len(var) == 2:
                os.environ[var[0]] = var[1]
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
