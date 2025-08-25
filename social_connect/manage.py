#!/usr/bin/env python
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_connect.settings')

    # If running 'runserver', default to 0.0.0.0 and PORT from env
    if 'runserver' in sys.argv:
        # Check if an address (like '8080' or '0.0.0.0:8080') is provided
        address_specified = any(':' in arg or arg.isdigit() for arg in sys.argv[2:])
        
        if not address_specified:
            port = os.environ.get('PORT', '8000')
            sys.argv.append(f'0.0.0.0:{port}')
                
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
