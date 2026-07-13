from __future__ import annotations

import argparse
import sys

from application_agent.integrations.slack.app import run_socket_mode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="application-agent")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("slack", help="Run Slack socket-mode listener")

    args = parser.parse_args(argv)
    if args.command == "slack":
        run_socket_mode()
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
