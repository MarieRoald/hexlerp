from pytest import approx, mark

from hexlerp import _clamp, hex_to_srgb, lerp_hex, srgb_to_hex, srgb_to_xyz, xyz_to_srgb

from .utils import generate_random_hex


def tuple_approx_equal(tuple1, tuple2, **kwargs):
    for element1, element2 in zip(tuple1, tuple2):
        assert element1 == approx(element2, **kwargs)


@mark.parametrize(
    "hex_, rgb",
    [
        ("FFFFFF", (255, 255, 255)),
        ("000000", (0, 0, 0)),
        ("424242", (66, 66, 66)),
        ("#800000", (128, 0, 0)),
    ],
)
def test_hex_to_srgb_known_values(hex_, rgb):
    assert rgb == hex_to_srgb(hex_)


@mark.parametrize(
    "hex_, rgb",
    [
        ("#FFFFFF", (255, 255, 255)),
        ("#000000", (0, 0, 0)),
        ("#424242", (66, 66, 66)),
        ("#800000", (128, 0, 0)),
    ],
)
def test_srgb_to_hex_known_values(hex_, rgb):
    assert hex_ == srgb_to_hex(rgb)


def test_srgb_to_hex_and_hex_to_srgb_inverse(random_hex, random_rgb):
    """Calling srgb_to_hex on the result from hex_to_srgb should
    return the same hex value as you started with.
    The same should hold for calling hex_to_srgb on the result from
    srgb_to_hex"""

    assert random_hex.upper() == srgb_to_hex(hex_to_srgb(random_hex))
    assert random_rgb == hex_to_srgb(srgb_to_hex(random_rgb))


def test_srgb_to_xyz_and_xyz_to_srgb_inverse(random_rgb):
    """Calling srgb_to_xyz on the result from xyz_to_srgb should
    return the same xyz values as you started with.
    The same should hold for calling xyz_to_srgb on the result from
    srgb_to_xyz"""

    assert random_rgb == xyz_to_srgb(srgb_to_xyz(random_rgb))
    random_xyz = srgb_to_xyz(random_rgb)
    assert random_xyz == srgb_to_xyz(xyz_to_srgb(random_xyz))


@mark.parametrize(
    "xyz, rgb",
    [
        ((95.05, 100, 108.899999), (255, 255, 255)),
        ((0, 0, 0), (0, 0, 0)),
        ((0.0061, 0.0066, 0.0130), (10, 20, 30)),
    ],
)
def test_xyz_to_srgb_known_values(xyz, rgb):
    assert rgb == xyz_to_srgb(xyz)


def test_clamp_between_0_and_1(rng):
    number = rng.uniform(-2, 2)
    clamped = _clamp(number, 0, 1)

    assert clamped <= 1
    assert clamped >= 0

    if number >= 1:
        assert clamped == 1
    elif number <= 0:
        assert clamped == 0
    else:
        assert clamped == number


def test_lerp_hex_endpoints(rng):
    """interpolating with t=0 should give the start hex
    and interpolating with t=1 should give the end hex"""
    hex1 = generate_random_hex(rng)
    hex2 = generate_random_hex(rng)
    assert lerp_hex(hex1, hex2, 0) == hex1.upper()
    assert lerp_hex(hex1, hex2, 1) == hex2.upper()
