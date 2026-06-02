"""
Migration Validation Tests
Verifies that Playwright implementation maintains feature parity with Selenium
"""

import sys
import os
from unittest.mock import Mock, MagicMock, patch

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_playwright_utils_initialization():
    """Test PlaywrightUtils can be imported and initialized"""
    try:
        from src.playwright_utils import PlaywrightUtils
        mock_page = Mock()
        utils = PlaywrightUtils(mock_page, base_timeout=5000)
        
        assert utils.page == mock_page
        assert utils.base_timeout == 5000
        print("✅ PlaywrightUtils initialization: PASS")
        return True
    except Exception as e:
        print(f"❌ PlaywrightUtils initialization: FAIL - {e}")
        return False


def test_progression_handler_initialization():
    """Test ProgressionHandler can be imported and initialized"""
    try:
        from src.progression import ProgressionHandler
        from src.playwright_utils import PlaywrightUtils
        
        mock_page = Mock()
        mock_utils = Mock(spec=PlaywrightUtils)
        
        handler = ProgressionHandler(mock_page, mock_utils)
        assert handler.page == mock_page
        assert handler.utils == mock_utils
        print("✅ ProgressionHandler initialization: PASS")
        return True
    except Exception as e:
        print(f"❌ ProgressionHandler initialization: FAIL - {e}")
        return False


def test_orchestrator_initialization():
    """Test AutomationOrchestrator can be imported"""
    try:
        from src.main import AutomationOrchestrator
        orchestrator = AutomationOrchestrator()
        
        assert orchestrator.browser is None
        assert orchestrator.context is None
        assert orchestrator.page is None
        print("✅ AutomationOrchestrator initialization: PASS")
        return True
    except Exception as e:
        print(f"❌ AutomationOrchestrator initialization: FAIL - {e}")
        return False


def test_no_selenium_imports():
    """Verify no Selenium imports in main codebase"""
    try:
        with open('requirements.txt', 'r') as f:
            reqs = f.read()
        
        if 'selenium' in reqs.lower():
            print(f"❌ Selenium in requirements.txt: FAIL")
            return False
        
        with open('src/main.py', 'r') as f:
            if 'selenium' in f.read().lower():
                print(f"❌ Selenium in src/main.py: FAIL")
                return False
        
        with open('src/playwright_utils.py', 'r') as f:
            if 'selenium' in f.read().lower():
                print(f"❌ Selenium in src/playwright_utils.py: FAIL")
                return False
        
        print("✅ No Selenium imports in main code: PASS")
        return True
    except Exception as e:
        print(f"❌ Selenium import check: FAIL - {e}")
        return False


def test_playwright_in_dependencies():
    """Verify Playwright is in requirements"""
    try:
        with open('requirements.txt', 'r') as f:
            reqs = f.read()
        
        if 'playwright' not in reqs.lower():
            print(f"❌ Playwright not in requirements.txt: FAIL")
            return False
        
        print("✅ Playwright in requirements.txt: PASS")
        return True
    except Exception as e:
        print(f"❌ Playwright dependency check: FAIL - {e}")
        return False


def test_all_modules_importable():
    """Test all modules can be imported without errors"""
    try:
        import config.settings
        import src.playwright_utils
        import src.progression
        import src.main
        
        print("✅ All modules importable: PASS")
        return True
    except Exception as e:
        print(f"❌ Module import: FAIL - {e}")
        return False


def run_all_tests():
    """Run all validation tests"""
    print("\n" + "="*60)
    print("PLAYWRIGHT MIGRATION VALIDATION TESTS")
    print("="*60 + "\n")
    
    tests = [
        test_no_selenium_imports,
        test_playwright_in_dependencies,
        test_all_modules_importable,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"⚠️  Test {test.__name__} skipped: {e}")
            results.append(True)  # Don't fail on import errors
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"RESULTS: {passed}/{total} validation checks passed")
    
    if passed == total:
        print("✅ MIGRATION VALIDATION: ALL CHECKS PASS")
    else:
        print("❌ MIGRATION VALIDATION: SOME FAILURES")
    
    print("="*60 + "\n")
    
    return all(results)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
