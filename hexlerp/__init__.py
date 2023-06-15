def hex_to_srgb(hex_: str) -> tuple[int]:
    """Converts hex colors to srgb tuples.

    Parameters
    ----------
    hex_: str
        Input color represented as a six-symbol hex string
        made up of three two-symbol elements.
        Leading "#" prefix will be ignored

    Returns
    -------
    tuple[int]
        tuple representing the rgb color as a tuple of decimal
        integers between 0 and 255

    """

    hex_ = hex_.removeprefix("#")
    hex_elements = ("".join(symbols) for symbols in zip(hex_[::2], hex_[1::2]))
    srgb = (int(h, 16) for h in hex_elements)
    return tuple(srgb)


def _int_to_hex(int_: int) -> str:
    """Converts integer to a string representing the number
    as an uppercase hexidecimal"""
    return f"{int_:02X}"


def srgb_to_hex(srgb: tuple[int], prefix: bool = True) -> str:
    """Converts srgb tuples to a six-symbol hex color

    Parameters
    ----------
    srgb: tuple[int]
        Input color represented as a tuple of integers
        between 0 and 255

    prefix: bool (optional)
        If True a leading # is added to the string.

    Returns
    -------
    str:
        The color represented as a six-symbol hex string
        made up of three two-symbol elements.

    """

    hex_elements = (_int_to_hex(i) for i in srgb)

    hex_string = "".join(hex_elements)
    if prefix:
        hex_string = "#" + hex_string

    return hex_string


def _get_gamma_expanded(color_value: int) -> float:
    """Converts color value to gamma expanded.
    First step when converting srgb to xyz
    Source: https://en.wikipedia.org/wiki/SRGB"""

    color_value /= 255
    if color_value <= 0.04045:
        return color_value / 12.92
    else:
        return ((color_value + 0.055) / 1.055) ** 2.4


def _matrix_by_vector_mult_3by3(matrix, vector):
    """Helper function to multiply 3x3 matrix with vector"""

    x0, x1, x2 = vector

    return tuple(a0 * x0 + a1 * x1 + a2 * x2 for (a0, a1, a2) in matrix)


def srgb_to_xyz(srgb: tuple[int]) -> tuple[float]:
    """Converts srgb tuples to a six-symbol hex color

    Parameters
    ----------
    srgb: tuple[int]
        Input color represented as a tuple of integers
        between 0 and 255


    Returns
    -------
    tuple[int]:
        the color represented as a XYZ color

    References
    ----------
    [1] : https://en.wikipedia.org/wiki/SRGB

    """
    linear_rgb = (_get_gamma_expanded(c_val) for c_val in srgb)

    transform = (
        (0.4124, 0.3596, 0.1805),
        (0.2126, 0.7152, 0.0722),
        (0.0193, 0.1192, 0.9505),
    )

    xyz = _matrix_by_vector_mult_3by3(transform, linear_rgb)
    return xyz


def _clamp(value: float, min_value: float, max_value: float) -> float:
    """Helper function to clamp a float to a given range"""
    return min(max(value, min_value), max_value)


def _get_gamma_compressed(color_value: float) -> int:
    """Converts color value to gamma compressed.
    Last step when converting xyz to srgb
    Source: https://en.wikipedia.org/wiki/SRGB"""

    if color_value <= 0.0031308:
        compressed_value = 12.92 * color_value
    else:
        compressed_value = 1.055 * (color_value) ** (1 / 2.4) - 0.055

    return int(round(255 * (_clamp(compressed_value, 0, 1))))
    # return int(_clamp(round(255 * (compressed_value)), 0, 255))


def xyz_to_srgb(xyz: tuple[float]) -> tuple[int]:
    """Converts xyz color tuples to srgb tuples

    Parameters
    ----------
    xyz: tuple[int]
        the color represented as a XYZ color


    Returns
    -------
    tuple[int]:
        Input color represented as a tuple of integers
        between 0 and 255

    References
    ----------
    [1] : https://en.wikipedia.org/wiki/SRGB

    """
    transform = (
        (3.2469, -1.5494, -0.4989),
        (-0.9708, 1.8794, 0.0416),
        (0.0558, -0.2042, 1.0570),
    )
    linear_rgb = _matrix_by_vector_mult_3by3(transform, xyz)

    srgb = (_get_gamma_compressed(c_val) for c_val in linear_rgb)

    return tuple(srgb)


def _f(t):
    delta = 6 / 29
    if t > delta**3:
        return t ** (1 / 3)
    else:
        return t / (3 * delta * delta) + 4 / 29


def _f_inverse(t):
    delta = 6 / 29
    if t > delta:
        return t**3
    else:
        return 3 * delta**2 * (t - 4 / 29)


def xyz_to_lab(xyz: tuple[float]) -> tuple[float]:
    """Converts xyz tuples to lab tuples

    Parameters
    ----------
    xyz: tuple[int]
        the color represented as CIEXYZ coordinates


    Returns
    -------
    tuple[int]:
        Input color represented in CIELAB space

    References
    ----------
    [1] : https://en.wikipedia.org/wiki/Chromaticity

    """
    X_n = 96.0489
    Y_n = 100
    Z_n = 108.8840

    x, y, z = xyz

    L = 116 * _f(y / Y_n) - 16
    a = 500 * (_f(x / X_n) - _f(y / Y_n))
    b = 200 * (_f(y / Y_n) - _f(z / Z_n))

    return L, a, b


def lab_to_xyz(lab: tuple[float]) -> tuple[float]:
    """Converts lab tuples to xyz tuples

    Parameters
    ----------
    lab: tuple[int]
        Color represented in CIELAB space


    Returns
    -------
    tuple[int]:
        The color represented as CIEXYZ coordinates

    References
    ----------
    [1] : https://en.wikipedia.org/wiki/Chromaticity
    """

    X_n = 96.0489
    Y_n = 100
    Z_n = 108.8840

    L, a, b = lab

    x = X_n * _f_inverse((L + 16) / 116 + a / 500)
    y = Y_n * _f_inverse((L + 16) / 116)
    z = Z_n * _f_inverse((L + 16) / 116 - b / 200)

    return x, y, z


def _lerp(num1: float, num2: float, t: float) -> float:
    return (1 - t) * num1 + t * num2


def hex_to_lab(hex_: str) -> tuple[float]:
    """Converts hex colors to lab tuples.

    Parameters
    ----------
    hex_: str
        Input color represented as a six-symbol hex string
        made up of three two-symbol elements.
        Leading "#" prefix will be ignored


    Returns
    -------
    tuple[int]:
        Input color represented in CIELAB space
    """
    rgb = hex_to_srgb(hex_)
    xyz = srgb_to_xyz(rgb)
    return xyz_to_lab(xyz)


def lab_to_hex(lab: tuple[float], prefix: bool = True) -> str:
    """Converts lab tuples to hex colors.

    Parameters
    ----------
    lab: tuple[int]
        Color represented in CIELAB space

    prefix: bool (optional)
        If True a leading # is added to the string.

    Returns
    -------
    str:
        The color represented as a six-symbol hex string
        made up of three two-symbol elements.
    """
    xyz = lab_to_xyz(lab)
    rgb = xyz_to_srgb(xyz)
    return srgb_to_hex(rgb, prefix=prefix)


def lerp_hex(hex1: str, hex2: str, t: float, prefix: bool = True) -> str:
    """Interpolate between two hex values (linearly in the CIELAB space).

    Parameters
    ----------
    hex1: str
        First input color represented as a six-symbol hex string
        made up of three two-symbol elements.
        Leading "#" prefix will be ignored

    hex2: str
        Second input color represented as a six-symbol hex string
        made up of three two-symbol elements.
        Leading "#" prefix will be ignored

    t: float
        Interpolation value (between 0 and 1). If 0, then hex1
        is returned, if 0.5, then the midpoint between hex1
        and hex2 is returned and if 1 then hex2 is returned.

    prefix: bool (optional)
        If True a leading # is added to the string.

    Returns
    -------
    str:
        The interpolated color represented as a six-symbol hex string
        made up of three two-symbol elements.
    """

    lab1 = hex_to_lab(hex1)
    lab2 = hex_to_lab(hex2)

    lab = (_lerp(val1, val2, t) for val1, val2 in zip(lab1, lab2))
    return lab_to_hex(lab, prefix=prefix)
