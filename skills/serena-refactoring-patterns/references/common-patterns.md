# Common Refactoring Patterns

## Step-by-Step Patterns with Serena MCP

---

## 1. Extract Method

**When**: A method is too long or contains repeated code blocks.

### Step-by-Step
```yaml
1. Analyze original method:
   - Tool: find_symbol
   - Args: { name_path: "ClassName/longMethod", include_body: true }
   
2. Identify extraction target:
   - Lines X-Y form a cohesive unit
   - Has clear inputs and outputs
   
3. Design new method signature:
   - Name: descriptive verb + noun
   - Parameters: variables used from context
   - Return: values needed after the block
   
4. Insert new method:
   - Tool: insert_after_symbol
   - Args: { name_path: "ClassName/longMethod", body: NEW_METHOD }
   
5. Replace original code with call:
   - Tool: replace_content
   - Args: { needle: ORIGINAL_BLOCK, repl: METHOD_CALL }
   
6. Verify references:
   - Tool: find_referencing_symbols
   - Check: no broken references
```

### Example
```typescript
// Before
class OrderProcessor {
  async process(order: Order) {
    // 20 lines of validation
    if (!order.items) throw new Error('No items');
    if (order.total < 0) throw new Error('Invalid total');
    // ... more validation
    
    // Continue processing
    await this.save(order);
  }
}

// After extraction
class OrderProcessor {
  async process(order: Order) {
    this.validateOrder(order);  // Extracted call
    await this.save(order);
  }
  
  private validateOrder(order: Order): void {
    if (!order.items) throw new Error('No items');
    if (order.total < 0) throw new Error('Invalid total');
    // ... validation logic
  }
}
```

---

## 2. Extract Interface

**When**: Multiple classes share common methods or DIP violation exists.

### Step-by-Step
```yaml
1. Analyze class structure:
   - Tool: find_symbol
   - Args: { name_path: "ConcreteClass", depth: 1 }
   
2. Identify interface candidates:
   - Public methods used by clients
   - Methods that define the contract
   
3. Create interface definition:
   - Tool: insert_before_symbol
   - Args: { name_path: "ConcreteClass", body: INTERFACE_DEF }
   
4. Update class declaration:
   - Tool: replace_symbol_body
   - Args: Add "implements IInterface" to class
   
5. Update dependent classes:
   - Tool: find_referencing_symbols
   - For each: replace concrete type with interface
```

### Example
```typescript
// Before
class MySQLUserRepository {
  findById(id: string): User { ... }
  save(user: User): void { ... }
}

// After
interface UserRepository {
  findById(id: string): User;
  save(user: User): void;
}

class MySQLUserRepository implements UserRepository {
  findById(id: string): User { ... }
  save(user: User): void { ... }
}
```

---

## 3. Move Method

**When**: A method belongs better in another class.

### Step-by-Step
```yaml
1. Read source method:
   - Tool: find_symbol
   - Args: { name_path: "SourceClass/method", include_body: true }
   
2. Add to target class:
   - Tool: insert_after_symbol
   - Args: { name_path: "TargetClass/lastMethod", body: METHOD }
   
3. Find all call sites:
   - Tool: find_referencing_symbols
   - Args: { name_path: "SourceClass/method" }
   
4. Update each call site:
   - Tool: replace_content
   - For each: sourceObj.method() → targetObj.method()
   
5. Remove from source:
   - Tool: replace_symbol_body
   - Args: Remove method or leave delegation
```

### Example
```typescript
// Before
class Order {
  calculateTax(): number {
    // Tax calculation logic
    return this.total * this.taxRate;
  }
}

// After
class TaxCalculator {
  calculate(order: Order): number {
    return order.total * order.taxRate;
  }
}
```

---

## 4. Replace Conditional with Polymorphism

**When**: Switch/if chains on type discriminators.

### Step-by-Step
```yaml
1. Find conditional:
   - Tool: search_for_pattern
   - Args: { pattern: "switch.*type|if.*instanceof" }
   
2. Identify branches:
   - Each case/branch becomes a class
   
3. Create base interface:
   - Tool: insert_before_symbol
   - Args: Create interface with common method
   
4. Create implementation classes:
   - Tool: create_text_file (for each type)
   - Implement interface method
   
5. Replace switch with polymorphic call:
   - Tool: replace_content
   - Args: switch → strategy.execute()
   
6. Create factory/registry:
   - Tool: create_text_file
   - Map type → implementation
```

### Example
```typescript
// Before
function getArea(shape: Shape): number {
  switch (shape.type) {
    case 'circle': return Math.PI * shape.radius ** 2;
    case 'rectangle': return shape.width * shape.height;
    case 'triangle': return 0.5 * shape.base * shape.height;
  }
}

// After
interface Shape {
  getArea(): number;
}

class Circle implements Shape {
  getArea(): number { return Math.PI * this.radius ** 2; }
}

class Rectangle implements Shape {
  getArea(): number { return this.width * this.height; }
}
```

---

## 5. Inline Temporary

**When**: A temporary variable adds no clarity.

### Step-by-Step
```yaml
1. Find variable assignment:
   - Tool: search_for_pattern
   - Args: { pattern: "const temp = expression" }
   
2. Find all usages:
   - Tool: search_for_pattern
   - Args: { pattern: "temp" in same scope }
   
3. Replace all usages:
   - Tool: replace_content
   - Args: { needle: "temp", repl: "expression" }
   
4. Remove declaration:
   - Tool: replace_content
   - Args: { needle: "const temp = expression;\n", repl: "" }
```

---

## 6. Introduce Parameter Object

**When**: Method has > 3 parameters.

### Step-by-Step
```yaml
1. Identify parameter group:
   - Tool: find_symbol
   - Note parameters that travel together
   
2. Create parameter class:
   - Tool: create_text_file
   - Define class/interface with properties
   
3. Update method signature:
   - Tool: replace_symbol_body
   - Change: (a, b, c) → (params: ParamObject)
   
4. Update all call sites:
   - Tool: find_referencing_symbols
   - For each: replace arguments with object
```

### Example
```typescript
// Before
function createUser(
  name: string,
  email: string,
  age: number,
  address: string,
  phone: string
) { ... }

// After
interface CreateUserParams {
  name: string;
  email: string;
  age: number;
  address: string;
  phone: string;
}

function createUser(params: CreateUserParams) { ... }
```

---

## 7. Safe Rename

**When**: Renaming a symbol across the codebase.

### Step-by-Step
```yaml
1. Check impact:
   - Tool: find_referencing_symbols
   - Note: number of references
   
2. Verify uniqueness:
   - Tool: find_symbol
   - Args: { name_path: "newName" }
   - Ensure: no conflicts
   
3. Execute rename:
   - Tool: rename_symbol
   - Args: { name_path: "oldName", new_name: "newName" }
   
4. Verify results:
   - All references automatically updated
```

---

## Quick Reference: Tool Selection

| Refactoring | Primary Tool | Supporting Tools |
|-------------|--------------|------------------|
| Extract Method | insert_after_symbol | replace_content |
| Extract Interface | insert_before_symbol | replace_symbol_body |
| Move Method | insert_after_symbol | find_referencing_symbols |
| Rename | rename_symbol | find_symbol |
| Delete | replace_symbol_body (empty) | find_referencing_symbols |
| Replace | replace_content | search_for_pattern |
