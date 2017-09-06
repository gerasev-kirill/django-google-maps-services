
MARKER_NAMED_COLORS = [
    'red', 'blue', 'green', 'orange', 'purple',
    'black', 'brown', 'yellow', 'gray', 'white'
]



def Client(*args, **kwargs):
    from .gmap.gmap import GMapClient
    return GMapClient(*args, **kwargs)


def StaticClient(*args, **kwargs):
    from .gmap.gmap_static import GMapStaticClient
    return GMapStaticClient(*args, **kwargs)
