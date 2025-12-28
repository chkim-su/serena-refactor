---
description: SOLID principles and TDD enforcement rules. Reference for maintainable software design. Used for code quality analysis, refactoring planning, and architecture verification.
name: solid-design-rules
allowed-tools: ["Read", "Grep", "Glob"]
---
# SOLID Design Rules

## Core Principle

**Design for change isolation.**
Predict what will change and strictly limit the propagation scope of those changes.

---

## 1. Single Responsibility Principle (SRP)

Every class, module, and function must have **exactly one reason to change**.

**Prohibited:**
- Mixing business rules, data persistence, and formatting in one class
- "God" services that coordinate unrelated concerns
- Methods exceeding 20 lines
- Classes with more than 5 dependencies

**Required:**
- Explicit separation of policy, orchestration, and execution
- Small, intent-revealing components

**Example - Violation:**
```typescript
// ❌ SRP Violation: Handles business logic, DB, and email
class UserService {
  async createUser(data: UserData) {
    // Validation logic
    if (!data.email.includes('@')) throw new Error('Invalid email');

    // DB save
    await db.query('INSERT INTO users...');

    // Email sending
    await smtp.send({ to: data.email, subject: 'Welcome!' });

    // Logging
    console.log('User created:', data.email);
  }
}
```

**Example - Fixed:**
```typescript
// ✓ SRP Compliant: Each responsibility separated
class UserValidator {
  validate(data: UserData): ValidationResult { ... }
}

class UserRepository {
  async save(user: User): Promise<void> { ... }
}

class WelcomeEmailSender {
  async send(user: User): Promise<void> { ... }
}

class UserCreationUseCase {
  constructor(
    private validator: UserValidator,
    private repo: UserRepository,
    private emailer: WelcomeEmailSender
  ) {}

  async execute(data: UserData): Promise<User> {
    this.validator.validate(data);
    const user = await this.repo.save(new User(data));
    await this.emailer.send(user);
    return user;
  }
}
```

---

## 2. Open-Closed Principle (OCP)

Systems must be **open for extension, closed for modification**.

**Prohibited:**
- `if/switch` chains that grow with types or enums
- Feature flags embedded in core logic
- Boolean parameters that branch behavior

**Required:**
- Interface-based extensibility
- Strategy pattern and polymorphic dispatch

**Example - Violation:**
```typescript
// ❌ OCP Violation: Adding new payment requires modifying switch
function processPayment(type: string, amount: number) {
  switch (type) {
    case 'credit': return processCreditCard(amount);
    case 'paypal': return processPaypal(amount);
    case 'crypto': return processCrypto(amount);
    // Adding new type requires case here...
  }
}
```

**Example - Fixed:**
```typescript
// ✓ OCP Compliant: New payment just implements interface
interface PaymentProcessor {
  process(amount: number): Promise<PaymentResult>;
}

class CreditCardProcessor implements PaymentProcessor { ... }
class PaypalProcessor implements PaymentProcessor { ... }
class CryptoProcessor implements PaymentProcessor { ... }

// New method: Just add implementation without modifying existing code
class ApplePayProcessor implements PaymentProcessor { ... }

class PaymentService {
  constructor(private processors: Map<string, PaymentProcessor>) {}

  async process(type: string, amount: number) {
    return this.processors.get(type)?.process(amount);
  }
}
```

---

## 3. Liskov Substitution Principle (LSP)

Subtypes must be **completely substitutable** for their base types.

**Prohibited:**
- Empty method implementations in subclasses
- `instanceof` checks in calling code
- Strengthening preconditions in subclasses
- Throwing unexpected exceptions

**Required:**
- Behavioral contracts maintained across all implementations

**Example - Violation:**
```typescript
// ❌ LSP Violation: Square breaks Rectangle contract
class Rectangle {
  constructor(public width: number, public height: number) {}
  setWidth(w: number) { this.width = w; }
  setHeight(h: number) { this.height = h; }
  area() { return this.width * this.height; }
}

class Square extends Rectangle {
  setWidth(w: number) { this.width = this.height = w; }  // Contract violation!
  setHeight(h: number) { this.width = this.height = h; } // Contract violation!
}

// Client code doesn't work as expected
function resize(rect: Rectangle) {
  rect.setWidth(5);
  rect.setHeight(10);
  console.log(rect.area()); // Rectangle: 50, Square: 100 (!)
}
```

**Example - Fixed:**
```typescript
// ✓ LSP Compliant: Separated with common interface
interface Shape {
  area(): number;
}

class Rectangle implements Shape {
  constructor(public width: number, public height: number) {}
  area() { return this.width * this.height; }
}

class Square implements Shape {
  constructor(public side: number) {}
  area() { return this.side * this.side; }
}
```

---

## 4. Interface Segregation Principle (ISP)

Interfaces must be designed from the **client's perspective**.

**Prohibited:**
- Interfaces with more than 5 methods
- Forcing implementations to depend on methods they don't use

**Required:**
- Minimal interfaces per role
- Separation of commands and queries

**Example - Violation:**
```typescript
// ❌ ISP Violation: Fat interface
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
  attendMeeting(): void;
  writeReport(): void;
}

// Robot doesn't need eat, sleep but forced to implement
class Robot implements Worker {
  work() { ... }
  eat() { throw new Error('Not applicable'); }  // Meaningless implementation
  sleep() { throw new Error('Not applicable'); }
  ...
}
```

**Example - Fixed:**
```typescript
// ✓ ISP Compliant: Separated by role
interface Workable {
  work(): void;
}

interface Feedable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

class Human implements Workable, Feedable, Sleepable { ... }
class Robot implements Workable { ... }  // Only implements what's needed
```

---

## 5. Dependency Inversion Principle (DIP)

High-level business logic must **not depend on low-level details**.

**Prohibited:**
- `new` keyword for infrastructure classes in business logic
- Direct DB/HTTP client usage in domain services
- Framework annotations on domain entities

**Required:**
- Constructor-based dependency injection
- Interfaces owned by business layer

**Example - Violation:**
```typescript
// ❌ DIP Violation: Business logic directly depends on concrete classes
class OrderService {
  private db = new MySQLConnection();  // Direct creation!
  private mailer = new SendGridClient(); // Direct creation!

  async createOrder(data: OrderData) {
    await this.db.query('INSERT INTO orders...');
    await this.mailer.send(data.customerEmail, 'Order confirmed');
  }
}
```

**Example - Fixed:**
```typescript
// ✓ DIP Compliant: Depends on abstractions, injected
interface OrderRepository {
  save(order: Order): Promise<void>;
}

interface NotificationService {
  notify(recipient: string, message: string): Promise<void>;
}

class OrderService {
  constructor(
    private repo: OrderRepository,       // Interface injected
    private notifier: NotificationService // Interface injected
  ) {}

  async createOrder(data: OrderData) {
    const order = new Order(data);
    await this.repo.save(order);
    await this.notifier.notify(data.customerEmail, 'Order confirmed');
  }
}

// Implementations injected from outside
const service = new OrderService(
  new MySQLOrderRepository(),
  new SendGridNotifier()
);
```

---

## 6. TDD Rules

### Test Before Implementation

1. Define failing test scenarios first
2. Write only enough implementation to satisfy tests
3. Refactor only after tests pass

### Design Violation Signals

| Signal | Violation |
|--------|-----------|
| Excessive mocking | SRP violation |
| Need to test private methods | Wrong boundaries |
| DB/Network needed for unit tests | DIP violation |

**Example - Testable Design:**
```typescript
// ✓ Testable: Dependencies can be mocked via injection
describe('OrderService', () => {
  it('should save order and notify customer', async () => {
    const mockRepo = { save: jest.fn() };
    const mockNotifier = { notify: jest.fn() };
    const service = new OrderService(mockRepo, mockNotifier);

    await service.createOrder({ customerEmail: 'test@test.com' });

    expect(mockRepo.save).toHaveBeenCalled();
    expect(mockNotifier.notify).toHaveBeenCalledWith('test@test.com', expect.any(String));
  });
});
```

---

## 7. Repository Pattern

**Repository = Collection abstraction, not persistence mechanism**

**Prohibited:**
- SQL/query language in interfaces
- Infrastructure terms in method names

**Required:**
- Domain-centric operations (`find`, `save`, `exists`)
- Swappable with in-memory implementation for tests

**Example:**
```typescript
// ✓ Domain-centric interface
interface UserRepository {
  findById(id: UserId): Promise<User | null>;
  findByEmail(email: Email): Promise<User | null>;
  save(user: User): Promise<void>;
  exists(id: UserId): Promise<boolean>;
}

// In-memory implementation for tests
class InMemoryUserRepository implements UserRepository {
  private users: Map<string, User> = new Map();

  async findById(id: UserId) {
    return this.users.get(id.value) ?? null;
  }
  // ...
}
```
