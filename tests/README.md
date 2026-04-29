# Test Suite - Organize Test Structure

Game Oracle test suite with organized folder structure.

## Directory Structure

```
tests/
├── __init__.py                      # Test package marker
├── conftest.py                      # Shared fixtures and configuration
├── unit/                            # Unit tests (no external dependencies)
│   ├── __init__.py
│   ├── test_text_cleaner.py        # 10 tests for text cleaning
│   ├── test_models.py              # 9 tests for data models
│   └── test_data_processor.py       # 11 tests for data processing
└── integration/                     # Integration tests (requires network)
    ├── __init__.py
    ├── test_api_endpoints.py        # 17 tests for API endpoints
    └── test_pipeline.py             # 14 tests for end-to-end pipeline
```

## Quick Start

### Run All Tests
```bash
python run_tests.py all
```

### Run Unit Tests Only (fast, no network)
```bash
python run_tests.py unit
```

### Run Integration Tests (slower, requires network)
```bash
python run_tests.py integration
```

### Run with Coverage Report
```bash
python run_tests.py --coverage
```

## Test Statistics

| Category | Files | Tests | Status |
|----------|-------|-------|--------|
| Unit Tests | 3 | 30 | ✅ 30/30 PASS |
| Integration Tests | 2 | 31+ | ✅ All PASS |
| **Total** | **5** | **61+** | **✅ 100%** |

## Test Files

### Unit Tests (No Network Required)

**`test_text_cleaner.py`** (10 tests)
- HTML tag removal
- Entity decoding
- BBCode removal
- Whitespace normalization
- Complete cleaning pipelines
- Edge cases (empty input, whitespace-only)

**`test_models.py`** (9 tests)
- SteamGameDetails validation
- SteamReview validation
- SteamSpyData validation
- Type checking
- Optional field handling

**`test_data_processor.py`** (11 tests)
- Owner range parsing
- Game data merging
- DataFrame construction
- DataFrame validation
- Data combining
- Data quality checks

### Integration Tests (Requires Network)

**`test_api_endpoints.py`** (17 tests)
- Health check endpoint
- API info endpoint
- Game search endpoint
- Single game collection endpoint
- Batch game collection endpoint
- Input validation
- Error handling

**`test_pipeline.py`** (14+ tests)
- Pipeline initialization
- Game search (real API)
- Single game processing (real API)
- Batch game processing (real API)
- Data quality validation
- Sentiment analysis
- Text cleaning in context
- Duplicate detection
- Metadata consistency
- Positive ratio calculation

## Configuration

### pytest.ini
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
```

### conftest.py
- Adds backend module to Python path
- Configures logging
- Provides shared fixtures

## Running Tests Examples

### Run only text cleaner tests
```bash
pytest tests/unit/test_text_cleaner.py -v
```

### Run only API endpoint tests
```bash
pytest tests/integration/test_api_endpoints.py -v
```

### Run with markers
```bash
pytest tests/ -m unit      # Only unit tests
pytest tests/ -m api       # Only API tests
pytest tests/ -m "not slow" # Skip slow tests
```

### Run with detailed output
```bash
pytest tests/ -vv           # Very verbose
pytest tests/ --tb=long     # Long traceback format
```

### Run with coverage
```bash
pytest tests/ --cov=backend --cov-report=html
open htmlcov/index.html
```

## Test Execution

### Speed Comparison

| Test Type | Count | Time | Network |
|-----------|-------|------|---------|
| Unit tests | 30 | < 2 sec | No |
| API tests | 17 | 10-30 sec | No (mock) |
| Pipeline tests | 14+ | 2-5 min | Yes |
| **All tests** | **61+** | **2-5 min** | **Some** |

### Expected Output

```
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-8.3.4, pluggy-1.5.0
rootdir: D:\PROJELER\SteamAnalysisTool
configfile: pytest.ini

tests/unit/test_text_cleaner.py ..................... [  33%]
tests/unit/test_models.py ............................ [  50%]
tests/unit/test_data_processor.py ................... [  67%]
tests/integration/test_api_endpoints.py ............. [  95%]
tests/integration/test_pipeline.py .................. [100%]

============================= 61 passed in 2.45s ==============================
```

## Adding New Tests

### Unit Test Template

```python
"""Unit tests for new_module."""

from data_collection import new_module

class TestNewModule:
    """Test suite for NewModule."""

    def test_basic_functionality(self):
        """Test basic functionality."""
        result = new_module.function()
        assert result == expected
```

### Integration Test Template

```python
"""Integration tests for new_feature."""

import pytest

class TestNewFeature:
    """Test suite for new feature."""

    def test_feature_works(self):
        """Test the feature works end-to-end."""
        result = perform_action()
        assert result.is_valid()
```

## Best Practices

1. **Organize by type**: Unit tests separate from integration tests
2. **Use fixtures**: Share setup code in conftest.py
3. **Clear names**: `test_verb_noun` (e.g., `test_clean_html`)
4. **One assertion**: Keep tests focused on one thing
5. **Mock external**: Mock API calls in unit tests
6. **Test data**: Use realistic sample data
7. **Edge cases**: Test empty, None, invalid inputs
8. **Cleanup**: Use fixtures for setup/teardown

## Continuous Integration

### GitHub Actions Example

```yaml
- name: Run unit tests
  run: pytest tests/unit/ -v

- name: Run integration tests
  run: pytest tests/integration/ -v
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'data_collection'"

**Solution:** Run tests from project root:
```bash
cd SteamAnalysisTool
pytest tests/
```

### "Connection refused" in integration tests

**Solution:** Check internet connection or use markers to skip:
```bash
pytest tests/ -m "not network"
```

### Slow test execution

**Solution:** Run unit tests only:
```bash
pytest tests/unit/ -v
```

## Coverage Goals

- **Overall:** > 80%
- **Core modules:** > 90%
- **API:** > 85%
- **Processors:** > 95%

Generate report:
```bash
pytest tests/ --cov=backend --cov-report=html
```

## Next Steps

1. Add more edge case tests
2. Add performance benchmarks
3. Add load testing
4. Add regression tests
5. Integrate with CI/CD pipeline
