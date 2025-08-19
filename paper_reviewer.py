#!/usr/bin/env python3
"""
Comprehensive paper review system for LaTeX academic papers
Combines spell checking, LaTeX validation, and academic style checking
"""

import sys
import os
from typing import List, Tuple, Dict
from spell_checker import LaTeXSpellChecker
from latex_validator import LaTeXValidator
from academic_style_checker import AcademicStyleChecker

class PaperReviewer:
    def __init__(self):
        self.spell_checker = LaTeXSpellChecker()
        self.latex_validator = LaTeXValidator()
        self.style_checker = AcademicStyleChecker()
        
    def review_paper(self, filepath: str) -> Dict[str, List[Tuple[int, str, str, str]]]:
        """Comprehensive review of the paper"""
        results = {}
        
        print(f"🔍 Reviewing paper: {filepath}")
        print("=" * 60)
        
        # 1. Spell checking
        print("📝 Checking spelling and typos...")
        spelling_issues = self.spell_checker.check_spelling(filepath)
        duplicate_issues = self.spell_checker.check_duplicated_words(filepath)
        results['spelling'] = spelling_issues + duplicate_issues
        
        # 2. LaTeX validation
        print("🔧 Validating LaTeX syntax...")
        bracket_issues = self.latex_validator.check_bracket_matching(filepath)
        env_issues = self.latex_validator.check_environment_matching(filepath)
        common_issues = self.latex_validator.check_common_latex_errors(filepath)
        figure_issues = self.latex_validator.check_figure_references(filepath)
        math_issues = self.latex_validator.check_math_environments(filepath)
        results['latex'] = bracket_issues + env_issues + common_issues + figure_issues + math_issues
        
        # 3. Academic style checking
        print("✍️  Checking academic writing style...")
        informal_issues = self.style_checker.check_informal_expressions(filepath)
        wordy_issues = self.style_checker.check_wordy_expressions(filepath)
        weak_issues = self.style_checker.check_weak_expressions(filepath)
        pronoun_issues = self.style_checker.check_personal_pronouns(filepath)
        structure_issues = self.style_checker.check_sentence_structure(filepath)
        technical_issues = self.style_checker.check_technical_language(filepath)
        results['style'] = informal_issues + wordy_issues + weak_issues + pronoun_issues + structure_issues + technical_issues
        
        return results
    
    def generate_report(self, results: Dict[str, List], filepath: str) -> str:
        """Generate a comprehensive report"""
        report = []
        report.append(f"📋 PAPER REVIEW REPORT")
        report.append(f"File: {filepath}")
        report.append("=" * 80)
        
        total_issues = sum(len(issues) for issues in results.values())
        
        if total_issues == 0:
            report.append("✅ Excellent! No issues found in your paper.")
            report.append("")
            report.append("Your paper appears to be well-written with:")
            report.append("• No spelling or typographical errors")
            report.append("• Proper LaTeX syntax and formatting")
            report.append("• Appropriate academic writing style")
            return "\n".join(report)
        
        # Summary
        report.append("📊 SUMMARY")
        report.append("-" * 40)
        report.append(f"Total issues found: {total_issues}")
        report.append(f"• Spelling/Typos: {len(results['spelling'])}")
        report.append(f"• LaTeX Syntax: {len(results['latex'])}")
        report.append(f"• Style Suggestions: {len(results['style'])}")
        report.append("")
        
        # Detailed findings
        if results['spelling']:
            report.append("📝 SPELLING AND TYPOS")
            report.append("-" * 40)
            for line_num, issue_type, description, context in sorted(results['spelling']):
                report.append(f"Line {line_num}: {description}")
                report.append(f"  → {context}")
                report.append("")
        
        if results['latex']:
            report.append("🔧 LATEX SYNTAX ISSUES")
            report.append("-" * 40)
            for line_num, issue_type, description, context in sorted(results['latex']):
                report.append(f"Line {line_num}: {description}")
                report.append(f"  → {context}")
                report.append("")
        
        if results['style']:
            report.append("✍️  ACADEMIC STYLE SUGGESTIONS")
            report.append("-" * 40)
            for line_num, issue_type, description, context in sorted(results['style']):
                report.append(f"Line {line_num}: {description}")
                report.append(f"  → {context}")
                report.append("")
        
        # Recommendations
        report.append("💡 RECOMMENDATIONS")
        report.append("-" * 40)
        
        if results['spelling']:
            report.append("• Review and correct spelling errors before submission")
        
        if results['latex']:
            report.append("• Fix LaTeX syntax issues to ensure proper compilation")
            report.append("• Test compilation with your LaTeX editor")
        
        if results['style']:
            report.append("• Consider style suggestions to improve academic tone")
            report.append("• Review sentence structure and clarity")
        
        report.append("")
        report.append("🎯 PRIORITY ACTIONS:")
        
        # Categorize by priority
        high_priority = [issue for issues in [results['spelling'], results['latex']] for issue in issues 
                        if any(keyword in issue[1].lower() for keyword in ['error', 'bracket', 'environment'])]
        
        medium_priority = [issue for issues in [results['latex'], results['style']] for issue in issues 
                          if any(keyword in issue[1].lower() for keyword in ['warning', 'formatting'])]
        
        if high_priority:
            report.append("1. HIGH: Fix critical LaTeX and spelling errors")
        if medium_priority:
            report.append("2. MEDIUM: Address formatting and style suggestions")
        if results['style']:
            report.append("3. LOW: Review academic writing style improvements")
        
        return "\n".join(report)
    
    def save_report(self, report: str, filepath: str):
        """Save report to file"""
        base_name = os.path.splitext(filepath)[0]
        report_file = f"{base_name}_review_report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 Report saved to: {report_file}")
        return report_file

def main():
    if len(sys.argv) != 2:
        print("Usage: python paper_reviewer.py <tex_file>")
        print()
        print("This tool provides comprehensive review of LaTeX academic papers:")
        print("• Spell checking and typo detection")
        print("• LaTeX syntax validation")
        print("• Academic writing style analysis")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    
    if not filepath.endswith('.tex'):
        print(f"Warning: '{filepath}' does not appear to be a LaTeX file.")
    
    # Initialize reviewer
    reviewer = PaperReviewer()
    
    # Perform comprehensive review
    results = reviewer.review_paper(filepath)
    
    # Generate and display report
    report = reviewer.generate_report(results, filepath)
    print("\n" + report)
    
    # Save report to file
    report_file = reviewer.save_report(report, filepath)
    
    # Return exit code based on critical issues
    critical_issues = len(results['spelling']) + len([issue for issue in results['latex'] 
                                                   if 'error' in issue[1].lower()])
    
    if critical_issues > 0:
        print(f"\n⚠️  Found {critical_issues} critical issues that should be addressed.")
        return 1
    else:
        print(f"\n✅ No critical issues found!")
        return 0

if __name__ == "__main__":
    sys.exit(main())