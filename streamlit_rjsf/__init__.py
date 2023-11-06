import hashlib
import os
from pathlib import Path
from typing import TypeVar

import streamlit.components.v1 as components
from jsonschema import Draft202012Validator, SchemaError
from pydantic import BaseModel, ValidationError

__all__ = ["raw_jsonform", "pydantic_jsonform", "SchemaError", "ValidationError"]
COMPONENT_NAME = "react_jsonform_component"

if bool(os.environ.get("USE_DEBUG_SERVER", False)):
    # Serve the npm server directly to get hot reloading.
    _component_func = components.declare_component(
        COMPONENT_NAME,
        url="http://localhost:3000",
    )
else:
    # Serve static build files
    here = Path(__file__).parent.absolute()
    build_dir = here / "build"
    assert (build_dir / "index.html").is_file(), "Frontend component not built!"
    _component_func = components.declare_component(COMPONENT_NAME, path=str(build_dir))


Schema = TypeVar("Schema", bound=BaseModel)


class FormData(BaseModel):
    errors: list = []
    formData: dict = {}
    schemaValidationErrors: list = []


def pydantic_jsonform(
    schema: type[Schema],
    ui_schema: dict = {},
    user_data: dict | None = None,
    key: str | None = None,
) -> None | Schema:
    """Render a web form corresponding to a pydantic model."""
    schema_dict = schema.model_json_schema()
    data = raw_jsonform(schema_dict, ui_schema, user_data, key)
    if data is None:
        return None
    return schema.model_validate(data)


def raw_jsonform(
    schema: dict,
    ui_schema: dict = {},
    user_data: dict | None = None,
    key: str | None = None,
) -> None | dict:
    """Render a web form using a json schema.
    Raises a SchemaError if the schema is invalid.
    """
    user_data_sha = _sha1(user_data)
    Draft202012Validator.check_schema(schema)
    component_value = _component_func(
        schema=schema,
        uiSchema=ui_schema,
        userData=user_data,
        key=f"{key}_{user_data_sha}",
        default=None,
        height=None,
    )
    if component_value is None:
        return None

    data = FormData.model_validate(component_value)
    if data.errors:
        raise ValidationError.from_exception_data("Invalid form data", data.errors)
    if data.schemaValidationErrors:
        raise SchemaError("Invalid schema", cause=data.schemaValidationErrors)
    return data.formData


def _sha1(user_data) -> str:
    sha1 = hashlib.sha1()
    sha1.update(str(user_data).encode("utf-8"))
    return sha1.hexdigest()
