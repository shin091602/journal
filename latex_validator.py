#!/usr/bin/env python3
"""
LaTeX syntax validator for academic papers
Checks for common LaTeX formatting and syntax errors
"""

import re
import sys
from typing import List, Tuple, Dict

class LaTeXValidator:
    def __init__(self):
        # Compile regex patterns once for better performance
        self._begin_pattern = re.compile(r'\\begin\{([^}]+)\}')
        self._end_pattern = re.compile(r'\\end\{([^}]+)\}')
        self._missing_space_pattern = re.compile(r'\w\.\w')
        self._double_space_pattern = re.compile(r'  ')
        self._cite_space_pattern = re.compile(r'\w\s+\\cite')
        self._ref_space_pattern = re.compile(r'\w\s+\\ref')
        self._linebreak_pattern = re.compile(r'\\\\')
        self._environment_check_pattern = re.compile(r'\\begin\{(tabular|array|aligned)\}')
        self._label_pattern = re.compile(r'\\label\{([^}]+)\}')
        self._ref_pattern = re.compile(r'\\ref\{([^}]+)\}')
        self._math_content_pattern = re.compile(r'\$([^$]+)\$')
        
        self.bracket_pairs = {
            '{': '}',
            '[': ']',
            '(': ')'
        }
        
        self.math_environments = [
            ('equation', 'equation'),
            ('align', 'align'),
            ('aligned', 'aligned'),
            ('array', 'array'),
            ('matrix', 'matrix'),
            ('bmatrix', 'bmatrix'),
            ('pmatrix', 'pmatrix')
        ]
        
        self.float_environments = [
            ('figure', 'figure'),
            ('table', 'table'),
            ('subfigure', 'subfigure')
        ]
        
    def check_bracket_matching(self, filepath: str) -> List[Tuple[int, str, str, str]]:
        """Check for mismatched brackets and braces"""
        issues = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        stack = []
        
        for line_num, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('%'):
                continue
            
            for i, char in enumerate(line):
                if char in self.bracket_pairs:
                    stack.append((char, line_num, i))
                elif char in self.bracket_pairs.values():
                    if not stack:
                        issues.append((
                            line_num,
                            "Bracket Error",
                            f"Unmatched closing bracket '{char}'",
                            line.strip()
                        ))
                    else:
                        last_open, last_line, last_pos = stack.pop()
                        expected_close = self.bracket_pairs[last_open]
                        if char != expected_close:
                            issues.append((
                                line_num,
                                "Bracket Error",
                                f"Expected '{expected_close}' but found '{char}'",
                                line.strip()
                            ))
        
        # Check for unclosed brackets
        for open_bracket, line_num, pos in stack:
            issues.append((
                line_num,
                "Bracket Error",
                f"Unclosed bracket '{open_bracket}'",
                lines[line_num-1].strip()
            ))
        
        return issues
    
    def check_environment_matching(self, filepath: str) -> List[Tuple[int, str, str, str]]:
        """Check for mismatched begin/end environments"""
        issues = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Use compiled patterns
        
        env_stack = []
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%'):
                continue
            
            # Find begin environments
            for match in self._begin_pattern.finditer(line):
                env_name = match.group(1)
                env_stack.append((env_name, line_num))
            
            # Find end environments
            for match in self._end_pattern.finditer(line):
                env_name = match.group(1)
                
                if not env_stack:
                    issues.append((
                        line_num,
                        "Environment Error",
                        f"Unmatched \\end{{{env_name}}}",
                        line.strip()
                    ))
                else:
                    last_env, last_line = env_stack.pop()
                    if env_name != last_env:
                        issues.append((
                            line_num,
                            "Environment Error",
                            f"Expected \\end{{{last_env}}} but found \\end{{{env_name}}}",
                            line.strip()
                        ))
        
        # Check for unclosed environments
        for env_name, line_num in env_stack:
            issues.append((
                line_num,
                "Environment Error",
                f"Unclosed environment '{env_name}'",
                lines[line_num-1].strip()
            ))
        
        return issues
    
    def check_common_latex_errors(self, filepath: str) -> List[Tuple[int, str, str, str]]:
        """Check for common LaTeX syntax errors"""
        issues = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%'):
                continue
            
            # Check for missing spaces after periods
            if self._missing_space_pattern.search(line):
                issues.append((
                    line_num,
                    "Formatting Warning",
                    "Missing space after period (may cause incorrect spacing)",
                    line.strip()
                ))
            
            # Check for double spaces
            if '  ' in line and not line.strip().startswith('\\'):
                issues.append((
                    line_num,
                    "Formatting Warning",
                    "Multiple consecutive spaces found",
                    line.strip()
                ))
            
            # Check for missing ~ before citations
            if self._cite_space_pattern.search(line):
                issues.append((
                    line_num,
                    "Formatting Warning",
                    "Consider using non-breaking space (~) before \\cite",
                    line.strip()
                ))
            
            # Check for missing ~ before references
            if self._ref_space_pattern.search(line):
                issues.append((
                    line_num,
                    "Formatting Warning",
                    "Consider using non-breaking space (~) before \\ref",
                    line.strip()
                ))
            
            # Check for \\ outside of tables/arrays
            if self._linebreak_pattern.search(line) and not any(env in line for env in ['tabular', 'array', 'aligned']):
                if not self._environment_check_pattern.search(line):
                    issues.append((
                        line_num,
                        "Formatting Warning",
                        "Line break (\\\\) found outside table/math environment",
                        line.strip()
                    ))
        
        return issues
    
    def check_figure_references(self, filepath: str) -> List[Tuple[int, str, str, str]]:
        """Check that all figures have labels and are referenced"""
        issues = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Find all figure environments and their labels
        figure_labels = set()
        figures_without_labels = []
        
        in_figure = False
        current_figure_line = 0
        current_figure_has_label = False
        
        for line_num, line in enumerate(lines, 1):
            if '\\begin{figure}' in line:
                in_figure = True
                current_figure_line = line_num
                current_figure_has_label = False
            elif '\\end{figure}' in line and in_figure:
                in_figure = False
                if not current_figure_has_label:
                    figures_without_labels.append(current_figure_line)
            elif in_figure and '\\label{' in line:
                current_figure_has_label = True
                label_match = self._label_pattern.search(line)
                if label_match:
                    figure_labels.add(label_match.group(1))
        
        # Report figures without labels
        for fig_line in figures_without_labels:
            issues.append((
                fig_line,
                "Reference Warning",
                "Figure environment without \\label{}",
                lines[fig_line-1].strip()
            ))
        
        # Find all references and check if they exist
        for line_num, line in enumerate(lines, 1):
            for match in self._ref_pattern.finditer(line):
                ref_label = match.group(1)
                if ref_label not in figure_labels and 'fig' in ref_label.lower():
                    issues.append((
                        line_num,
                        "Reference Warning",
                        f"Reference to undefined figure label '{ref_label}'",
                        line.strip()
                    ))
        
        return issues
    
    def check_math_environments(self, filepath: str) -> List[Tuple[int, str, str, str]]:
        """Check for issues in math environments"""
        issues = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%'):
                continue
            
            # Check for text in math mode without \text{}
            if '$' in line:
                math_content = self._math_content_pattern.findall(line)
                for content in math_content:
                    # Check for common words that should be in \text{}
                    text_words = ['and', 'or', 'where', 'for', 'if', 'when', 'the', 'a', 'an']
                    for word in text_words:
                        if f' {word} ' in content.lower():
                            issues.append((
                                line_num,
                                "Math Warning",
                                f"Text word '{word}' in math mode should use \\text{{{word}}}",
                                line.strip()
                            ))

        return issues
    
    def check_bracket_matching_content(self, content: str) -> List[Tuple[int, str, str, str]]:
        """Check for mismatched brackets and braces in content"""
        issues = []
        lines = content.split('\n')
        stack = []
        
        for line_num, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('%'):
                continue
            
            for i, char in enumerate(line):
                if char in self.bracket_pairs:
                    stack.append((char, line_num, i))
                elif char in self.bracket_pairs.values():
                    if not stack:
                        issues.append((
                            line_num,
                            "Bracket Error",
                            f"Unmatched closing bracket '{char}'",
                            line.strip()
                        ))
                    else:
                        last_open, last_line, last_pos = stack.pop()
                        expected_close = self.bracket_pairs[last_open]
                        if char != expected_close:
                            issues.append((
                                line_num,
                                "Bracket Error",
                                f"Expected '{expected_close}' but found '{char}'",
                                line.strip()
                            ))
        
        # Check for unclosed brackets
        for open_bracket, line_num, pos in stack:
            issues.append((
                line_num,
                "Bracket Error",
                f"Unclosed bracket '{open_bracket}'",
                lines[line_num-1].strip()
            ))
        
        return issues
    
    def check_environment_matching_content(self, content: str) -> List[Tuple[int, str, str, str]]:
        """Check for mismatched begin/end environments in content"""
        issues = []
        lines = content.split('\n')
        env_stack = []
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%'):
                continue
            
            # Find begin environments
            for match in self._begin_pattern.finditer(line):
                env_name = match.group(1)
                env_stack.append((env_name, line_num))
            
            # Find end environments
            for match in self._end_pattern.finditer(line):
                env_name = match.group(1)
                
                if not env_stack:
                    issues.append((
                        line_num,
                        "Environment Error",
                        f"Unmatched \\end{{{env_name}}}",
                        line.strip()
                    ))
                else:
                    last_env, last_line = env_stack.pop()
                    if env_name != last_env:
                        issues.append((
                            line_num,
                            "Environment Error",
                            f"Expected \\end{{{last_env}}} but found \\end{{{env_name}}}",
                            line.strip()
                        ))
        
        # Check for unclosed environments
        for env_name, line_num in env_stack:
            issues.append((
                line_num,
                "Environment Error",
                f"Unclosed environment '{env_name}'",
                lines[line_num-1].strip()
            ))
        
        return issues
    
    def check_common_latex_errors_content(self, content: str) -> List[Tuple[int, str, str, str]]:
        """Check for common LaTeX syntax errors in content"""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%'):
                continue
            
            # Check for missing spaces after periods
            if self._missing_space_pattern.search(line):
                issues.append((
                    line_num,
                    "Formatting Warning",
                    "Missing space after period (may cause incorrect spacing)",
                    line.strip()
                ))
            
            # Check for double spaces
            if self._double_space_pattern.search(line) and not line.strip().startswith('\\'):
                issues.append((
                    line_num,
                    "Formatting Warning",
                    "Multiple consecutive spaces found",
                    line.strip()
                ))
            
            # Check for missing ~ before citations
            if self._cite_space_pattern.search(line):
                issues.append((
                    line_num,
                    "Formatting Warning",
                    "Consider using non-breaking space (~) before \\cite",
                    line.strip()
                ))
            
            # Check for missing ~ before references
            if self._ref_space_pattern.search(line):
                issues.append((
                    line_num,
                    "Formatting Warning",
                    "Consider using non-breaking space (~) before \\ref",
                    line.strip()
                ))
            
            # Check for \\\\ outside of tables/arrays
            if self._linebreak_pattern.search(line) and not any(env in line for env in ['tabular', 'array', 'aligned']):
                if not self._environment_check_pattern.search(line):
                    issues.append((
                        line_num,
                        "Formatting Warning",
                        "Line break (\\\\) found outside table/math environment",
                        line.strip()
                    ))
        
        return issues
    
    def check_figure_references_content(self, content: str) -> List[Tuple[int, str, str, str]]:
        """Check that all figures have labels and are referenced in content"""
        issues = []
        lines = content.split('\n')
        
        # Find all figure environments and their labels
        figure_labels = set()
        figures_without_labels = []
        
        in_figure = False
        current_figure_line = 0
        current_figure_has_label = False
        
        for line_num, line in enumerate(lines, 1):
            if '\\begin{figure}' in line:
                in_figure = True
                current_figure_line = line_num
                current_figure_has_label = False
            elif '\\end{figure}' in line and in_figure:
                in_figure = False
                if not current_figure_has_label:
                    figures_without_labels.append(current_figure_line)
            elif in_figure and '\\label{' in line:
                current_figure_has_label = True
                label_match = self._label_pattern.search(line)
                if label_match:
                    figure_labels.add(label_match.group(1))
        
        # Report figures without labels
        for fig_line in figures_without_labels:
            issues.append((
                fig_line,
                "Reference Warning",
                "Figure environment without \\label{}",
                lines[fig_line-1].strip()
            ))
        
        # Find all references and check if they exist
        for line_num, line in enumerate(lines, 1):
            for match in self._ref_pattern.finditer(line):
                ref_label = match.group(1)
                if ref_label not in figure_labels and 'fig' in ref_label.lower():
                    issues.append((
                        line_num,
                        "Reference Warning",
                        f"Reference to undefined figure label '{ref_label}'",
                        line.strip()
                    ))
        
        return issues
    
    def check_math_environments_content(self, content: str) -> List[Tuple[int, str, str, str]]:
        """Check for issues in math environments in content"""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%'):
                continue
            
            # Check for text in math mode without \\text{}
            if '$' in line:
                math_contents = self._math_content_pattern.findall(line)
                for content_match in math_contents:
                    # Check for common words that should be in \\text{}
                    text_words = ['and', 'or', 'where', 'for', 'if', 'when', 'the', 'a', 'an']
                    for word in text_words:
                        if f' {word} ' in content_match.lower():
                            issues.append((
                                line_num,
                                "Math Warning",
                                f"Text word '{word}' in math mode should use \\text{{{word}}}",
                                line.strip()
                            ))

        return issues

def main():
    if len(sys.argv) != 2:
        print("Usage: python latex_validator.py <tex_file>")
        sys.exit(1)
    
    validator = LaTeXValidator()
    filepath = sys.argv[1]
    
    print(f"Validating LaTeX syntax in {filepath}...")
    
    # Run all validation checks
    bracket_issues = validator.check_bracket_matching(filepath)
    env_issues = validator.check_environment_matching(filepath)
    common_issues = validator.check_common_latex_errors(filepath)
    figure_issues = validator.check_figure_references(filepath)
    math_issues = validator.check_math_environments(filepath)
    
    all_issues = bracket_issues + env_issues + common_issues + figure_issues + math_issues
    
    if all_issues:
        print(f"\nFound {len(all_issues)} LaTeX issues:")
        for line_num, issue_type, description, context in all_issues:
            print(f"Line {line_num}: {issue_type} - {description}")
            print(f"  Context: {context}")
            print()
    else:
        print("No LaTeX syntax issues found!")
    
    return len(all_issues)

if __name__ == "__main__":
    sys.exit(main())