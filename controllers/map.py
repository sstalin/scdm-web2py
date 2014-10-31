def index():
    latitude = 42.0104
    longitude = -87.4351
    set_up_layers()
    return locals()


def set_up_layers():
    response.layers = ["NGS(3D)", "NGS(2D)", "NGS(1D)"]