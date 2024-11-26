def parse_nested_deps(input: dict[str, str], output: set[str]) -> None:
    for k, v in input.items():
        if isinstance(v, dict):
            v = v.get("version", "*").strip("=")
        output.add(f"{k}={v}")
