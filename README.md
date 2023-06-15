# HexLerp
HexLerp interpolates between two colours in a <a href="https://programmingdesignsystems.com/color/perceptually-uniform-color-spaces/">perceptually meaningful way</a> by performing the interpolation in the <a href="https://en.wikipedia.org/wiki/CIELAB_color_space">CIELAB</a> colour space.

You can use the colour picker, type in HEX values or type in LAB values -- the other colour representations will automatically update.

The interpolation value specifies how close the interpolated value should be to the start/end point (0 being equal to start and 1 being equal to end).

This app is powered by <a href="https://pyscript.net">PyScript</a>, a Python runtime for the browser. This is mostly a fun project to learn about PyScript and there are still some bugs to sort out :)

You can view the app on <a href="https://marieroald.github.io/hexlerp">GitHub Pages</a>