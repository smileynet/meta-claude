#!/usr/bin/env python3
"""Documentation validator for meta-agentic best practices.

Validates markdown files for structure, links, and content quality.
Supports auto-fixing safe issues like formatting and missing frontmatter.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


@dataclass
class Issue:
    """A validation issue."""

    file: Path
    line: int | None
    category: Literal["structure", "links", "content"]
    severity: Literal["error", "warning", "info"]
    message: str
    auto_fixable: bool = False
    fix_description: str | None = None

    def __str__(self) -> str:
        line_str = f"Line {self.line}" if self.line else "Line -"
        severity_str = f"[{self.severity.upper()}]"
        return f"  {severity_str:10} {line_str}: {self.message}"


@dataclass
class ValidationResult:
    """Results from validating a file or directory."""

    target: Path
    issues: list[Issue] = field(default_factory=list)
    auto_fixed: list[str] = field(default_factory=list)
    files_checked: int = 0

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")

    @property
    def info_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "info")

    @property
    def status(self) -> str:
        if self.error_count > 0:
            return "FAIL"
        elif self.warning_count > 0:
            return "WARN"
        else:
            return "PASS"


class DocValidator:
    """Validates documentation files against meta-agentic best practices."""

    # Thresholds
    MAX_SKILL_LINES = 500
    OPTIMAL_SKILL_LINES = 150

    # Valid tool names for allowed-tools field
    VALID_TOOLS = {
        "Read", "Write", "Edit", "Grep", "Glob", "Bash",
        "WebFetch", "WebSearch", "Task", "TodoWrite",
        "NotebookEdit", "AskUserQuestion", "LSP"
    }

    # Valid model names for agents
    VALID_MODELS = {"haiku", "sonnet", "opus"}

    def __init__(self, target: Path, auto_fix: bool = False, dry_run: bool = False):
        self.target = target
        self.auto_fix = auto_fix
        self.dry_run = dry_run
        self.issues: list[Issue] = []
        self.fixed: list[str] = []
        self.files_checked = 0

    def validate(self) -> ValidationResult:
        """Run all validation checks."""
        if self.target.is_file():
            self._validate_file(self.target)
        else:
            self._validate_directory(self.target)

        return ValidationResult(
            target=self.target,
            issues=self.issues,
            auto_fixed=self.fixed,
            files_checked=self.files_checked,
        )

    def _add_issue(
        self,
        file: Path,
        line: int | None,
        category: Literal["structure", "links", "content"],
        severity: Literal["error", "warning", "info"],
        message: str,
        auto_fixable: bool = False,
        fix_description: str | None = None,
    ) -> None:
        """Add a validation issue."""
        self.issues.append(
            Issue(
                file=file,
                line=line,
                category=category,
                severity=severity,
                message=message,
                auto_fixable=auto_fixable,
                fix_description=fix_description,
            )
        )

    def _validate_file(self, path: Path) -> None:
        """Validate a single markdown file."""
        if path.suffix.lower() != ".md":
            return

        self.files_checked += 1

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            self._add_issue(path, None, "structure", "error", f"Cannot read file: {e}")
            return

        lines = content.splitlines()

        # Run checks
        content = self._check_formatting(path, content, lines)
        self._check_frontmatter(path, content, lines)
        self._check_links(path, content, lines)
        self._check_size(path, lines)

    def _validate_directory(self, path: Path) -> None:
        """Validate a directory (skill, commands, etc.)."""
        # Check if this is a skill directory
        skill_md = path / "SKILL.md"
        if path.name not in ("skills", "commands", "agents", "scripts"):
            if not skill_md.exists():
                # Check if parent is 'skills' directory
                if path.parent.name == "skills":
                    self._add_issue(
                        path, None, "structure", "error",
                        "Skill directory missing SKILL.md"
                    )

        # Validate all markdown files
        for md_file in path.rglob("*.md"):
            self._validate_file(md_file)

    def _check_formatting(self, path: Path, content: str, lines: list[str]) -> str:
        """Check and optionally fix formatting issues."""
        modified = False
        new_lines = []
        in_code_block = False

        for i, line in enumerate(lines, 1):
            original_line = line

            # Track code block state
            stripped = line.strip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_code_block = not in_code_block

            # Check for tabs (skip code blocks)
            if "\t" in line and not in_code_block:
                self._add_issue(
                    path, i, "content", "warning",
                    "Tab character found (use spaces)",
                    auto_fixable=True,
                    fix_description="Convert tabs to spaces"
                )
                if self.auto_fix:
                    line = line.replace("\t", "  ")
                    if line != original_line:
                        modified = True
                        if not self.dry_run:
                            self.fixed.append(f"{path.name}:{i} - Converted tabs to spaces")

            # Check for trailing whitespace
            if line.rstrip() != line:
                self._add_issue(
                    path, i, "content", "info",
                    "Trailing whitespace",
                    auto_fixable=True,
                    fix_description="Remove trailing whitespace"
                )
                if self.auto_fix:
                    line = line.rstrip()
                    if line != original_line:
                        modified = True
                        if not self.dry_run:
                            self.fixed.append(f"{path.name}:{i} - Removed trailing whitespace")

            new_lines.append(line)

        # Check for final newline
        if content and not content.endswith("\n"):
            self._add_issue(
                path, None, "content", "info",
                "Missing final newline",
                auto_fixable=True,
                fix_description="Add final newline"
            )
            if self.auto_fix:
                modified = True
                if not self.dry_run:
                    self.fixed.append(f"{path.name} - Added final newline")

        # Write fixes
        if modified and self.auto_fix and not self.dry_run:
            new_content = "\n".join(new_lines)
            if not new_content.endswith("\n"):
                new_content += "\n"
            path.write_text(new_content, encoding="utf-8")
            return new_content

        return content

    def _check_frontmatter(self, path: Path, content: str, lines: list[str]) -> None:
        """Check YAML frontmatter validity."""
        # Only SKILL.md files require frontmatter
        is_skill_md = path.name == "SKILL.md"

        # Check for frontmatter presence
        if not lines or lines[0] != "---":
            if is_skill_md:
                self._add_issue(
                    path, 1, "content", "error",
                    "Missing YAML frontmatter (should start with ---)",
                    auto_fixable=True,
                    fix_description="Add frontmatter delimiters"
                )
                if self.auto_fix and not self.dry_run:
                    # Add frontmatter
                    folder_name = path.parent.name
                    new_content = f'---\nname: {folder_name}\ndescription: "TODO: Add description with trigger keywords"\n---\n\n{content}'
                    path.write_text(new_content, encoding="utf-8")
                    self.fixed.append(f"{path.name} - Added frontmatter with name and description")
            return

        # Find closing ---
        end_idx = None
        for i, line in enumerate(lines[1:], 2):
            if line == "---":
                end_idx = i
                break

        if end_idx is None:
            self._add_issue(
                path, None, "content", "error",
                "Frontmatter not closed (missing closing ---)"
            )
            return

        # Parse YAML
        frontmatter_text = "\n".join(lines[1:end_idx-1])
        try:
            frontmatter = yaml.safe_load(frontmatter_text) or {}
        except yaml.YAMLError as e:
            self._add_issue(
                path, None, "content", "error",
                f"Invalid YAML in frontmatter: {e}"
            )
            return

        # Check required fields (only for SKILL.md)
        if is_skill_md:
            if "name" not in frontmatter:
                self._add_issue(
                    path, None, "content", "error",
                    "Missing required field: name",
                    auto_fixable=True,
                    fix_description="Generate name from folder"
                )

            if "description" not in frontmatter:
                self._add_issue(
                    path, None, "content", "error",
                    "Missing required field: description",
                    auto_fixable=True,
                    fix_description="Add placeholder description"
                )
            elif frontmatter.get("description"):
                desc = frontmatter["description"]
                # Check description quality
                if len(desc) < 20:
                    self._add_issue(
                        path, None, "content", "warning",
                        f"Description too short ({len(desc)} chars). Add trigger keywords."
                    )
                if "use when" not in desc.lower() and "use for" not in desc.lower():
                    self._add_issue(
                        path, None, "content", "info",
                        "Description could include 'Use when...' trigger phrases"
                    )

            # Check name format
            if "name" in frontmatter:
                name = frontmatter["name"]
                if not re.match(r"^[a-z0-9-]+$", name):
                    self._add_issue(
                        path, None, "content", "warning",
                        f"Name '{name}' should use only lowercase, numbers, and hyphens"
                    )

        # Check allowed-tools if present
        if "allowed-tools" in frontmatter:
            tools_str = frontmatter["allowed-tools"]
            if isinstance(tools_str, str):
                tools = [t.strip() for t in tools_str.split(",")]
                for tool in tools:
                    if tool and tool not in self.VALID_TOOLS:
                        self._add_issue(
                            path, None, "content", "warning",
                            f"Unknown tool in allowed-tools: {tool}"
                        )

        # Check model if present (for agents)
        if "model" in frontmatter:
            model = frontmatter["model"]
            if model not in self.VALID_MODELS:
                self._add_issue(
                    path, None, "content", "error",
                    f"Invalid model: {model}. Use: {', '.join(self.VALID_MODELS)}"
                )

    def _is_in_code_block(self, lines: list[str], line_num: int) -> bool:
        """Check if a line number is inside a fenced code block."""
        in_code_block = False
        for i, line in enumerate(lines[:line_num], 1):
            stripped = line.strip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_code_block = not in_code_block
        return in_code_block

    def _check_links(self, path: Path, content: str, lines: list[str]) -> None:
        """Check internal links and references."""
        # Pattern for markdown links: [text](path)
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

        for i, line in enumerate(lines, 1):
            # Skip lines inside code blocks
            if self._is_in_code_block(lines, i - 1):
                continue

            # Skip inline code
            line_no_inline_code = re.sub(r'`[^`]+`', '', line)

            for match in link_pattern.finditer(line_no_inline_code):
                link_text, link_path = match.groups()

                # Skip external links
                if link_path.startswith(("http://", "https://", "mailto:")):
                    continue

                # Skip anchor links
                if link_path.startswith("#"):
                    continue

                # Skip ~ paths (user home relative - can't validate portably)
                if link_path.startswith("~"):
                    continue

                # Resolve relative path
                if link_path.startswith("/"):
                    target = Path(link_path)
                else:
                    target = path.parent / link_path

                # Remove anchor from path
                target_str = str(target).split("#")[0]
                target = Path(target_str)

                if not target.exists():
                    self._add_issue(
                        path, i, "links", "error",
                        f"Broken link: [{link_text}]({link_path}) - file not found"
                    )

        # Check @file references
        at_pattern = re.compile(r'@([~./][^\s\n`]+)')
        for i, line in enumerate(lines, 1):
            # Skip lines inside code blocks
            if self._is_in_code_block(lines, i - 1):
                continue

            # Skip inline code
            line_no_inline_code = re.sub(r'`[^`]+`', '', line)

            for match in at_pattern.finditer(line_no_inline_code):
                ref_path = match.group(1)

                # Skip paths with wildcards or regex patterns
                if any(c in ref_path for c in ['*', '?', '"', "'"]):
                    continue

                # Expand ~
                if ref_path.startswith("~"):
                    ref_path = str(Path.home()) + ref_path[1:]

                target = Path(ref_path)
                if not target.exists():
                    self._add_issue(
                        path, i, "links", "error",
                        f"Broken @file reference: {match.group(0)} - file not found"
                    )

    def _check_size(self, path: Path, lines: list[str]) -> None:
        """Check file size for progressive disclosure."""
        line_count = len(lines)

        if path.name == "SKILL.md":
            if line_count > self.MAX_SKILL_LINES:
                self._add_issue(
                    path, None, "structure", "warning",
                    f"File is {line_count} lines (threshold: {self.MAX_SKILL_LINES}). "
                    "Consider splitting into supporting files."
                )
            elif line_count > self.OPTIMAL_SKILL_LINES:
                self._add_issue(
                    path, None, "structure", "info",
                    f"File is {line_count} lines. "
                    f"Optimal is under {self.OPTIMAL_SKILL_LINES} lines."
                )


def format_console_output(result: ValidationResult) -> str:
    """Format validation results for console output."""
    output = []
    output.append(f"\nValidating: {result.target}\n")

    # Group issues by file
    issues_by_file: dict[Path, list[Issue]] = {}
    for issue in result.issues:
        if issue.file not in issues_by_file:
            issues_by_file[issue.file] = []
        issues_by_file[issue.file].append(issue)

    for file_path, issues in sorted(issues_by_file.items()):
        output.append(f"\n{file_path}")
        for issue in sorted(issues, key=lambda x: (x.line or 0)):
            output.append(str(issue))

    # Auto-fixed items
    if result.auto_fixed:
        output.append("\nAuto-fixed:")
        for fix in result.auto_fixed:
            output.append(f"  -> {fix}")

    # Summary
    output.append("\nSUMMARY")
    output.append("=" * 63)
    output.append(f"Files checked:    {result.files_checked}")
    output.append(f"Errors:           {result.error_count}")
    output.append(f"Warnings:         {result.warning_count}")
    output.append(f"Info:             {result.info_count}")
    if result.auto_fixed:
        output.append(f"Auto-fixed:       {len(result.auto_fixed)} issues")
    output.append(f"Status:           {result.status}")

    return "\n".join(output)


def format_json_output(result: ValidationResult) -> str:
    """Format validation results as JSON."""
    data = {
        "target": str(result.target),
        "summary": {
            "files_checked": result.files_checked,
            "errors": result.error_count,
            "warnings": result.warning_count,
            "info": result.info_count,
            "auto_fixed": len(result.auto_fixed),
            "status": result.status,
        },
        "issues": [
            {
                "file": str(issue.file),
                "line": issue.line,
                "category": issue.category,
                "severity": issue.severity,
                "message": issue.message,
                "auto_fixable": issue.auto_fixable,
            }
            for issue in result.issues
        ],
        "auto_fixed": result.auto_fixed,
    }
    return json.dumps(data, indent=2)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate documentation against meta-agentic best practices"
    )
    parser.add_argument(
        "path",
        type=Path,
        help="File or directory to validate"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix safe issues"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fixed without modifying files"
    )
    parser.add_argument(
        "--format",
        choices=["console", "json"],
        default="console",
        help="Output format (default: console)"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error code 1 on any issue"
    )

    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: Path not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    validator = DocValidator(
        target=args.path,
        auto_fix=args.fix,
        dry_run=args.dry_run,
    )
    result = validator.validate()

    if args.format == "json":
        print(format_json_output(result))
    else:
        print(format_console_output(result))

    # Exit code
    if args.strict and (result.error_count > 0 or result.warning_count > 0):
        sys.exit(1)
    elif result.error_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
