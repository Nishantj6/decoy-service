#!/usr/bin/env python3
"""
Legacy daemon entrypoint.
Starts the same localhost API server used by the Firefox extension.
"""

from api_server import app, API_PORT, logger


def main():
    logger.info(f"Starting Decoy Service daemon on http://localhost:{API_PORT}")
    app.run(
        host="localhost",
        port=API_PORT,
        debug=False,
        use_reloader=False,
    )


if __name__ == "__main__":
    main()
