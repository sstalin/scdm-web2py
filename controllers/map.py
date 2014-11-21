def index():
    """
    Sets location on map
    :return:
    """
    latitude = 42.023333
    longitude = -87.790755
    setLocation = DEBUG
    # set_up_layers()
    return locals()

#
# def set_up_layers():
#     response.layers = ["NGS(3D)", "NGS(2D)", "NGS(1D)"]

@cache.action()
def download():
    return response.download(request, db)