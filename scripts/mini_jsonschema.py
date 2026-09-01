"""Minimal JSON Schema validator (deterministic, dependency-free).

Supports exactly the draft-07 subset used by the CQC P0 schema:
type (incl. unions), const, enum, required, properties,
additionalProperties (bool), items, minItems, minLength, pattern.
Unsupported keywords raise UnsupportedSchemaFeatureError at load-check time
(fail closed, never silent pass).
"""
from __future__ import annotations

import re


class UnsupportedSchemaFeatureError(Exception):
    pass


def _check_schema_keywords(schema):
    allowed = {
        "$schema", "title", "description", "type", "const", "enum",
        "required", "properties", "additionalProperties", "items",
        "minItems", "minLength", "pattern",
    }
    for k in schema:
        if k not in allowed:
            raise UnsupportedSchemaFeatureError(f"schema keyword not supported by mini validator: {k!r}")
    if "items" in schema and isinstance(schema["items"], dict):
        _check_schema_keywords(schema["items"])
    for sub in (schema.get("properties") or {}).values():
        _check_schema_keywords(sub)


def _type_ok(instance, name) -> bool:
    if name == "object":
        return isinstance(instance, dict)
    if name == "array":
        return isinstance(instance, list)
    if name == "string":
        return isinstance(instance, str)
    if name == "null":
        return instance is None
    if name == "boolean":
        return isinstance(instance, bool)
    if name in ("number", "integer"):
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    return False


def validate(instance, schema, path="$") -> list[str]:
    errors: list[str] = []
    t = schema.get("type")
    if t is not None:
        names = t if isinstance(t, list) else [t]
        if not any(_type_ok(instance, n) for n in names):
            return [f"{path}: expected type {'/'.join(names)}, got {type(instance).__name__}"]
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: const mismatch (expected {schema['const']!r})")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value not in enum")
    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: minLength {schema['minLength']} violated")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"{path}: pattern {schema['pattern']} not matched")
    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errors.append(f"{path}: missing required property '{req}'")
        props = schema.get("properties", {})
        addl = schema.get("additionalProperties", True)
        for key, val in instance.items():
            if key in props:
                errors.extend(validate(val, props[key], f"{path}.{key}"))
            elif addl is False:
                errors.append(f"{path}: additional property '{key}' not allowed")
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: minItems {schema['minItems']} violated")
        items = schema.get("items")
        if isinstance(items, dict):
            for i, item in enumerate(instance):
                errors.extend(validate(item, items, f"{path}[{i}]"))
    return errors
