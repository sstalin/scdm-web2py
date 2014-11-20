def index():
    latitude = 42.023333
    longitude = -87.790755
    set_up_layers()
    return locals()


def set_up_layers():
    response.layers = ["NGS(3D)", "NGS(2D)", "NGS(1D)"]

@cache.action()
def download():
    return response.download(request, db)