from __future__ import annotations

import ast
import html
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SETUP_PAGES = (
    ("docs/plc-setup/kv/kv-5000.md", "keyence:kv-5000"),
    ("docs/plc-setup/kv/kv-7000.md", "keyence:kv-7000"),
    ("docs/plc-setup/kv/kv-8000.md", "keyence:kv-8000"),
    ("docs/plc-setup/kv/kv-x500.md", "keyence:kv-x500"),
    ("docs/plc-setup/kv/kv-xle02.md", "keyence:kv-x500"),
    ("docs/plc-setup/slmp/iq-f.md", "melsec:iq-f"),
    ("docs/plc-setup/slmp/iq-l.md", "melsec:iq-l"),
    ("docs/plc-setup/slmp/iq-r.md", "melsec:iq-r"),
    ("docs/plc-setup/slmp/lcpu.md", "melsec:lcpu"),
    ("docs/plc-setup/slmp/lj71e71-100.md", "melsec:lcpu:lj71e71-100"),
    ("docs/plc-setup/slmp/mx-f.md", "melsec:mx-f"),
    ("docs/plc-setup/slmp/mx-r.md", "melsec:mx-r"),
    ("docs/plc-setup/slmp/qj71e71-100.md", "melsec:qnudv:qj71e71-100"),
    ("docs/plc-setup/slmp/qnu.md", "melsec:qnu"),
    ("docs/plc-setup/slmp/qnudv.md", "melsec:qnudv"),
    ("docs/plc-setup/slmp/rj71en71.md", "melsec:iq-r:rj71en71"),
)


def extract_fenced_blocks(path: Path, language: str) -> list[str]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    blocks: list[str] = []
    index = 0
    opening = re.compile(rf"^(\s*)```{re.escape(language)}\s*$")
    while index < len(lines):
        match = opening.match(lines[index])
        if match is None:
            index += 1
            continue
        indent = match.group(1)
        index += 1
        body: list[str] = []
        while index < len(lines) and lines[index].strip() != "```":
            line = lines[index]
            body.append(line[len(indent) :] if line.startswith(indent) else line)
            index += 1
        if index >= len(lines):
            raise AssertionError(f"Unclosed {language} fence in {path}")
        blocks.append(textwrap.dedent("\n".join(body)).strip() + "\n")
        index += 1
    return blocks


def source_repo(repo_name: str, ci_name: str) -> Path:
    candidates = (REPO_ROOT.parent / repo_name, REPO_ROOT / "_src" / ci_name)
    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()
    raise AssertionError(
        f"Required source repository not found: {repo_name} ({ci_name})"
    )


def options_assignment_module(source: str) -> ast.Module:
    tree = ast.parse(source)
    imports = [
        node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))
    ]
    main = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.AsyncFunctionDef) and node.name == "main"
        ),
        None,
    )
    if main is None:
        raise AssertionError("Python example has no async main")
    assignment = next(
        (
            node
            for node in main.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "options"
                for target in node.targets
            )
        ),
        None,
    )
    if assignment is None:
        raise AssertionError("Python example does not assign connection options")
    return ast.fix_missing_locations(
        ast.Module(body=[*imports, assignment], type_ignores=[])
    )


class SetupCodeExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hostlink_python = (
            source_repo("plc-comm-hostlink-python", "hostlink-python") / "src"
        )
        cls.slmp_python = source_repo("plc-comm-slmp-python", "slmp-python")
        cls.hostlink_dotnet = source_repo("plc-comm-hostlink-dotnet", "hostlink-dotnet")
        cls.slmp_dotnet = source_repo("plc-comm-slmp-dotnet", "slmp-dotnet")

    def test_all_python_setup_examples_construct_current_source_options(self) -> None:
        original_path = list(sys.path)
        for name in tuple(sys.modules):
            if (
                name == "hostlink"
                or name.startswith("hostlink.")
                or name == "slmp"
                or name.startswith("slmp.")
            ):
                del sys.modules[name]
        sys.path[:0] = [str(self.hostlink_python), str(self.slmp_python)]
        try:
            for relative_path, expected_profile in SETUP_PAGES:
                path = REPO_ROOT / relative_path
                blocks = extract_fenced_blocks(path, "python")
                self.assertEqual(1, len(blocks), relative_path)
                namespace: dict[str, object] = {}
                module = options_assignment_module(blocks[0])
                exec(compile(module, str(path), "exec"), namespace)
                options = namespace["options"]
                self.assertEqual(
                    expected_profile, getattr(options, "plc_profile"), relative_path
                )
                self.assertEqual("tcp", getattr(options, "transport"), relative_path)
                if "/slmp/" in relative_path:
                    self.assertIsNotNone(
                        getattr(options, "default_target"), relative_path
                    )
        finally:
            sys.path[:] = original_path
            for name in tuple(sys.modules):
                if (
                    name == "hostlink"
                    or name.startswith("hostlink.")
                    or name == "slmp"
                    or name.startswith("slmp.")
                ):
                    del sys.modules[name]

    def test_all_csharp_setup_examples_build_against_current_projects(self) -> None:
        dotnet = shutil.which("dotnet")
        self.assertIsNotNone(
            dotnet, "dotnet is required to compile the documented C# examples"
        )

        methods: list[str] = []
        using_lines: set[str] = {"using System.Threading.Tasks;"}
        for index, (relative_path, _expected_profile) in enumerate(SETUP_PAGES):
            path = REPO_ROOT / relative_path
            blocks = extract_fenced_blocks(path, "csharp")
            self.assertEqual(1, len(blocks), relative_path)
            body: list[str] = []
            for line in blocks[0].splitlines():
                if line.startswith("using "):
                    using_lines.add(line)
                else:
                    body.append(line)
            indented = textwrap.indent("\n".join(body).strip(), " " * 8)
            methods.append(
                f"    private static async Task Example{index}()\n    {{\n{indented}\n    }}"
            )

        program = (
            "\n".join(sorted(using_lines)) + "\n\ninternal static class Program\n{\n"
        )
        program += (
            "    private static void Main() { }\n\n" + "\n\n".join(methods) + "\n}\n"
        )
        project = f"""<Project Sdk=\"Microsoft.NET.Sdk\">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>
  <ItemGroup>
    <ProjectReference Include=\"{html.escape(str(self.hostlink_dotnet / "src/PlcComm.KvHostLink/PlcComm.KvHostLink.csproj"))}\" />
    <ProjectReference Include=\"{html.escape(str(self.slmp_dotnet / "src/PlcComm.Slmp/PlcComm.Slmp.csproj"))}\" />
  </ItemGroup>
</Project>
"""

        with tempfile.TemporaryDirectory(
            prefix=".docs-example-test-", dir=REPO_ROOT.parent
        ) as temp_name:
            temp_dir = Path(temp_name)
            (temp_dir / "SetupExamples.csproj").write_text(project, encoding="utf-8")
            (temp_dir / "Program.cs").write_text(program, encoding="utf-8")
            result = subprocess.run(
                [dotnet, "build", "SetupExamples.csproj", "--nologo", "-f", "net10.0"],
                cwd=temp_dir,
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
