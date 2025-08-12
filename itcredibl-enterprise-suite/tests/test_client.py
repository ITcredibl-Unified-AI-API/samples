import os

import pytest
from itcredibl_enterprise.client import ITCAuthError, ITcrediblClient


def test_missing_key():
    old = os.environ.pop("ITCREDIBL_API_KEY", None)
    try:
        with pytest.raises(ITCAuthError):
            ITcrediblClient()
    finally:
        if old:
            os.environ["ITCREDIBL_API_KEY"] = old
