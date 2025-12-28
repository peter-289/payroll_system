def _generate_deduction_code( name: str) -> str:
        import uuid
        prefix = name[:4].upper()
        unique_suffix = uuid.uuid4().hex[:6].upper()
        code = f"{prefix}-{unique_suffix}"
        return code

code = _generate_deduction_code("peter")
print(code)