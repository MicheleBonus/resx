from typing import Dict, Optional, Tuple
from flask import jsonify


class ValidationResult:
    def __init__(self, data: Dict[str, object], error: Optional[Tuple[dict, int]] = None):
        self.data = data
        self.error = error


def _missing_field(field: str) -> Tuple[dict, int]:
    return {"error": f"Missing required field: {field}"}, 400


def _invalid_number(field: str) -> Tuple[dict, int]:
    return {"error": f"{field} must be an integer"}, 400


def _invalid_window() -> Tuple[dict, int]:
    return {"error": "window must be an integer between 0 and 10"}, 400


def _invalid_insertion_code() -> Tuple[dict, int]:
    return {"error": "insertion_code must be a single character"}, 400


def validate_request(form, required_fields, *, allow_insertion_code: bool = False) -> ValidationResult:
    data: Dict[str, object] = {}

    for field in required_fields:
        value = form.get(field)
        if value is None or value == "":
            return ValidationResult({}, _missing_field(field))
        data[field] = value

    try:
        data["residue"] = int(data["residue"])
    except (KeyError, ValueError, TypeError):
        return ValidationResult({}, _invalid_number("residue"))

    window_raw = form.get("window", "0")
    try:
        window = int(window_raw)
    except (ValueError, TypeError):
        return ValidationResult({}, _invalid_number("window"))

    if window < 0 or window > 10:
        return ValidationResult({}, _invalid_window())

    data["window"] = window

    if allow_insertion_code:
        insertion_code = form.get("insertion_code", "")
        if insertion_code and len(insertion_code) > 1:
            return ValidationResult({}, _invalid_insertion_code())
        data["insertion_code"] = insertion_code

    return ValidationResult(data)


def handle_validation(result: ValidationResult):
    if result.error:
        error_body, status = result.error
        return jsonify(error_body), status
    return None
