import random
import re

from js import document
from pyodide.ffi import create_proxy

import hexlerp.hexlerp as hexlerp  # Because GitHub Pages won't serve __init__.py


def random_light_hex():
    srgb = (
        random.randint(100, 255),
        random.randint(100, 255),
        random.randint(100, 255),
    )
    return hexlerp.srgb_to_hex(srgb)


def add_missing_hex_prefix(hex_value):
    if not hex_value.startswith("#"):
        hex_value = "#" + hex_value
    return hex_value


def parse_lab_string(lab_string):
    lab_string = lab_string.removeprefix("(").removesuffix(")")
    return tuple((float(c) for c in lab_string.split(",")))


def format_lab_string(lab_tuple):
    value_strings = ", ".join(f"{c:.4f}" for c in lab_tuple)
    return f"({value_strings})"


def validate_hex(hex_string):
    return re.fullmatch("#?[0-9a-fA-F]{6}", hex_string)


# -- Utilities to update two out of three color picker elements based on the third -- #
def update_lab_and_picker(hex_element, lab_element, picker_element):
    hex_value = add_missing_hex_prefix(hex_element.value)
    if validate_hex(hex_value):
        lab_element.value = format_lab_string(hexlerp.hex_to_lab(hex_value))
        picker_element.value = hex_value
        hex_element.value = hex_value


def update_lab_and_hex(hex_element, lab_element, picker_element):
    hex_value = picker_element.value

    lab_element.value = format_lab_string(hexlerp.hex_to_lab(hex_value))
    hex_element.value = hex_value


def update_picker_and_hex(hex_element, lab_element, picker_element):
    lab_value = parse_lab_string(lab_element.value)
    # TODO: Validate lab
    hex_value = hexlerp.lab_to_hex(lab_value)
    picker_element.value = hex_value
    hex_element.value = hex_value


# ------- Callbacks for start colour------- #
def callback_update_c1_lab_and_picker(*args):
    c1_hex = document.getElementById("c1_hex")
    c1_lab = document.getElementById("c1_lab")
    c1_picker = document.getElementById("c1_picker")

    update_lab_and_picker(c1_hex, c1_lab, c1_picker)


def callback_update_c1_lab_and_hex(*args):
    c1_hex = document.getElementById("c1_hex")
    c1_lab = document.getElementById("c1_lab")
    c1_picker = document.getElementById("c1_picker")

    update_lab_and_hex(c1_hex, c1_lab, c1_picker)


def callback_update_c1_picker_and_hex(*args):
    c1_hex = document.getElementById("c1_hex")
    c1_lab = document.getElementById("c1_lab")
    c1_picker = document.getElementById("c1_picker")

    update_picker_and_hex(c1_hex, c1_lab, c1_picker)


# ------- Callbacks for end colour------- #
def callback_update_c2_lab_and_picker(*args):
    c2_hex = document.getElementById("c2_hex")
    c2_lab = document.getElementById("c2_lab")
    c2_picker = document.getElementById("c2_picker")

    update_lab_and_picker(c2_hex, c2_lab, c2_picker)


def callback_update_c2_lab_and_hex(*args):
    c2_hex = document.getElementById("c2_hex")
    c2_lab = document.getElementById("c2_lab")
    c2_picker = document.getElementById("c2_picker")

    update_lab_and_hex(c2_hex, c2_lab, c2_picker)


def callback_update_c2_picker_and_hex(*args):
    c2_hex = document.getElementById("c2_hex")
    c2_lab = document.getElementById("c2_lab")
    c2_picker = document.getElementById("c2_picker")

    update_picker_and_hex(c2_hex, c2_lab, c2_picker)


# ------- Callbacks for the interpolation value ------- #
def callback_update_slider_value(*args):
    lerp_slider = document.getElementById("lerp_value")
    lerp_output = document.getElementById("lerp_value_output")

    lerp_output.value = lerp_slider.value


def callback_update_slider(*args):
    lerp_slider = document.getElementById("lerp_value")
    lerp_output = document.getElementById("lerp_value_output")

    lerp_slider.value = float(lerp_output.value)


# ------- Callback for interpolating ------- #
def callback_hex_lerp(*args):
    c1 = document.getElementById("c1_hex")
    c2 = document.getElementById("c2_hex")
    output_hex = document.getElementById("output_hex")
    output_lab = document.getElementById("output_lab")
    lerp_slider = document.getElementById("lerp_value")

    if not c1.value:
        c1.value = c1.placeholder
    if not c2.value:
        c2.value = c2.placeholder

    lerp_value = float(lerp_slider.value)

    if not (validate_hex(c1.value) and validate_hex(c2.value)):
        return

    new_hex = hexlerp.lerp_hex(c1.value, c2.value, lerp_value)
    output_hex.textContent = new_hex
    output_lab.textContent = format_lab_string(hexlerp.hex_to_lab(new_hex))

    document.body.style.background = new_hex


if __name__ == "__main__":

    # ------- Choose random colors for placeholders ------ #
    hex_1 = random_light_hex()
    hex_2 = random_light_hex()
    c1_hex = document.getElementById("c1_hex")
    c2_hex = document.getElementById("c2_hex")
    c1_hex.value = hex_1
    c2_hex.value = hex_2

    callback_update_c1_lab_and_picker()
    callback_update_c2_lab_and_picker()

    callback_hex_lerp()

    # ------- Callbacks for start colour------- #
    c1_hex.addEventListener("input", create_proxy(callback_update_c1_lab_and_picker))

    c1_picker = document.getElementById("c1_picker")
    c1_picker.addEventListener("input", create_proxy(callback_update_c1_lab_and_hex))

    c1_lab = document.getElementById("c1_lab")
    c1_lab.addEventListener("input", create_proxy(callback_update_c1_picker_and_hex))

    # ------- Callbacks for end colour------- #
    c2_hex = document.getElementById("c2_hex")
    c2_hex.addEventListener("input", create_proxy(callback_update_c2_lab_and_picker))

    c2_picker = document.getElementById("c2_picker")
    c2_picker.addEventListener("input", create_proxy(callback_update_c2_lab_and_hex))

    c2_lab = document.getElementById("c2_lab")
    c2_lab.addEventListener("input", create_proxy(callback_update_c2_picker_and_hex))

    # ------- Callbacks for the interpolation value ------- #
    lerp_value = document.getElementById("lerp_value_output")
    lerp_value.addEventListener("input", create_proxy(callback_update_slider))

    lerp_slider = document.getElementById("lerp_value")
    lerp_slider.addEventListener("input", create_proxy(callback_update_slider_value))

    # ------- Callbacks for interpolating ------- #
    for element in [
        c1_hex,
        c1_picker,
        c1_lab,
        c2_hex,
        c2_picker,
        c2_lab,
        lerp_slider,
        lerp_value,
    ]:
        element.addEventListener("input", create_proxy(callback_hex_lerp))
