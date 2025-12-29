---
description: Rules and patterns for simulating real user behavior in E2E tests. Covers UI interactions, API flows, and scenario-based testing strategies.
name: user-simulation-test
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Task", "mcp__plugin_playwright_playwright__*"]
---
# User Simulation Test Rules

## Core Principle

**Test as users do, not as developers think.**

Simulate complete user journeys including:
- UI interactions (clicks, inputs, drag-drop, scrolls)
- Form submissions with realistic data
- Multi-step workflows with wait states
- Error scenarios and edge cases

---

## Test Type Selection

| Project Type | Primary Test | Secondary Test | Tools |
|--------------|--------------|----------------|-------|
| Web Frontend | Playwright E2E | API Mock | browser_* MCP tools |
| API Backend | HTTP Sequence | Unit Tests | curl/httpie + project runner |
| Full Stack | Integration E2E | API + UI | Playwright + API calls |
| CLI Tool | Script Execution | Unit Tests | Bash + project runner |

---

## Scenario Structure

Every test scenario must include:

```yaml
Scenario:
  name: string           # Descriptive name
  description: string    # What this tests
  preconditions: []      # Required state before test
  steps: Step[]          # User actions in sequence
  assertions: []         # Expected outcomes
  cleanup: []            # Post-test cleanup actions
```

> **Detailed templates**: `Read("references/scenario-templates.md")`

---

## UI Interaction Patterns

### Click & Input

| Action | Playwright Tool | Notes |
|--------|-----------------|-------|
| Click button | `browser_click` | Use ref from snapshot |
| Type text | `browser_type` | Set slowly=true for key handlers |
| Fill form | `browser_fill_form` | Batch field updates |
| Select option | `browser_select_option` | For dropdowns |
| Press key | `browser_press_key` | Enter, Escape, etc. |

### Advanced Interactions

| Action | Playwright Tool | Use Case |
|--------|-----------------|----------|
| Drag & Drop | `browser_drag` | File upload, reordering |
| Hover | `browser_hover` | Tooltips, menus |
| Wait for text | `browser_wait_for` | Loading states |
| Take screenshot | `browser_take_screenshot` | Visual verification |

---

## API Testing Patterns

### HTTP Sequence Test

```yaml
APISequence:
  - name: "Login"
    method: POST
    endpoint: /api/auth/login
    body: { email, password }
    extract: { token: "response.data.token" }

  - name: "Create Resource"
    method: POST
    endpoint: /api/resources
    headers: { Authorization: "Bearer ${token}" }
    body: { ... }
    assertions:
      - status: 201
      - response.data.id: exists
```

---

## Test Data Strategy

### Realistic Data Generation

| Field Type | Strategy | Example |
|------------|----------|---------|
| Email | Pattern + timestamp | `test_${timestamp}@example.com` |
| Name | Fake names | Korean/English name generators |
| Phone | Pattern | `010-XXXX-XXXX` |
| Address | Realistic fake | Valid format, fake data |
| Payment | Test cards | Stripe/Toss test numbers |

### Data Isolation

- Always use test-specific data prefixes
- Clean up created data after tests
- Use separate test database/environment when possible

---

## Wait Strategies

| Situation | Strategy | Tool |
|-----------|----------|------|
| Page load | Wait for element | `browser_wait_for` text |
| API response | Wait for network idle | `browser_network_requests` |
| Animation | Fixed delay | `browser_wait_for` time |
| Loading spinner | Wait for disappear | `browser_wait_for` textGone |

---

## Assertion Patterns

### UI Assertions

```yaml
UIAssertions:
  - type: text_visible
    value: "Success message"

  - type: element_exists
    selector: "[data-testid='result']"

  - type: url_contains
    value: "/dashboard"

  - type: no_console_errors
    level: error
```

### API Assertions

```yaml
APIAssertions:
  - type: status_code
    expected: 200

  - type: response_time
    max_ms: 2000

  - type: json_path
    path: "$.data.items"
    condition: "length > 0"
```

---

## Error Handling

### Graceful Degradation

1. **Screenshot on failure** - Capture visual state
2. **Console log capture** - Get browser errors
3. **Network request dump** - See failed API calls
4. **State preservation** - Keep test state for debugging

### Recovery Actions

```yaml
OnFailure:
  - capture_screenshot
  - capture_console_logs
  - capture_network_requests
  - preserve_browser_state  # Don't close immediately
```

---

## Test Categories

| Category | Frequency | Coverage |
|----------|-----------|----------|
| Smoke | Every change | Critical paths only |
| Regression | Pre-release | Full user journeys |
| Integration | Feature complete | Cross-service flows |
| Load | Scheduled | Performance under stress |

> **Test patterns**: `Read("references/test-patterns.md")`
