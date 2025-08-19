#!/usr/bin/env python3
"""
Academic writing style checker for papers
Checks for inappropriate expressions and suggests improvements
"""

import re
import sys
from typing import List, Tuple, Dict

class AcademicStyleChecker:
    def __init__(self, max_sentence_words=40, max_and_count=3):
        # Configurable thresholds
        self.max_sentence_words = max_sentence_words
        self.max_and_count = max_and_count
        
        # Compile regex patterns once for better performance
        self._comment_pattern = re.compile(r'%.*$', re.MULTILINE)
        self._latex_cmd_pattern = re.compile(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})*')
        self._math_inline_pattern = re.compile(r'\$.*?\$')
        self._math_equation_pattern = re.compile(r'\\begin\{equation\}.*?\\end\{equation\}', re.DOTALL)
        self._figure_pattern = re.compile(r'\\begin\{figure\}.*?\\end\{figure\}', re.DOTALL)
        self._table_pattern = re.compile(r'\\begin\{table\}.*?\\end\{table\}', re.DOTALL)
        self._whitespace_pattern = re.compile(r'\s+')
        self._word_pattern = re.compile(r'\b\w+\b')
        self._starts_with_this_pattern = re.compile(r'^\s*(This|These)\s+(is|are|can|will|should|may)')
        # Informal expressions to avoid in academic writing
        self.informal_expressions = {
            "a lot of": "many, numerous, considerable",
            "lots of": "many, numerous, considerable", 
            "tons of": "numerous, substantial amounts of",
            "kind of": "somewhat, rather",
            "sort of": "somewhat, rather",
            "pretty much": "essentially, largely",
            "really": "significantly, considerably",
            "very": "highly, significantly",
            "quite": "rather, considerably",
            "totally": "completely, entirely",
            "absolutely": "completely, entirely",
            "basically": "fundamentally, essentially",
            "obviously": "clearly, evidently",
            "clearly": "as demonstrated, as shown",
            "of course": "naturally, as expected",
            "needless to say": "notably, importantly",
            "it's": "it is",
            "can't": "cannot",
            "don't": "do not",
            "won't": "will not",
            "isn't": "is not",
            "aren't": "are not",
            "doesn't": "does not",
            "haven't": "have not",
            "hasn't": "has not",
            "wasn't": "was not",
            "weren't": "were not",
            "wouldn't": "would not",
            "shouldn't": "should not",
            "couldn't": "could not"
        }
        
        # Wordy expressions that can be simplified
        self.wordy_expressions = {
            "in order to": "to",
            "due to the fact that": "because",
            "in the event that": "if", 
            "at this point in time": "now, currently",
            "in the near future": "soon",
            "a large number of": "many",
            "a great deal of": "much",
            "in spite of the fact that": "although",
            "for the purpose of": "for, to",
            "with regard to": "regarding, concerning",
            "in relation to": "regarding, concerning",
            "with respect to": "regarding, concerning",
            "in connection with": "regarding, concerning",
            "it is important to note that": "notably",
            "it should be mentioned that": "notably",
            "it is worth noting that": "notably",
            "take into consideration": "consider",
            "give consideration to": "consider",
            "make use of": "use",
            "carry out": "conduct, perform",
            "bring about": "cause",
            "point out": "note, indicate"
        }
        
        # Weak or vague expressions
        self.weak_expressions = {
            "seems to": "appears to, suggests",
            "appears to": "indicates, suggests, demonstrates",
            "might be": "may be, could be",
            "could be": "may be, potentially",
            "maybe": "perhaps, possibly",
            "probably": "likely, presumably",
            "somewhat": "moderately, to some extent",
            "rather": "moderately, considerably",
            "fairly": "moderately, reasonably",
            "quite": "considerably, substantially"
        }
        
        # First/second person pronouns to avoid
        self.personal_pronouns = [
            "I", "we", "you", "your", "our", "us", "my", "mine", "ours"
        ]
        
        # Passive voice indicators (to suggest active voice)
        self.passive_indicators = [
            "is/are + past participle",
            "was/were + past participle",
            "has/have been + past participle",
            "had been + past participle",
            "will be + past participle"
        ]
        
    def clean_latex_text(self, text: str) -> str:
        """Remove LaTeX commands and extract readable text"""
        # Remove comments
        text = self._comment_pattern.sub('', text)
        
        # Remove common LaTeX commands
        text = self._latex_cmd_pattern.sub(' ', text)
        
        # Remove math environments
        text = self._math_inline_pattern.sub(' ', text)
        text = self._math_equation_pattern.sub(' ', text)
        
        # Remove figures and tables
        text = self._figure_pattern.sub(' ', text)
        text = self._table_pattern.sub(' ', text)
        
        # Clean up whitespace
        text = self._whitespace_pattern.sub(' ', text)
        
        return text.strip()
    
    def check_informal_expressions(self, filepath: str) -> List[Tuple[int, str, str, str]]:
        """Check for informal expressions"""
        issues = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%') or line.strip().startswith('\\'):
                continue
            
            clean_line = self.clean_latex_text(line).lower()
            
            for informal, formal in self.informal_expressions.items():
                if informal in clean_line:
                    issues.append((
                        line_num,
                        "Style Warning",
                        f"Informal expression '{informal}' → Consider: {formal}",
                        line.strip()
                    ))
        
        return issues
    
    def check_wordy_expressions(self, filepath: str) -> List[Tuple[int, str, str, str]]:
        """Check for wordy expressions that can be simplified"""
        issues = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%') or line.strip().startswith('\\'):
                continue
            
            clean_line = self.clean_latex_text(line).lower()
            
            for wordy, concise in self.wordy_expressions.items():
                if wordy in clean_line:
                    issues.append((
                        line_num,
                        "Conciseness",
                        f"Wordy expression '{wordy}' → Consider: {concise}",
                        line.strip()
                    ))
        
        return issues
    
    def check_weak_expressions(self, filepath: str) -> List[Tuple[int, str, str, str]]:
        """Check for weak or vague expressions"""
        issues = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%') or line.strip().startswith('\\'):
                continue
            
            clean_line = self.clean_latex_text(line).lower()
            
            for weak, stronger in self.weak_expressions.items():
                if weak in clean_line:
                    issues.append((
                        line_num,
                        "Precision",
                        f"Vague expression '{weak}' → Consider: {stronger}",
                        line.strip()
                    ))
        
        return issues
    
    def check_personal_pronouns(self, filepath: str) -> List[Tuple[int, str, str, str]]:
        """Check for personal pronouns (should be avoided in academic writing)"""
        issues = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%') or line.strip().startswith('\\'):
                continue
            
            clean_line = self.clean_latex_text(line)
            words = self._word_pattern.findall(clean_line)
            
            for word in words:
                if word in self.personal_pronouns:
                    issues.append((
                        line_num,
                        "Academic Style",
                        f"Personal pronoun '{word}' - Consider using passive voice or 'the authors'",
                        line.strip()
                    ))
        
        return issues
    
    def check_sentence_structure(self, filepath: str) -> List[Tuple[int, str, str, str]]:
        """Check for sentence structure issues"""
        issues = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%') or line.strip().startswith('\\'):
                continue
            
            clean_line = self.clean_latex_text(line)
            
            # Check for very long sentences
            words = self._word_pattern.findall(clean_line)
            if len(words) > self.max_sentence_words:
                issues.append((
                    line_num,
                    "Readability",
                    f"Very long sentence ({len(words)} words) - Consider breaking into shorter sentences",
                    line.strip()
                ))
            
            # Check for sentences starting with "This" or "These" without clear antecedent
            if self._starts_with_this_pattern.match(clean_line):
                issues.append((
                    line_num,
                    "Clarity",
                    "Sentence starts with 'This/These' - Consider being more specific",
                    line.strip()
                ))
            
            # Check for excessive use of "and"
            and_count = clean_line.lower().count(' and ')
            if and_count > self.max_and_count:
                issues.append((
                    line_num,
                    "Style",
                    f"Multiple 'and' connectors ({and_count}) - Consider using varied connectors",
                    line.strip()
                ))
        
        return issues
    
    def check_technical_language(self, filepath: str) -> List[Tuple[int, str, str, str]]:
        """Check for appropriate technical language usage"""
        issues = []
        
        # Terms that should be defined on first use
        technical_terms = [
            "CR3BP", "GMOS", "manifold", "heteroclinic", "quasi-periodic"
        ]
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        defined_terms = set()
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%') or line.strip().startswith('\\'):
                continue
            
            clean_line = self.clean_latex_text(line)
            
            # Check if technical terms are properly introduced
            for term in technical_terms:
                if term in clean_line and term not in defined_terms:
                    # Check if it's defined in this line or nearby
                    if '(' in clean_line and ')' in clean_line:
                        defined_terms.add(term)
                    else:
                        issues.append((
                            line_num,
                            "Technical Language",
                            f"Technical term '{term}' may need definition on first use",
                            line.strip()
                        ))
        
        return issues
    
    def check_informal_expressions_content(self, content: str) -> List[Tuple[int, str, str, str]]:
        """Check for informal expressions in content"""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%') or line.strip().startswith('\\'):
                continue
            
            clean_line = self.clean_latex_text(line).lower()
            
            for informal, formal in self.informal_expressions.items():
                if informal in clean_line:
                    issues.append((
                        line_num,
                        "Style Warning",
                        f"Informal expression '{informal}' → Consider: {formal}",
                        line.strip()
                    ))
        
        return issues
    
    def check_wordy_expressions_content(self, content: str) -> List[Tuple[int, str, str, str]]:
        """Check for wordy expressions that can be simplified in content"""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%') or line.strip().startswith('\\'):
                continue
            
            clean_line = self.clean_latex_text(line).lower()
            
            for wordy, concise in self.wordy_expressions.items():
                if wordy in clean_line:
                    issues.append((
                        line_num,
                        "Conciseness",
                        f"Wordy expression '{wordy}' → Consider: {concise}",
                        line.strip()
                    ))
        
        return issues
    
    def check_weak_expressions_content(self, content: str) -> List[Tuple[int, str, str, str]]:
        """Check for weak or vague expressions in content"""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%') or line.strip().startswith('\\'):
                continue
            
            clean_line = self.clean_latex_text(line).lower()
            
            for weak, stronger in self.weak_expressions.items():
                if weak in clean_line:
                    issues.append((
                        line_num,
                        "Precision",
                        f"Vague expression '{weak}' → Consider: {stronger}",
                        line.strip()
                    ))
        
        return issues
    
    def check_personal_pronouns_content(self, content: str) -> List[Tuple[int, str, str, str]]:
        """Check for personal pronouns in content"""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%') or line.strip().startswith('\\'):
                continue
            
            clean_line = self.clean_latex_text(line)
            words = self._word_pattern.findall(clean_line)
            
            for word in words:
                if word in self.personal_pronouns:
                    issues.append((
                        line_num,
                        "Academic Style",
                        f"Personal pronoun '{word}' - Consider using passive voice or 'the authors'",
                        line.strip()
                    ))
        
        return issues
    
    def check_sentence_structure_content(self, content: str) -> List[Tuple[int, str, str, str]]:
        """Check for sentence structure issues in content"""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%') or line.strip().startswith('\\'):
                continue
            
            clean_line = self.clean_latex_text(line)
            
            # Check for very long sentences
            words = self._word_pattern.findall(clean_line)
            if len(words) > self.max_sentence_words:
                issues.append((
                    line_num,
                    "Readability",
                    f"Very long sentence ({len(words)} words) - Consider breaking into shorter sentences",
                    line.strip()
                ))
            
            # Check for sentences starting with "This" or "These" without clear antecedent
            if self._starts_with_this_pattern.match(clean_line):
                issues.append((
                    line_num,
                    "Clarity",
                    "Sentence starts with 'This/These' - Consider being more specific",
                    line.strip()
                ))
            
            # Check for excessive use of "and"
            and_count = clean_line.lower().count(' and ')
            if and_count > self.max_and_count:
                issues.append((
                    line_num,
                    "Style",
                    f"Multiple 'and' connectors ({and_count}) - Consider using varied connectors",
                    line.strip()
                ))
        
        return issues
    
    def check_technical_language_content(self, content: str) -> List[Tuple[int, str, str, str]]:
        """Check for appropriate technical language usage in content"""
        issues = []
        
        # Terms that should be defined on first use
        technical_terms = [
            "CR3BP", "GMOS", "manifold", "heteroclinic", "quasi-periodic"
        ]
        
        lines = content.split('\n')
        defined_terms = set()
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%') or line.strip().startswith('\\'):
                continue
            
            clean_line = self.clean_latex_text(line)
            
            # Check if technical terms are properly introduced
            for term in technical_terms:
                if term in clean_line and term not in defined_terms:
                    # Check if it's defined in this line or nearby
                    if '(' in clean_line and ')' in clean_line:
                        defined_terms.add(term)
                    else:
                        issues.append((
                            line_num,
                            "Technical Language",
                            f"Technical term '{term}' may need definition on first use",
                            line.strip()
                        ))
        
        return issues

def main():
    if len(sys.argv) != 2:
        print("Usage: python academic_style_checker.py <tex_file>")
        sys.exit(1)
    
    checker = AcademicStyleChecker()
    filepath = sys.argv[1]
    
    print(f"Checking academic writing style in {filepath}...")
    
    # Run all style checks
    informal_issues = checker.check_informal_expressions(filepath)
    wordy_issues = checker.check_wordy_expressions(filepath)
    weak_issues = checker.check_weak_expressions(filepath)
    pronoun_issues = checker.check_personal_pronouns(filepath)
    structure_issues = checker.check_sentence_structure(filepath)
    technical_issues = checker.check_technical_language(filepath)
    
    all_issues = informal_issues + wordy_issues + weak_issues + pronoun_issues + structure_issues + technical_issues
    
    if all_issues:
        print(f"\nFound {len(all_issues)} style suggestions:")
        for line_num, issue_type, description, context in all_issues:
            print(f"Line {line_num}: {issue_type} - {description}")
            print(f"  Context: {context}")
            print()
    else:
        print("No style issues found!")
    
    return len(all_issues)

if __name__ == "__main__":
    sys.exit(main())