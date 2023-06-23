import string
import types
import uuid
from datetime import datetime
from random import choice, randint

import pytest


def gen_integer(min_int: int = 10, max_int: int = 1000) -> int:
    return randint(min_int, max_int)


def gen_string(max_length: int) -> str:
    return str(
        "".join(choice(string.ascii_letters) for _ in range(max_length))
    )


def gen_date_time() -> datetime:
    return datetime.now()


def gen_uuid() -> uuid.uuid4:
    return uuid.uuid4()


def gen_email() -> str:
    return f'{gen_string(5)}@example.com'


def generate_str(format: str) -> str | datetime | uuid.UUID:
    if format is None:
        return gen_string(10)
    elif format == 'date-time':
        return gen_date_time()
    elif format == 'uuid':
        return gen_uuid()
    elif format == 'email':
        return gen_email()
    else:
        raise ValueError(f"Unsupported format {format}")


def generate_for_type(_type: str, _format: str | None = None):
    if _type == 'string':
        return generate_str(_format)
    elif _type == 'integer':
        return gen_integer()
    else:
        raise ValueError("Unsupported type")


def generate_one_instance(model_klass, **desired_instance_attrs):
    attrs = {}

    for prop, value in model_klass.schema()['properties'].items():
        if prop in desired_instance_attrs.keys():
            attrs[prop] = desired_instance_attrs.get(prop)
        else:
            attrs[prop] = generate_for_type(
                value.get('type'),
                value.get('format', None)
            )

    return model_klass(**attrs)


def generate_instance(model_klass, _quantity=1, **desired_instance_attrs):

    gen_attrs = {}
    result = []

    if _quantity > 1:
        for key, value in desired_instance_attrs.items():
            if isinstance(value, types.GeneratorType):
                gen_attrs[key] = list(value)

        for idx in range(0, _quantity):
            for attr_name, _list in gen_attrs.items():
                desired_instance_attrs[attr_name] = _list[idx]
            result.append(
                generate_one_instance(model_klass, **desired_instance_attrs)
            )

        return result

    return generate_one_instance(model_klass, **desired_instance_attrs)


class Maker:
    def __init__(self):
        self._model_klass = None

    @classmethod
    def create(cls, model_klass, **desired_instance_attrs):
        """Builds an instance of model_klass"""
        return generate_instance(model_klass, **desired_instance_attrs)


@pytest.fixture()
def maker():
    return Maker()
