from hexlerp import lerp_hex

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("hex1", help="Start hex color")
    parser.add_argument("hex2", help="End hex color")
    parser.add_argument(
        "--amount", default=0.5, help="Value used to interpolate between hex1 and hex2."
    )

    args = parser.parse_args()

    hex2 = lerp_hex(args.hex1, args.hex2, float(args.t))
    print(hex2)
