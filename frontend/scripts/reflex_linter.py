#!/usr/bin/env python3
"""
Custom Reflex Linter - Catches common Reflex mistakes BEFORE compilation.

This linter checks for:
1. Invalid font weights (numeric strings like "700" instead of "bold")
2. Invalid icon names (old format vs Lucide format)
3. Python conditionals with Reflex vars (should use rx.cond)
4. Python slicing/indexing on Reflex vars
5. f-strings with potential Reflex state variables
6. Deprecated rx.Base usage

Run: python scripts/reflex_linter.py [files...]
Exit code 0 = no errors, 1 = errors found
"""

import re
import sys
import ast
from pathlib import Path
from typing import List, Tuple, NamedTuple
from dataclasses import dataclass


@dataclass
class LintError:
    """Represents a linting error."""
    file: str
    line: int
    column: int
    code: str
    message: str
    
    def __str__(self):
        return f"{self.file}:{self.line}:{self.column}: {self.code} {self.message}"


# ============ CONFIGURATION ============

# Invalid numeric font weights - should use string literals
INVALID_WEIGHTS = {
    '"100"': '"light"',
    '"200"': '"light"',
    '"300"': '"light"',
    '"400"': '"regular"',
    '"500"': '"medium"',
    '"600"': '"bold"',
    '"700"': '"bold"',
    '"800"': '"bold"',
    '"900"': '"bold"',
    "'100'": '"light"',
    "'200'": '"light"',
    "'300'": '"light"',
    "'400'": '"regular"',
    "'500'": '"medium"',
    "'600'": '"bold"',
    "'700'": '"bold"',
    "'800'": '"bold"',
    "'900'": '"bold"',
}

# Invalid icon names (old -> new Lucide format)
INVALID_ICONS = {
    "check-circle": "circle-check",
    "check_circle": "circle-check",
    "alert-circle": "circle-alert",
    "alert_circle": "circle-alert",
    "x-circle": "circle-x",
    "x_circle": "circle-x",
    "info-circle": "circle-info",  
    "info_circle": "circle-info",
    "more-vertical": "ellipsis-vertical",
    "more_vertical": "ellipsis-vertical",
    "more-horizontal": "ellipsis",
    "more_horizontal": "ellipsis",
    "chevron-down": "chevron-down",  # This one is correct
    "arrow-left": "arrow-left",  # This one is correct
}

# Patterns that indicate problematic Python operations on Reflex vars
PROBLEMATIC_PATTERNS = [
    # Python slicing on potential Reflex vars: var[:2], var[0]
    (r'\b(\w+)\s*\[\s*:\s*\d+\s*\]', 'RFX003', 'Potential Python slicing on Reflex var. Use rx.cond or state method instead.'),
    (r'\b(\w+)\s*\[\s*\d+\s*\](?!\s*[=,\]\)])', 'RFX004', 'Potential Python indexing on Reflex var. Consider using state method.'),
]

# rx.Base deprecation pattern
RX_BASE_PATTERN = r'class\s+\w+\s*\(\s*rx\.Base\s*\)'


class ReflexLinter:
    """Linter for Reflex-specific issues."""
    
    def __init__(self):
        self.errors: List[LintError] = []
    
    def lint_file(self, filepath: Path) -> List[LintError]:
        """Lint a single file and return errors."""
        self.errors = []
        
        try:
            content = filepath.read_text(encoding='utf-8')
            lines = content.split('\n')
        except Exception as e:
            self.errors.append(LintError(
                file=str(filepath),
                line=0,
                column=0,
                code='RFX000',
                message=f'Could not read file: {e}'
            ))
            return self.errors
        
        # Run all checks
        self._check_font_weights(filepath, lines)
        self._check_icon_names(filepath, lines)
        self._check_rx_base_deprecation(filepath, lines)
        self._check_python_conditionals_in_rx(filepath, content, lines)
        self._check_problematic_patterns(filepath, lines)
        self._check_fstrings_with_state(filepath, content, lines)
        
        return self.errors
    
    def _check_font_weights(self, filepath: Path, lines: List[str]):
        """Check for invalid numeric font weights."""
        for line_num, line in enumerate(lines, 1):
            # Look for weight= assignments
            if 'weight=' in line or 'weight:' in line:
                for invalid, suggestion in INVALID_WEIGHTS.items():
                    if invalid in line:
                        col = line.find(invalid)
                        self.errors.append(LintError(
                            file=str(filepath),
                            line=line_num,
                            column=col + 1,
                            code='RFX001',
                            message=f'Invalid font weight {invalid}. Use {suggestion} instead. '
                                    f'Valid values: "light", "regular", "medium", "bold"'
                        ))
    
    def _check_icon_names(self, filepath: Path, lines: List[str]):
        """Check for invalid/old icon names."""
        for line_num, line in enumerate(lines, 1):
            # Look for rx.icon calls
            if 'rx.icon(' in line or 'icon=' in line:
                for old_name, new_name in INVALID_ICONS.items():
                    # Check various quote styles
                    patterns = [f'"{old_name}"', f"'{old_name}'", f'tag="{old_name}"', f"tag='{old_name}'"]
                    for pattern in patterns:
                        if pattern in line and old_name != new_name:
                            col = line.find(pattern)
                            self.errors.append(LintError(
                                file=str(filepath),
                                line=line_num,
                                column=col + 1,
                                code='RFX002',
                                message=f'Invalid icon name "{old_name}". Use "{new_name}" instead. '
                                        f'See: https://reflex.dev/docs/library/data-display/icon/'
                            ))
    
    def _check_rx_base_deprecation(self, filepath: Path, lines: List[str]):
        """Check for deprecated rx.Base usage."""
        for line_num, line in enumerate(lines, 1):
            if re.search(RX_BASE_PATTERN, line):
                col = line.find('rx.Base')
                self.errors.append(LintError(
                    file=str(filepath),
                    line=line_num,
                    column=col + 1 if col >= 0 else 1,
                    code='RFX005',
                    message='rx.Base is deprecated (removed in 0.9.0). Use pydantic.BaseModel instead.'
                ))
    
    def _check_python_conditionals_in_rx(self, filepath: Path, content: str, lines: List[str]):
        """Check for Python if/else with Reflex state variables inside rx components."""
        # Pattern: var.field if var.field else "default" (inside rx context)
        # This is tricky - we look for patterns like `state.var if state.var`
        pattern = r'(\w+\.\w+)\s+if\s+\1\s+else'
        
        for line_num, line in enumerate(lines, 1):
            # Skip comment lines
            stripped = line.strip()
            if stripped.startswith('#'):
                continue
            
            # Look for the pattern
            match = re.search(pattern, line)
            if match:
                # Check if we're inside an rx component context (heuristic)
                if any(rx_indicator in line for rx_indicator in ['rx.', 'size=', 'color=', 'weight=']):
                    col = match.start()
                    self.errors.append(LintError(
                        file=str(filepath),
                        line=line_num,
                        column=col + 1,
                        code='RFX006',
                        message=f'Python conditional with Reflex var "{match.group(1)}". '
                                f'Use rx.cond({match.group(1)}, ..., ...) instead.'
                    ))
    
    def _check_problematic_patterns(self, filepath: Path, lines: List[str]):
        """Check for problematic patterns like slicing/indexing."""
        for line_num, line in enumerate(lines, 1):
            # Skip comment lines and string definitions
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                continue
            
            # Check if line seems to be in rx component context
            if not any(indicator in line for indicator in ['rx.', 'AppState.', 'self.']):
                continue
                
            for pattern, code, message in PROBLEMATIC_PATTERNS:
                match = re.search(pattern, line)
                if match:
                    # Avoid false positives on list literals and dict access
                    if '[' in line and ']' in line:
                        # Skip if it's clearly a list literal like [1, 2, 3]
                        if re.search(r'\[\s*\d+\s*,', line):
                            continue
                        # Skip dictionary string key access
                        if re.search(r'\[\s*["\']', line):
                            continue
                    
                    col = match.start()
                    self.errors.append(LintError(
                        file=str(filepath),
                        line=line_num,
                        column=col + 1,
                        code=code,
                        message=message
                    ))
    
    def _check_fstrings_with_state(self, filepath: Path, content: str, lines: List[str]):
        """Check for f-strings that might contain state variables."""
        # Pattern: f"...{state.var}..." or f"...{self.var}..."
        pattern = r'f["\'][^"\']*\{(AppState\.\w+|self\.\w+)[^}]*\}[^"\']*["\']'
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('#'):
                continue
            
            # Look for f-strings with state references
            match = re.search(pattern, line)
            if match:
                # Check if inside rx component (rx.text, etc.)
                if 'rx.text(' in line or 'rx.heading(' in line or 'rx.badge(' in line:
                    col = match.start()
                    self.errors.append(LintError(
                        file=str(filepath),
                        line=line_num,
                        column=col + 1,
                        code='RFX007',
                        message=f'f-string with state variable in rx component. '
                                f'Pass state var directly to rx.text() or use rx.text(state.var) instead.'
                    ))


def main():
    """Main entry point."""
    # Get files to lint
    if len(sys.argv) > 1:
        files = [Path(f) for f in sys.argv[1:]]
    else:
        # Default: lint all Python files in barber_crm
        base_path = Path(__file__).parent.parent / 'barber_crm'
        files = list(base_path.rglob('*.py'))
    
    linter = ReflexLinter()
    all_errors: List[LintError] = []
    
    for filepath in files:
        if not filepath.exists():
            print(f"Warning: File not found: {filepath}", file=sys.stderr)
            continue
        
        if filepath.suffix != '.py':
            continue
            
        errors = linter.lint_file(filepath)
        all_errors.extend(errors)
    
    # Print errors
    if all_errors:
        print(f"\n{'='*60}")
        print(f"🚨 REFLEX LINTER: Found {len(all_errors)} error(s)")
        print(f"{'='*60}\n")
        
        for error in sorted(all_errors, key=lambda e: (e.file, e.line)):
            print(f"  {error}")
        
        print(f"\n{'='*60}")
        print("Fix these issues before committing!")
        print(f"{'='*60}\n")
        
        return 1
    else:
        print("✅ Reflex linter: No issues found!")
        return 0


if __name__ == '__main__':
    sys.exit(main())

