# Test Patterns

## Discovery Patterns

### Auto-Detect Test Environment

```yaml
DetectionFlow:
  1. Check for existing test configuration:
     - package.json scripts (test, e2e, integration)
     - pytest.ini, setup.cfg (Python)
     - Makefile test targets
     - docker-compose.test.yml

  2. Detect frontend framework:
     - React: src/App.jsx, package.json dependencies
     - Vue: src/App.vue, vue.config.js
     - Next.js: pages/, next.config.js
     - Nuxt: nuxt.config.js

  3. Detect backend framework:
     - Express: app.js with express
     - FastAPI: main.py with FastAPI
     - Django: manage.py, settings.py
     - NestJS: src/main.ts with NestFactory

  4. Detect existing test tools:
     - Playwright: playwright.config.ts
     - Cypress: cypress.config.js
     - Jest: jest.config.js
     - Pytest: conftest.py
```

---

## Execution Patterns

### Progressive Test Execution

```yaml
Strategy: ProgressiveExecution
Description: "Start simple, increase complexity on success"

Levels:
  - level: 1
    name: "Smoke Test"
    description: "Basic health check"
    tests:
      - homepage_loads
      - api_responds
      - auth_works
    on_fail: STOP
    on_success: continue

  - level: 2
    name: "Critical Path"
    description: "Main user journeys"
    tests:
      - user_registration
      - core_feature_flow
      - checkout_flow
    on_fail: report_and_continue
    on_success: continue

  - level: 3
    name: "Edge Cases"
    description: "Error handling and boundaries"
    tests:
      - invalid_input_handling
      - concurrent_access
      - rate_limiting
    on_fail: log_only
```

---

### Parallel vs Sequential

```yaml
ParallelSafe:
  description: "Tests that can run simultaneously"
  conditions:
    - No shared state modification
    - Independent data
    - Isolated resources
  examples:
    - read_only_queries
    - independent_user_flows
    - static_page_tests

Sequential:
  description: "Tests that must run in order"
  conditions:
    - Shared state dependency
    - Order-dependent data
    - Resource locks
  examples:
    - user_creation → user_login
    - cart_add → checkout
    - file_upload → file_process
```

---

## UI Test Patterns

### Page Object Pattern

```yaml
PageObject:
  name: "LoginPage"
  url: "/login"

  elements:
    email_input: "[data-testid='email']"
    password_input: "[data-testid='password']"
    submit_button: "button[type='submit']"
    error_message: ".error-message"
    forgot_password_link: "a[href='/forgot-password']"

  actions:
    login:
      steps:
        - fill: email_input, "${email}"
        - fill: password_input, "${password}"
        - click: submit_button
      returns: DashboardPage | ErrorState

    get_error:
      steps:
        - read_text: error_message
      returns: string
```

---

### Visual Regression Pattern

```yaml
VisualRegression:
  description: "Compare screenshots against baselines"

  workflow:
    1. Navigate to page
    2. Wait for stable state (no animations)
    3. Take screenshot
    4. Compare with baseline:
       - If baseline exists: diff comparison
       - If new: save as baseline
    5. Report differences

  config:
    threshold: 0.1  # 0.1% pixel difference allowed
    ignore_regions:
      - timestamps
      - dynamic_ads
      - user_avatars
    responsive_breakpoints:
      - 375   # mobile
      - 768   # tablet
      - 1440  # desktop
```

---

### Accessibility Testing Pattern

```yaml
AccessibilityTest:
  description: "Verify WCAG compliance"

  checks:
    - type: "aria_labels"
      description: "All interactive elements have labels"

    - type: "color_contrast"
      description: "Text meets contrast requirements"

    - type: "keyboard_navigation"
      description: "All features accessible via keyboard"

    - type: "focus_indicators"
      description: "Focus state is visible"

    - type: "screen_reader"
      description: "Content is screen reader compatible"

  tools:
    - axe-core (via browser evaluate)
    - lighthouse accessibility audit
```

---

## API Test Patterns

### Contract Testing

```yaml
ContractTest:
  description: "Verify API matches expected schema"

  workflow:
    1. Load OpenAPI/Swagger spec
    2. For each endpoint:
       - Send valid request
       - Validate response schema
       - Send invalid request
       - Validate error schema

  assertions:
    - response_matches_schema
    - required_fields_present
    - correct_data_types
    - proper_error_format
```

---

### Load Testing Pattern

```yaml
LoadTest:
  description: "Test system under various load conditions"

  scenarios:
    - name: "Normal Load"
      concurrent_users: 10
      duration: "1m"
      requests_per_second: 50

    - name: "Peak Load"
      concurrent_users: 100
      duration: "5m"
      requests_per_second: 500

    - name: "Spike Test"
      pattern: "0 → 1000 → 0 users"
      duration: "2m"

  metrics:
    - response_time_p95
    - error_rate
    - throughput
    - resource_utilization
```

---

### Error Injection Pattern

```yaml
ErrorInjection:
  description: "Test system resilience to failures"

  scenarios:
    - name: "Network Timeout"
      inject: delay(5000)
      target: external_api_call
      expected: graceful_timeout_handling

    - name: "Service Unavailable"
      inject: status(503)
      target: dependency_service
      expected: circuit_breaker_opens

    - name: "Invalid Response"
      inject: corrupt_json
      target: api_response
      expected: parse_error_handled

    - name: "Database Down"
      inject: connection_refused
      target: database
      expected: fallback_or_error_page
```

---

## Data Patterns

### Test Data Factory

```yaml
DataFactory:
  User:
    template:
      email: "test_${uuid}@example.com"
      name: "${faker.name}"
      phone: "${faker.phone.ko}"
    variants:
      admin:
        role: "admin"
        permissions: ["*"]
      basic:
        role: "user"
        permissions: ["read"]

  Product:
    template:
      name: "Test Product ${uuid}"
      price: "${random(1000, 100000)}"
      stock: "${random(0, 100)}"
    variants:
      out_of_stock:
        stock: 0
      expensive:
        price: 1000000
```

---

### Database Seeding Pattern

```yaml
DatabaseSeed:
  description: "Prepare test database state"

  workflow:
    pre_test:
      - truncate_test_tables
      - insert_base_data
      - create_test_users

    post_test:
      - delete_created_records
      - restore_original_state

  isolation:
    strategy: "transaction_rollback"
    # OR
    strategy: "dedicated_test_db"
    # OR
    strategy: "prefix_isolation"  # All test data has TEST_ prefix
```

---

## Reporting Patterns

### Test Report Structure

```yaml
TestReport:
  summary:
    total: 50
    passed: 45
    failed: 3
    skipped: 2
    duration: "5m 32s"

  failed_tests:
    - name: "checkout_flow"
      error: "Payment button not found"
      screenshot: "./screenshots/checkout_fail.png"
      console_logs: "./logs/checkout.log"
      network_log: "./logs/checkout_network.har"

  performance:
    slowest_tests:
      - name: "file_upload"
        duration: "45s"
      - name: "search_with_filters"
        duration: "12s"

  coverage:
    pages_tested: 15
    api_endpoints_tested: 32
    user_flows_covered: 8
```

---

### Failure Analysis Pattern

```yaml
FailureAnalysis:
  categories:
    - name: "UI Element Not Found"
      pattern: "Element .* not found"
      likely_causes:
        - "Page not loaded completely"
        - "Element selector changed"
        - "Feature removed/hidden"
      suggestions:
        - "Increase wait timeout"
        - "Update element selector"
        - "Check feature flags"

    - name: "API Timeout"
      pattern: "Request timeout"
      likely_causes:
        - "Server overloaded"
        - "Network issues"
        - "Long-running operation"
      suggestions:
        - "Check server health"
        - "Increase timeout"
        - "Add retry logic"

    - name: "Assertion Failed"
      pattern: "Expected .* but got"
      likely_causes:
        - "Business logic changed"
        - "Data inconsistency"
        - "Race condition"
      suggestions:
        - "Update expected values"
        - "Add data validation"
        - "Add synchronization"
```

---

## Integration Patterns

### CI/CD Integration

```yaml
CIIntegration:
  triggers:
    - on: pull_request
      run: smoke_tests
    - on: merge_to_main
      run: full_regression
    - on: release_tag
      run: full_regression + load_tests

  artifacts:
    - test_reports
    - screenshots
    - video_recordings
    - coverage_reports

  notifications:
    on_failure:
      - slack_channel
      - email_to_author
    on_success:
      - update_dashboard
```

---

### Environment Configuration

```yaml
Environments:
  local:
    base_url: "http://localhost:3000"
    api_url: "http://localhost:8000"
    database: "test_local"
    features:
      debug_mode: true
      mock_payments: true

  staging:
    base_url: "https://staging.example.com"
    api_url: "https://api.staging.example.com"
    database: "test_staging"
    features:
      debug_mode: true
      mock_payments: true

  production:
    base_url: "https://example.com"
    api_url: "https://api.example.com"
    database: null  # Read-only tests
    features:
      debug_mode: false
      mock_payments: false
    restrictions:
      - no_data_mutation
      - read_only_tests
```
