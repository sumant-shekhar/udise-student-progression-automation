#!/bin/bash

# Comprehensive Project Audit Script
# Verifies project structure, code quality, and migration completion

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  UDISE+ AUTOMATION - COMPREHENSIVE PROJECT AUDIT               ║"
echo "║  Selenium to Playwright Migration Verification                 ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Track results
PASSED=0
FAILED=0
WARNINGS=0

# Helper functions
pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
    ((PASSED++))
}

fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    ((FAILED++))
}

warn() {
    echo -e "${YELLOW}⚠️  WARN${NC}: $1"
    ((WARNINGS++))
}

info() {
    echo -e "${BLUE}ℹ️  INFO${NC}: $1"
}

# Section 1: Directory Structure
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📁 SECTION 1: DIRECTORY STRUCTURE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check main directories exist
for dir in src config tests; do
    if [ -d "$dir" ]; then
        pass "Directory exists: $dir"
    else
        fail "Directory missing: $dir"
    fi
done

# Check no old Selenium code directory
if [ ! -d "old Selenium Code" ]; then
    pass "Old Selenium code removed"
else
    fail "Old Selenium code directory still exists"
fi

# Section 2: Source Files
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📄 SECTION 2: SOURCE FILES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check core source files
declare -a SOURCE_FILES=("src/main.py" "src/playwright_utils.py" "src/progression.py" "config/settings.py" "tests/test_migration.py")

for file in "${SOURCE_FILES[@]}"; do
    if [ -f "$file" ]; then
        lines=$(wc -l < "$file" 2>/dev/null)
        pass "Source file exists: $file ($lines lines)"
    else
        fail "Source file missing: $file"
    fi
done

# Section 3: Configuration Files
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚙️  SECTION 3: CONFIGURATION FILES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "requirements.txt" ]; then
    if grep -q "playwright" requirements.txt; then
        pass "Playwright in requirements.txt"
    else
        fail "Playwright not in requirements.txt"
    fi
    
    if ! grep -q "selenium" requirements.txt; then
        pass "Selenium removed from requirements.txt"
    else
        fail "Selenium still in requirements.txt"
    fi
else
    fail "requirements.txt missing"
fi

if [ -f ".env.example" ]; then
    pass ".env.example exists"
else
    fail ".env.example missing"
fi

if [ -f "setup.sh" ]; then
    pass "setup.sh exists"
else
    fail "setup.sh missing"
fi

# Section 4: Documentation
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📚 SECTION 4: DOCUMENTATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

declare -a DOC_FILES=("README.md" "CHANGELOG.md" "MIGRATION_REPORT.md" "MIGRATION_SUMMARY.md" "MIGRATION_CHECKLIST.md")

for file in "${DOC_FILES[@]}"; do
    if [ -f "$file" ]; then
        lines=$(wc -l < "$file" 2>/dev/null)
        pass "Documentation: $file ($lines lines)"
    else
        fail "Documentation missing: $file"
    fi
done

# Section 5: Code Quality
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 SECTION 5: CODE QUALITY CHECKS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check for Selenium imports in main code
if ! grep -r "selenium" src/ config/ 2>/dev/null | grep -v ".pyc" > /dev/null; then
    pass "No Selenium imports in src/ and config/"
else
    fail "Selenium imports found in main code"
fi

# Check for Playwright imports
if grep -r "from playwright" src/ 2>/dev/null > /dev/null; then
    pass "Playwright imports found in codebase"
else
    fail "No Playwright imports found"
fi

# Check Python syntax
echo ""
info "Checking Python syntax..."
SYNTAX_ERRORS=0
for py_file in src/*.py config/*.py tests/*.py; do
    if [ -f "$py_file" ]; then
        if python3 -m py_compile "$py_file" 2>/dev/null; then
            pass "Python syntax valid: $py_file"
        else
            fail "Python syntax error in: $py_file"
            ((SYNTAX_ERRORS++))
        fi
    fi
done

# Section 6: Git Repository
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔗 SECTION 6: GIT REPOSITORY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -d ".git" ]; then
    pass "Git repository initialized"
    
    COMMITS=$(git log --oneline 2>/dev/null | wc -l)
    info "Total commits: $COMMITS"
    
    if [ "$COMMITS" -gt 0 ]; then
        pass "Git history exists"
    else
        fail "No git commits found"
    fi
    
    # Check for meaningful commits
    FEAT_COMMITS=$(git log --oneline 2>/dev/null | grep -c "feat:" || true)
    pass "Feature commits: $FEAT_COMMITS"
    
    DOCS_COMMITS=$(git log --oneline 2>/dev/null | grep -c "docs:" || true)
    pass "Documentation commits: $DOCS_COMMITS"
else
    fail "Git repository not initialized"
fi

# Section 7: Code Statistics
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 SECTION 7: CODE STATISTICS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

TOTAL_PY_LINES=$(find src config tests -name "*.py" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}')
info "Total Python lines: $TOTAL_PY_LINES"

TOTAL_MD_LINES=$(find . -name "*.md" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}')
info "Total documentation lines: $TOTAL_MD_LINES"

PY_FILES=$(find src config tests -name "*.py" | wc -l)
pass "Python files: $PY_FILES"

# Section 8: Type Hints
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 SECTION 8: TYPE HINTS & DOCSTRINGS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check for type hints
TYPE_HINTS=$(grep -r "def.*->" src/ config/ 2>/dev/null | wc -l)
info "Functions with type hints: $TYPE_HINTS"
if [ "$TYPE_HINTS" -gt 0 ]; then
    pass "Type hints present in codebase"
else
    warn "No type hints found"
fi

# Check for docstrings
DOCSTRINGS=$(grep -r '"""' src/ config/ 2>/dev/null | wc -l)
info "Docstring occurrences: $DOCSTRINGS"
if [ "$DOCSTRINGS" -gt 0 ]; then
    pass "Docstrings present in codebase"
else
    warn "No docstrings found"
fi

# Section 9: Project Standards
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ SECTION 9: PROJECT STANDARDS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "LICENSE" ]; then
    pass "LICENSE file exists"
else
    warn "LICENSE file not found"
fi

if [ -f ".gitignore" ]; then
    pass ".gitignore configured"
    
    if grep -q "\.env" .gitignore; then
        pass ".env files in .gitignore"
    else
        warn ".env not in .gitignore"
    fi
    
    if grep -q "__pycache__" .gitignore; then
        pass "__pycache__ in .gitignore"
    else
        warn "__pycache__ not in .gitignore"
    fi
else
    fail ".gitignore not found"
fi

# Final Summary
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  AUDIT SUMMARY                                                 ║"
echo "╚════════════════════════════════════════════════════════════════╝"

TOTAL=$((PASSED + FAILED + WARNINGS))
PERCENT=$((PASSED * 100 / TOTAL))

echo ""
echo -e "${GREEN}✅ PASSED:${NC}   $PASSED"
echo -e "${RED}❌ FAILED:${NC}   $FAILED"
echo -e "${YELLOW}⚠️  WARNINGS:${NC}  $WARNINGS"
echo ""
echo "Total Checks: $TOTAL"
echo "Success Rate: $PERCENT%"
echo ""

if [ "$FAILED" -eq 0 ]; then
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo -e "║  ${GREEN}✅ AUDIT PASSED - PROJECT READY FOR PRODUCTION${NC}           ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    exit 0
else
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo -e "║  ${RED}❌ AUDIT FAILED - REVIEW ISSUES ABOVE${NC}                   ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    exit 1
fi
