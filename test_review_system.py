#!/usr/bin/env python3
"""
Test script for the paper review system
"""

import sys
import os

def test_review_system():
    """Test the paper review system"""
    print("Testing Paper Review System")
    print("=" * 40)
    
    # Check if required files exist
    required_files = [
        'ISTS_shin.tex',
        'spell_checker.py',
        'latex_validator.py', 
        'academic_style_checker.py',
        'paper_reviewer.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    
    # Test imports
    try:
        from spell_checker import LaTeXSpellChecker
        from latex_validator import LaTeXValidator
        from academic_style_checker import AcademicStyleChecker
        from paper_reviewer import PaperReviewer
        print("✅ All modules import successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Quick functionality test
    try:
        spell_checker = LaTeXSpellChecker()
        latex_validator = LaTeXValidator()
        style_checker = AcademicStyleChecker()
        reviewer = PaperReviewer()
        print("✅ All classes instantiate successfully")
    except Exception as e:
        print(f"❌ Instantiation error: {e}")
        return False
    
    # Test basic functionality
    try:
        # Test spell checker
        spelling_issues = spell_checker.check_spelling('ISTS_shin.tex')
        print(f"✅ Spell checker found {len(spelling_issues)} potential issues")
        
        # Test LaTeX validator  
        bracket_issues = latex_validator.check_bracket_matching('ISTS_shin.tex')
        print(f"✅ LaTeX validator found {len(bracket_issues)} bracket issues")
        
        # Test style checker
        informal_issues = style_checker.check_informal_expressions('ISTS_shin.tex')
        print(f"✅ Style checker found {len(informal_issues)} informal expressions")
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False
    
    print("\n🎉 All tests passed! The review system is working correctly.")
    return True

if __name__ == "__main__":
    success = test_review_system()
    sys.exit(0 if success else 1)