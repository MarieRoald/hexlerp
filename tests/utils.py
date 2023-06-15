def generate_random_hex(rng):
    hex_values = "0123456789abcdefABCDEF"
    random_hex_values = (rng.choice(hex_values) for _ in range(6))
    return "#" + "".join(random_hex_values)