from datetime import datetime, timedelta

import pytest
import six
from hypothesis import assume, given
from hypothesis import strategies as st

from dateutil import tz as tz

EPOCHALYPSE = datetime.fromtimestamp(2147483647)
NEGATIVE_EPOCHALYPSE = datetime.fromtimestamp(0) - timedelta(seconds=2147483648)


@pytest.mark.gettz
@given(key=st.timezone_keys(allow_prefix=True))
def test_key_property(key):
    tzi = tz.gettz(key)
    assume(isinstance(tzi, tz.tzfile))
    assert tzi.key == key


@pytest.mark.gettz
@pytest.mark.skipif(six.PY2, reason="Not supported on Python 2")
@pytest.mark.parametrize("gettz_arg", [None, ""])
# TODO: Remove bounds when GH #590 is resolved
@given(
    dt=st.datetimes(
        min_value=NEGATIVE_EPOCHALYPSE, max_value=EPOCHALYPSE, timezones=st.just(tz.UTC),
    )
)
def test_gettz_returns_local(gettz_arg, dt):
    act_tz = tz.gettz(gettz_arg)
    if isinstance(act_tz, tz.tzlocal):
        return

    dt_act = dt.astimezone(tz.gettz(gettz_arg))
    dt_exp = dt.astimezone()

    assert dt_act == dt_exp
    assert dt_act.tzname() == dt_exp.tzname()
    assert dt_act.utcoffset() == dt_exp.utcoffset()
