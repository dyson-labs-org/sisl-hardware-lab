"""CLI entry point for quick SISL lab checks."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_config
from .protocol.hail import HailBody, build_hail_frame


def build_parser() -> argparse.ArgumentParser:
    """Construct the command-line parser."""

    parser = argparse.ArgumentParser(prog="sisl-lab")
    sub = parser.add_subparsers(dest="command", required=True)

    show_config = sub.add_parser("show-config", help="Load and print config summary")
    show_config.add_argument("--config", default="configs/default.toml")

    gen_hail = sub.add_parser("gen-hail", help="Generate a plaintext scaffold hail frame")
    gen_hail.add_argument("--source", type=int, default=12345)
    gen_hail.add_argument("--target", type=int, default=54321)
    gen_hail.add_argument("--freq-offset", type=int, default=100)
    gen_hail.add_argument("--bandwidth-code", type=int, default=3)
    gen_hail.add_argument("--mode-code", type=int, default=1)
    gen_hail.add_argument("--chip-rate", type=int, default=5)
    gen_hail.add_argument("--nonce", type=int, default=0x0102030405060708)
    gen_hail.add_argument("--flags", type=int, default=0x03)

    return parser


def run_show_config(config_path: str) -> int:
    """Load a config and print a concise summary."""

    path = Path(config_path)
    config = load_config(path)
    print(f"Loaded: {path.resolve()}")
    print(f"Local NORAD: {config.local_norad_id}")
    print(f"Callsign: {config.local_callsign}")
    print(
        f"Radio: {config.radio.center_freq_mhz} MHz, {config.radio.bandwidth_mhz} MHz BW, "
        f"{config.radio.chip_rate_mcps} Mcps {config.radio.mode}"
    )
    return 0


def run_gen_hail(args: argparse.Namespace) -> int:
    """Generate and print a scaffold hail frame in hex."""

    body = HailBody(
        source_norad=args.source,
        center_freq_offset_mhz=args.freq_offset,
        bandwidth_code=args.bandwidth_code,
        mode_code=args.mode_code,
        chip_rate_mcps=args.chip_rate,
        nonce=args.nonce,
        flags=args.flags,
    )
    packet = build_hail_frame(body=body, target_norad=args.target)
    print(packet.hex())
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run the CLI."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "show-config":
        return run_show_config(args.config)
    if args.command == "gen-hail":
        return run_gen_hail(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
