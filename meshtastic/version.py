""" Version lookup utilities, isolated for cleanliness """
import sys
try:
    from importlib.metadata import version, PackageNotFoundError
except:
    import pkg_resources

__version__ = "2.3.10"


def get_active_version():
    """Get the currently active version using importlib, or pkg_resources if we must"""
    try:
        if "importlib.metadata" in sys.modules:
            return version("meshtastic")
        else:
            return pkg_resources.get_distribution("meshtastic").version  # pylint: disable=E0601
    except PackageNotFoundError:
        return __version__
