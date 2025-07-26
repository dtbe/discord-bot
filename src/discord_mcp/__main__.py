import asyncio
import sys
from .server import main

# This file serves as the entry point when the package is executed with `python -m discord_mcp`.
# This resolves the RuntimeWarning related to 'runpy' and module execution order.
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down server.")
        sys.exit(0)