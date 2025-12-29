# Scenario Templates

## Basic Templates

### Authentication Flow

```yaml
Scenario:
  name: "User Authentication Flow"
  description: "Complete login/logout cycle with session verification"

  preconditions:
    - User account exists
    - User is logged out
    - Login page accessible

  steps:
    - action: navigate
      url: "/login"

    - action: fill_form
      fields:
        - name: email
          value: "${TEST_USER_EMAIL}"
        - name: password
          value: "${TEST_USER_PASSWORD}"

    - action: click
      element: "Login button"
      ref: "button[type='submit']"

    - action: wait_for
      text: "Welcome"
      timeout: 5000

    - action: verify
      type: url_contains
      value: "/dashboard"

    - action: click
      element: "Logout button"
      ref: "[data-testid='logout']"

    - action: wait_for
      text: "Login"

  assertions:
    - type: session_cleared
    - type: redirect_to_login

  cleanup:
    - clear_cookies
    - clear_local_storage
```

---

### Form Submission Flow

```yaml
Scenario:
  name: "Complete Form Submission"
  description: "Multi-step form with validation and submission"

  preconditions:
    - User logged in
    - Form page accessible

  steps:
    # Step 1: Basic Information
    - action: navigate
      url: "/form/new"

    - action: fill_form
      fields:
        - name: title
          type: textbox
          value: "Test Entry ${TIMESTAMP}"
        - name: category
          type: combobox
          value: "Category A"
        - name: priority
          type: radio
          value: "high"

    - action: click
      element: "Next button"

    # Step 2: Details
    - action: wait_for
      text: "Step 2"

    - action: type
      element: "Description textarea"
      text: "Detailed description for testing purposes..."

    - action: click
      element: "Add attachment button"

    - action: file_upload
      paths: ["${TEST_FILE_PATH}"]

    - action: wait_for
      text: "Upload complete"

    # Step 3: Review & Submit
    - action: click
      element: "Review button"

    - action: wait_for
      text: "Review your submission"

    - action: verify
      type: text_visible
      value: "Test Entry"

    - action: click
      element: "Submit button"

    - action: wait_for
      text: "Successfully submitted"

  assertions:
    - type: success_message_visible
    - type: entry_created_in_database
    - type: notification_sent

  cleanup:
    - delete_test_entry
```

---

### E-commerce Checkout Flow

```yaml
Scenario:
  name: "Complete Purchase Flow"
  description: "Product selection through payment completion"

  preconditions:
    - User logged in
    - Products available in catalog
    - Test payment method configured

  steps:
    # Browse & Add to Cart
    - action: navigate
      url: "/products"

    - action: click
      element: "First product card"

    - action: wait_for
      text: "Product Details"

    - action: select_option
      element: "Size selector"
      value: "Medium"

    - action: type
      element: "Quantity input"
      text: "2"

    - action: click
      element: "Add to Cart button"

    - action: wait_for
      text: "Added to cart"

    # Cart Review
    - action: click
      element: "Cart icon"

    - action: wait_for
      text: "Shopping Cart"

    - action: verify
      type: text_visible
      value: "2 items"

    - action: click
      element: "Proceed to Checkout"

    # Checkout
    - action: wait_for
      text: "Checkout"

    - action: fill_form
      fields:
        - name: shipping_address
          value: "${TEST_ADDRESS}"
        - name: phone
          value: "${TEST_PHONE}"

    - action: click
      element: "Continue to Payment"

    # Payment
    - action: wait_for
      text: "Payment"

    - action: fill_form
      fields:
        - name: card_number
          value: "4242424242424242"  # Stripe test card
        - name: expiry
          value: "12/25"
        - name: cvc
          value: "123"

    - action: click
      element: "Complete Purchase"

    - action: wait_for
      text: "Order Confirmed"
      timeout: 10000

  assertions:
    - type: order_created
    - type: payment_processed
    - type: confirmation_email_sent
    - type: inventory_updated

  cleanup:
    - cancel_test_order
    - refund_test_payment
```

---

### Drag & Drop Interaction

```yaml
Scenario:
  name: "Kanban Board Reordering"
  description: "Move cards between columns via drag and drop"

  preconditions:
    - User logged in
    - Board exists with multiple columns
    - Cards exist in first column

  steps:
    - action: navigate
      url: "/board/${TEST_BOARD_ID}"

    - action: wait_for
      text: "Task Board"

    - action: snapshot
      note: "Capture initial state"

    - action: drag
      start_element: "First task card"
      start_ref: "[data-card-id='card-1']"
      end_element: "Done column"
      end_ref: "[data-column='done']"

    - action: wait_for
      time: 500  # Wait for animation

    - action: snapshot
      note: "Capture after drag"

    - action: verify
      type: element_in_container
      element: "[data-card-id='card-1']"
      container: "[data-column='done']"

  assertions:
    - type: card_moved_successfully
    - type: database_updated
    - type: activity_logged

  cleanup:
    - reset_board_state
```

---

### Real-time Feature Test

```yaml
Scenario:
  name: "Real-time Collaboration"
  description: "Test real-time updates between multiple sessions"

  preconditions:
    - Two test users exist
    - Shared document exists

  steps:
    # Session 1: Make changes
    - action: navigate
      url: "/doc/${TEST_DOC_ID}"
      session: "user1"

    - action: type
      element: "Document editor"
      text: "Hello from User 1"
      session: "user1"

    # Session 2: Verify sync
    - action: navigate
      url: "/doc/${TEST_DOC_ID}"
      session: "user2"

    - action: wait_for
      text: "Hello from User 1"
      timeout: 3000
      session: "user2"

    # Session 2: Make changes
    - action: type
      element: "Document editor"
      text: "\nHello from User 2"
      session: "user2"

    # Session 1: Verify sync
    - action: wait_for
      text: "Hello from User 2"
      timeout: 3000
      session: "user1"

  assertions:
    - type: both_sessions_synced
    - type: no_data_loss
    - type: cursor_positions_visible

  cleanup:
    - reset_document
    - close_sessions
```

---

## API Scenario Templates

### REST API CRUD Flow

```yaml
APIScenario:
  name: "Resource CRUD Operations"
  description: "Complete create, read, update, delete cycle"
  base_url: "${API_BASE_URL}"

  steps:
    - name: "Create Resource"
      method: POST
      endpoint: /api/resources
      headers:
        Authorization: "Bearer ${TOKEN}"
        Content-Type: application/json
      body:
        name: "Test Resource ${TIMESTAMP}"
        type: "test"
      assertions:
        - status: 201
        - response.data.id: exists
      extract:
        resource_id: "response.data.id"

    - name: "Read Resource"
      method: GET
      endpoint: /api/resources/${resource_id}
      headers:
        Authorization: "Bearer ${TOKEN}"
      assertions:
        - status: 200
        - response.data.name: contains "Test Resource"

    - name: "Update Resource"
      method: PUT
      endpoint: /api/resources/${resource_id}
      headers:
        Authorization: "Bearer ${TOKEN}"
        Content-Type: application/json
      body:
        name: "Updated Resource ${TIMESTAMP}"
      assertions:
        - status: 200
        - response.data.name: contains "Updated"

    - name: "Delete Resource"
      method: DELETE
      endpoint: /api/resources/${resource_id}
      headers:
        Authorization: "Bearer ${TOKEN}"
      assertions:
        - status: 204

    - name: "Verify Deletion"
      method: GET
      endpoint: /api/resources/${resource_id}
      headers:
        Authorization: "Bearer ${TOKEN}"
      assertions:
        - status: 404
```

---

### GraphQL Mutation Flow

```yaml
APIScenario:
  name: "GraphQL User Operations"
  description: "Test GraphQL mutations with proper error handling"
  base_url: "${GRAPHQL_ENDPOINT}"

  steps:
    - name: "Create User"
      method: POST
      body:
        query: |
          mutation CreateUser($input: CreateUserInput!) {
            createUser(input: $input) {
              id
              email
              createdAt
            }
          }
        variables:
          input:
            email: "test_${TIMESTAMP}@example.com"
            name: "Test User"
      assertions:
        - response.data.createUser.id: exists
        - response.errors: null
      extract:
        user_id: "response.data.createUser.id"

    - name: "Query User"
      method: POST
      body:
        query: |
          query GetUser($id: ID!) {
            user(id: $id) {
              id
              email
              profile {
                name
              }
            }
          }
        variables:
          id: "${user_id}"
      assertions:
        - response.data.user.email: contains "@example.com"
```
