#!/usr/bin/env python3
"""
Spell checker for LaTeX files
Checks for common misspellings and typos in academic papers
"""

import re
import sys
from typing import List, Tuple, Dict

class LaTeXSpellChecker:
    def __init__(self):
        # Compile regex patterns once for better performance
        self._comment_pattern = re.compile(r'%.*$', re.MULTILINE)
        self._latex_cmd_pattern = re.compile(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})*')
        self._math_inline_pattern = re.compile(r'\$.*?\$')
        self._math_equation_pattern = re.compile(r'\\begin\{equation\}.*?\\end\{equation\}', re.DOTALL)
        self._math_aligned_pattern = re.compile(r'\\begin\{aligned\}.*?\\end\{aligned\}', re.DOTALL)
        self._figure_pattern = re.compile(r'\\begin\{figure\}.*?\\end\{figure\}', re.DOTALL)
        self._table_pattern = re.compile(r'\\begin\{table\}.*?\\end\{table\}', re.DOTALL)
        self._cite_pattern = re.compile(r'\\cite\{[^}]*\}')
        self._ref_pattern = re.compile(r'\\ref\{[^}]*\}')
        self._label_pattern = re.compile(r'\\label\{[^}]*\}')
        self._whitespace_pattern = re.compile(r'\s+')
        self._word_pattern = re.compile(r'\b[a-zA-Z]+\b')
        
        # Common academic misspellings
        self.common_misspellings = {
            "occurances": "occurrences",
            "occured": "occurred", 
            "occuring": "occurring",
            "seperate": "separate",
            "seperately": "separately",
            "recieve": "receive",
            "recieved": "received",
            "recieving": "receiving",
            "beleive": "believe",
            "beleived": "believed",
            "acheive": "achieve",
            "acheived": "achieved",
            "succesful": "successful",
            "succesfully": "successfully",
            "neccessary": "necessary",
            "accomodate": "accommodate",
            "aproximate": "approximate",
            "aproximately": "approximately",
            "aproximation": "approximation",
            "analize": "analyze",
            "analized": "analyzed",
            "analysing": "analyzing",
            "optimise": "optimize",
            "optimised": "optimized",
            "optimisation": "optimization",
            "realise": "realize",
            "realised": "realized",
            "realisation": "realization",
            "recognise": "recognize",
            "recognised": "recognized",
            "characterise": "characterize",
            "characterised": "characterized",
            "generalise": "generalize",
            "generalised": "generalized",
            "stabilise": "stabilize",
            "stabilised": "stabilized",
            "centre": "center",
            "centres": "centers",
            "colour": "color",
            "colours": "colors",
            "favour": "favor",
            "favoured": "favored",
            "behaviour": "behavior",
            "behaviours": "behaviors",
            "modelling": "modeling",
            "modelled": "modeled",
            "travelling": "traveling",
            "travelled": "traveled",
            "initialise": "initialize",
            "initialised": "initialized",
            "initialisation": "initialization",
            "minimise": "minimize",
            "minimised": "minimized",
            "minimisation": "minimization",
            "maximise": "maximize",
            "maximised": "maximized",
            "maximisation": "maximization",
            "visualise": "visualize",
            "visualised": "visualized",
            "visualisation": "visualization",
            "utilise": "utilize",
            "utilised": "utilized",
            "utilisation": "utilization",
            "parameterise": "parameterize",
            "parameterised": "parameterized",
            "parameterisation": "parameterization"
        }
        
        # Context-specific technical terms (known correct spellings)
        self.technical_terms = {
            "heteroclinic", "manifolds", "manifold", "torus", "tori", "quasi-periodic",
            "Lyapunov", "Lagrange", "Poincaré", "CR3BP", "monodromy", "eigenvalue",
            "eigenvector", "astrodynamics", "spacecraft", "celestial", "primaries",
            "Jacobi", "pseudo-potential", "dimensionality", "equilibrium", "halo",
            "incommensurate", "interpolation", "nonlinear", "topological", "thrustless"
        }
        
    def clean_latex_text(self, text: str) -> str:
        """Remove LaTeX commands and extract readable text"""
        # Remove comments
        text = self._comment_pattern.sub('', text)
        
        # Remove common LaTeX commands
        text = self._latex_cmd_pattern.sub(' ', text)
        
        # Remove math environments
        text = self._math_inline_pattern.sub(' ', text)
        text = self._math_equation_pattern.sub(' ', text)
        text = self._math_aligned_pattern.sub(' ', text)
        
        # Remove figures and tables
        text = self._figure_pattern.sub(' ', text)
        text = self._table_pattern.sub(' ', text)
        
        # Remove bibliography
        text = self._cite_pattern.sub(' ', text)
        text = self._ref_pattern.sub(' ', text)
        text = self._label_pattern.sub(' ', text)
        
        # Clean up whitespace
        text = self._whitespace_pattern.sub(' ', text)
        
        return text.strip()
    
    def check_spelling(self, filepath: str) -> List[Tuple[int, str, str, str]]:
        """Check spelling in LaTeX file"""
        issues = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            # Skip LaTeX command lines and comments
            if line.strip().startswith('%') or line.strip().startswith('\\'):
                continue
                
            clean_line = self.clean_latex_text(line)
            words = self._word_pattern.findall(clean_line.lower())
            
            for word in words:
                if word in self.common_misspellings:
                    issues.append((
                        line_num,
                        "Spelling Error",
                        f"'{word}' should be '{self.common_misspellings[word]}'",
                        line.strip()
                    ))
        
        return issues
    
    def check_duplicated_words(self, filepath: str) -> List[Tuple[int, str, str, str]]:
        """Check for duplicated words (like 'the the')"""
        issues = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%'):
                continue
                
            clean_line = self.clean_latex_text(line)
            words = self._word_pattern.findall(clean_line.lower())
            
            for i in range(len(words) - 1):
                if words[i] == words[i + 1] and len(words[i]) > 2:
                    issues.append((
                        line_num,
                        "Duplicated Word",
                        f"Duplicated word '{words[i]}'",
                        line.strip()
                    ))
        
        return issues
    
    def check_spelling_content(self, content: str) -> List[Tuple[int, str, str, str]]:
        """Check spelling in LaTeX content"""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Skip LaTeX command lines and comments
            if line.strip().startswith('%') or line.strip().startswith('\\'):
                continue
                
            clean_line = self.clean_latex_text(line)
            words = self._word_pattern.findall(clean_line.lower())
            
            for word in words:
                if word in self.common_misspellings:
                    issues.append((
                        line_num,
                        "Spelling Error",
                        f"'{word}' should be '{self.common_misspellings[word]}'",
                        line.strip()
                    ))
        
        return issues
    
    def check_duplicated_words_content(self, content: str) -> List[Tuple[int, str, str, str]]:
        """Check for duplicated words in LaTeX content"""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('%'):
                continue
                
            clean_line = self.clean_latex_text(line)
            words = self._word_pattern.findall(clean_line.lower())
            
            for i in range(len(words) - 1):
                if words[i] == words[i + 1] and len(words[i]) > 2:
                    issues.append((
                        line_num,
                        "Duplicated Word",
                        f"Duplicated word '{words[i]}'",
                        line.strip()
                    ))
        
        return issues

def main():
    if len(sys.argv) != 2:
        print("Usage: python spell_checker.py <tex_file>")
        sys.exit(1)
    
    checker = LaTeXSpellChecker()
    filepath = sys.argv[1]
    
    print(f"Checking spelling in {filepath}...")
    
    # Check spelling
    spelling_issues = checker.check_spelling(filepath)
    
    # Check duplicated words
    duplicate_issues = checker.check_duplicated_words(filepath)
    
    all_issues = spelling_issues + duplicate_issues
    
    if all_issues:
        print(f"\nFound {len(all_issues)} spelling/word issues:")
        for line_num, issue_type, description, context in all_issues:
            print(f"Line {line_num}: {issue_type} - {description}")
            print(f"  Context: {context}")
            print()
    else:
        print("No spelling issues found!")
    
    return len(all_issues)

if __name__ == "__main__":
    sys.exit(main())