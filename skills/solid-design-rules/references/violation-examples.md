# SOLID Violation Examples

## Detection Patterns and Anti-Patterns

This reference provides concrete examples of SOLID violations and detection patterns for automated analysis.

---

## SRP Violations

### Pattern: God Class
```typescript
// Detection: Class with > 10 methods or > 5 dependencies
class UserManager {
  createUser() { ... }
  updateUser() { ... }
  deleteUser() { ... }
  sendEmail() { ... }
  validatePayment() { ... }
  generateReport() { ... }
  exportToCSV() { ... }
  syncWithExternalAPI() { ... }
  handleWebhook() { ... }
  processQueue() { ... }
  // Too many unrelated responsibilities
}
```

### Pattern: Mixed Concerns in Single Method
```typescript
// Detection: Method > 20 lines with multiple try-catch or await chains
async function processOrder(order) {
  // Validation (responsibility 1)
  if (!order.items) throw new Error();
  
  // Business logic (responsibility 2)
  const total = order.items.reduce((sum, i) => sum + i.price, 0);
  
  // Persistence (responsibility 3)
  await db.insert('orders', { ...order, total });
  
  // Notification (responsibility 4)
  await email.send(order.customer, 'Order confirmed');
  
  // Logging (responsibility 5)
  console.log('Order processed:', order.id);
}
```

---

## OCP Violations

### Pattern: Type-Based Switch
```typescript
// Detection: switch/if chains on type/status fields
function calculateShipping(type: string): number {
  switch (type) {
    case 'standard': return 5.99;
    case 'express': return 15.99;
    case 'overnight': return 29.99;
    // Adding new type requires modification here
  }
}
```

### Pattern: Boolean Flag Parameters
```typescript
// Detection: boolean parameters that change behavior
function formatOutput(data: any, asJson: boolean, pretty: boolean) {
  if (asJson) {
    return pretty ? JSON.stringify(data, null, 2) : JSON.stringify(data);
  } else {
    return pretty ? formatPrettyText(data) : formatPlainText(data);
  }
}
```

---

## LSP Violations

### Pattern: Exception-Throwing Override
```typescript
// Detection: Child method throws where parent doesn't
class BasePayment {
  process(amount: number): void { ... }
}

class CryptoPayment extends BasePayment {
  process(amount: number): void {
    if (amount < 0.001) {
      throw new Error('Amount too small for crypto'); // Violates LSP
    }
    // ...
  }
}
```

### Pattern: Empty Implementation
```typescript
// Detection: Methods with empty body or just throwing NotImplemented
class Bird {
  fly(): void { ... }
}

class Penguin extends Bird {
  fly(): void {
    // Empty - penguins can't fly
    // This violates LSP!
  }
}
```

---

## ISP Violations

### Pattern: Fat Interface
```typescript
// Detection: Interface with > 5 methods
interface DataAccess {
  create(data: any): Promise<void>;
  read(id: string): Promise<any>;
  update(id: string, data: any): Promise<void>;
  delete(id: string): Promise<void>;
  list(): Promise<any[]>;
  search(query: string): Promise<any[]>;
  export(): Promise<Buffer>;
  import(data: Buffer): Promise<void>;
  validate(data: any): boolean;
  transform(data: any): any;
}
```

### Pattern: Unused Dependencies
```typescript
// Detection: Class implements interface but leaves methods empty
class ReadOnlyRepository implements DataAccess {
  create() { throw new Error('Not supported'); }
  update() { throw new Error('Not supported'); }
  delete() { throw new Error('Not supported'); }
  // Only read-related methods are implemented
  read(id: string) { ... }
  list() { ... }
}
```

---

## DIP Violations

### Pattern: Direct Instantiation
```typescript
// Detection: 'new' keyword for infrastructure classes in business logic
class OrderService {
  processOrder(order: Order) {
    const db = new MySQLConnection();        // Violation
    const cache = new RedisClient();          // Violation
    const logger = new FileLogger();          // Violation
    // ...
  }
}
```

### Pattern: Framework Coupling
```typescript
// Detection: Framework decorators on domain entities
@Entity()                           // Violation - ORM in domain
@Table({ name: 'users' })
class User {
  @PrimaryGeneratedColumn()
  id: number;
  
  @Column()
  email: string;
}
```

---

## Detection Commands

### Serena Pattern Search
```
# Find God classes (> 10 methods)
search_for_pattern: "class.*\{.*\n.*function.*\n.*function.*\n.*function.*"

# Find switch statements
search_for_pattern: "switch\s*\(.*type|status|kind"

# Find direct instantiation in services
search_for_pattern: "new\s+(MySQL|Redis|HTTP|SMTP)"

# Find fat interfaces
search_for_pattern: "interface.*\{[^\}]{500,}\}"
```

### Metrics-Based Detection
| Metric | Threshold | Violation |
|--------|-----------|-----------|
| Methods per class | > 10 | SRP |
| Dependencies per class | > 5 | SRP |
| Switch cases | > 3 | OCP |
| Interface methods | > 5 | ISP |
| Direct new in services | > 0 | DIP |
