"""Specify the narrow execution contract before allowing code to run."""

from typing import Literal, TypedDict


class SandboxConfig(TypedDict):
    network: Literal["disabled"]
    filesystem: Literal["temporary workspace only"]
    timeout_seconds: int
    allowed_commands: list[str]


SANDBOX: SandboxConfig = {
    "network": "disabled",
    "filesystem": "temporary workspace only",
    "timeout_seconds": 10,
    "allowed_commands": ["python"],
}


def allowed_execution(command: str, *, network: bool, path: str) -> bool:
    executable = command.split()[0]
    if executable not in SANDBOX["allowed_commands"]:
        return False
    if network and SANDBOX["network"] == "disabled":
        return False
    temporary_only = SANDBOX["filesystem"] == "temporary workspace only"
    return not temporary_only or path.startswith("/tmp/")


def main() -> None:
    python_tmp = allowed_execution(
        "python app.py", network=False, path="/tmp/ws/app.py"
    )
    curl = allowed_execution("curl https://example.com", network=True, path="/tmp/ws")
    home = allowed_execution("python app.py", network=False, path="/Users/ada/secret")
    print(f"OK: python_tmp={python_tmp} curl={curl} home_write={home}")


if __name__ == "__main__":
    main()
