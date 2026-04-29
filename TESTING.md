# Game Oracle - Testing Guide

Comprehensive testing guide for the Game Oracle project.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py                    # Shared fixtures and configuration
├── unit/                          # Unit tests for individual modules
│   ├── __init__.py
│   ├── test_text_cleaner.py      # Text cleaning functionality
│   ├── test_models.py            # Data model validation
│   └── test_data_processor.py    # Data processing and merging
└── integration/                   # Integration tests
    ├── __init__.py
    ├── test_api_endpoints.py      # FastAPI endpoint tests
    └── test_pipeline.py           # End-to-end pipeline tests
```

## Running Tests

### Run All Tests

```bash
python run_tests.py all
```

or

```bash
pytest tests/
```

### Run Unit Tests Only

```bash
python run_tests.py unit
```

or

```bash
pytest tests/unit/ -v
```

### Run Integration Tests Only

```bash
python run_tests.py integration
```

or

```bash
pytest tests/integration/ -v
```

### Run with Verbose Output

```bash
python run_tests.py all -v
```

or

```bash
pytest tests/ -vv
```

### Run with Coverage Report

```bash
python run_tests.py --coverage
```

or

```bash
pytest tests/ --cov=backend --cov-report=html
```

## Test Categories

### Unit Tests

Located in `tests/unit/`, these test individual components in isolation.

#### `test_text_cleaner.py`
Tests text cleaning pipeline:
- HTML tag removal
- Entity decoding
- BBCode removal
- Whitespace normalization
- Complete cleaning workflows

**Run:** `pytest tests/unit/test_text_cleaner.py -v`

#### `test_models.py`
Tests Pydantic data models:
- SteamGameDetails creation and validation
- SteamReview creation and validation
- SteamSpyData creation and validation
- Required field validation
- Type checking

**Run:** `pytest tests/unit/test_models.py -v`

#### `test_data_processor.py`
Tests data processing functionality:
- Owner range parsing
- Game data merging
- DataFrame construction
- DataFrame validation
- Data combining

**Run:** `pytest tests/unit/test_data_processor.py -v`

### Integration Tests

Located in `tests/integration/`, these test end-to-end workflows and API interactions.

#### `test_api_endpoints.py`
Tests FastAPI REST endpoints:
- Health check
- API info
- Game search
- Single game collection
- Batch game collection
- Input validation
- Error handling

**Run:** `pytest tests/integration/test_api_endpoints.py -v`

#### `test_pipeline.py`
Tests the complete data collection pipeline:
- Pipeline initialization
- Game search
- Single game processing
- Batch game processing
- Data quality validation
- Sentiment analysis
- Text cleaning in context

**Run:** `pytest tests/integration/test_pipeline.py -v`

## Test Markers

Use pytest markers to run specific test categories:

```bash
# Run only unit tests
pytest tests/ -m unit

# Run only API tests
pytest tests/ -m api

# Run only pipeline tests
pytest tests/ -m pipeline

# Run only text cleaning tests
pytest tests/ -m text_cleaning

# Skip slow tests
pytest tests/ -m "not slow"
```

Available markers:
- `unit` - Unit tests
- `integration` - Integration tests
- `slow` - Long-running tests
- `api` - API endpoint tests
- `pipeline` - Pipeline tests
- `models` - Data model tests
- `processors` - Data processor tests
- `text_cleaning` - Text cleaning tests

## Expected Results

### Unit Tests (3 test modules, 13 tests)

```
test_text_cleaner.py
  ✓ test_strip_html
  ✓ test_unescape_html_entities
  ✓ test_remove_steam_bbcode
  ✓ test_normalize_whitespace
  ✓ test_clean_review
  ✓ test_clean_description
  ✓ test_remove_urls
  ✓ test_clean_all_aggressive
  ✓ test_empty_input
  ✓ test_whitespace_only_input

test_models.py
  ✓ test_valid_game_details
  ✓ test_game_details_with_price
  ✓ test_valid_positive_review
  ✓ test_valid_negative_review
  ✓ test_review_with_none_playtime
  ✓ test_valid_steamspy_data
  ✓ test_steamspy_data_with_price
  ✓ test_empty_tags

test_data_processor.py
  ✓ test_parse_owners_range_valid
  ✓ test_parse_owners_range_invalid
  ✓ test_parse_owners_range_empty
  ✓ test_merge_game_data
  ✓ test_merge_game_data_without_steamspy
  ✓ test_build_reviews_dataframe
  ✓ test_build_game_summary_dataframe
  ✓ test_validate_dataframe_valid
  ✓ test_validate_dataframe_missing_column
  ✓ test_validate_dataframe_invalid_sentiment
  ✓ test_combine_game_dataframes
```

**Status:** All unit tests should PASS (no network required)

### Integration Tests (2 test modules, 25+ tests)

```
test_api_endpoints.py
  ✓ test_health_check_returns_ok
  ✓ test_api_info_returns_metadata
  ✓ test_api_info_contains_all_endpoints
  ✓ test_search_finds_existing_game
  ✓ test_search_returns_not_found_for_invalid_game
  ✓ test_search_missing_query
  ✓ test_collect_single_game_success
  ✓ test_collect_dataframe_structure
  ✓ test_collect_game_not_found
  ✓ test_collect_max_reviews_validation
  ✓ test_collect_missing_title
  ✓ test_batch_collect_multiple_games
  ✓ test_batch_collect_empty_list_validation
  ✓ test_batch_collect_too_many_games
  ✓ test_batch_collect_max_reviews_validation
  ✓ test_batch_collect_missing_games
  ✓ test_root_endpoint

test_pipeline.py
  ✓ test_pipeline_initialization
  ✓ test_search_game_by_name
  ✓ test_search_nonexistent_game
  ✓ test_process_single_game
  ✓ test_process_single_game_sentiment_distribution
  ✓ test_process_single_game_no_null_required_fields
  ✓ test_collect_and_process_multiple_games
  ✓ test_collect_single_nonexistent_game
  ✓ test_collect_and_process_partial_success
  ✓ test_no_duplicate_reviews
  ✓ test_game_metadata_consistency
  ✓ test_positive_ratio_calculation
  ✓ test_text_cleaning_applied
  ✓ test_review_text_not_empty
```

**Status:** All integration tests should PASS (requires internet for Steam API)

## Test Execution Flow

### Pre-test Setup (conftest.py)

1. Backend module is added to Python path
2. Logging is configured
3. Shared fixtures are initialized

### Unit Test Execution

1. Text cleaning tests (no external dependencies)
2. Model validation tests (Pydantic validation)
3. Data processor tests (with sample data)

**Duration:** < 5 seconds

### Integration Test Execution

1. API endpoint tests (with test client)
2. Pipeline tests (with real Steam API calls)

**Duration:** 2-5 minutes (depends on network)

## Continuous Integration

Example GitHub Actions workflow:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.12']
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -e backend/
        pip install pytest pytest-cov
    
    - name: Run unit tests
      run: pytest tests/unit/ -v
    
    - name: Run integration tests
      run: pytest tests/integration/ -v
    
    - name: Generate coverage
      run: pytest tests/ --cov=backend --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Troubleshooting

### Tests fail with "module not found"

**Solution:** Ensure backend directory is in Python path
```bash
cd SteamAnalysisTool
python -m pytest tests/
```

### API integration tests timeout

**Solution:** Increase timeout or skip slow tests
```bash
pytest tests/ -m "not slow" --timeout=30
```

### Mock data not working in tests

**Solution:** Check that fixtures are properly defined in conftest.py
```bash
pytest tests/ --fixtures  # List all available fixtures
```

## Best Practices

1. **Run tests before committing:**
   ```bash
   pytest tests/unit/      # Quick check
   ```

2. **Run full test suite before pushing:**
   ```bash
   pytest tests/ -v        # Complete validation
   ```

3. **Use markers for selective testing:**
   ```bash
   pytest tests/ -m "unit and not slow"
   ```

4. **Check coverage regularly:**
   ```bash
   pytest tests/ --cov=backend --cov-report=html
   ```

5. **Keep test files organized:**
   - Unit tests in `tests/unit/`
   - Integration tests in `tests/integration/`
   - Use descriptive test names

## Adding New Tests

### Unit Test Template

```python
import pytest
from module_to_test import FunctionOrClass

class TestMyComponent:
    """Test suite for MyComponent."""

    @pytest.fixture
    def component(self):
        """Create component instance."""
        return MyComponent()

    def test_basic_functionality(self, component):
        """Test basic functionality."""
        result = component.do_something()
        assert result == expected_value

    @pytest.mark.unit
    def test_edge_case(self, component):
        """Test edge case."""
        result = component.do_something(edge_case_input)
        assert result == expected_value
```

### Integration Test Template

```python
import pytest
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)

class TestMyEndpoint:
    """Test suite for my endpoint."""

    @pytest.mark.api
    def test_endpoint_success(self, client):
        """Test endpoint success case."""
        response = client.post("/api/endpoint", json={...})
        assert response.status_code == 200
        assert response.json() == {...}

    @pytest.mark.api
    def test_endpoint_validation(self, client):
        """Test endpoint validation."""
        response = client.post("/api/endpoint", json={})
        assert response.status_code == 422
```

## Performance Benchmarks

Expected test execution times:

| Test Type | Count | Duration | Notes |
|-----------|-------|----------|-------|
| Unit tests | 13 | < 5s | No external dependencies |
| API tests | 17 | 10-30s | Local test client |
| Pipeline tests | 14 | 2-5 min | Real Steam API calls |
| **Total** | **44** | **2-5 min** | Depends on network |

## Coverage Targets

- **Overall:** > 80%
- **Core modules:** > 90%
- **API endpoints:** > 85%
- **Data processors:** > 95%

Generate coverage report:
```bash
pytest tests/ --cov=backend --cov-report=html
open htmlcov/index.html
```
