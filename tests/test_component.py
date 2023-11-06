from pydantic import BaseModel

from streamlit_rjsf import pydantic_jsonform, raw_jsonform


def test_raw_init():
    comp = raw_jsonform({})
    assert comp is None


def test_raw_with_user_data():
    comp = raw_jsonform({}, user_data={"foo": "bar"})
    assert comp is None


def test_pydantic_with_data():
    class Model(BaseModel):
        foo: str

    comp = pydantic_jsonform(Model)
    assert comp is None
