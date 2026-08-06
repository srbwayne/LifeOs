from tsidpy import TSID


def new_tsid() -> str:
    """Gera um novo TSID como string."""
    return TSID.create().to_string()
