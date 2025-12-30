# Creative Approaches Reference

Patterns for generating unconventional implementation solutions.

## Approach Categories

### 1. API Bypass / Workarounds

When official APIs don't support needed functionality.

#### Techniques

| Technique | Description | Risk |
|-----------|-------------|------|
| Undocumented Endpoints | Use internal APIs not in public docs | Medium |
| Monkey Patching | Modify runtime behavior | High |
| Event Interception | Capture and modify events | Medium |
| Prototype Manipulation | Extend built-in objects | High |
| Internal Method Access | Use `_private` methods | Medium |

#### Example: Using Internal API

```typescript
// Problem: Official SDK doesn't support batch operations
// Creative: Access internal batch endpoint

// Instead of:
for (const item of items) {
  await sdk.create(item); // 100 API calls
}

// Use internal endpoint:
await fetch(`${sdk.baseUrl}/_internal/batch`, {
  method: 'POST',
  headers: { ...sdk.headers },
  body: JSON.stringify({ operations: items.map(i => ({ type: 'create', data: i })) })
});
```

---

### 2. Technology Combination

Combining libraries/patterns in unexpected ways.

#### Techniques

| Technique | Description | Risk |
|-----------|-------------|------|
| Cross-Ecosystem Bridge | Connect incompatible systems | Low |
| Hybrid Architecture | Mix paradigms (e.g., REST + GraphQL) | Medium |
| Pattern Fusion | Combine design patterns | Low |
| Tool Chaining | Pipe output between tools | Low |

#### Example: Hybrid Query Layer

```typescript
// Problem: Need fast full-text search + relational queries
// Creative: Combine Prisma with Elasticsearch

class HybridQuery {
  async searchWithRelations(query: string, include: object) {
    // Fast text search via Elasticsearch
    const ids = await elastic.search({
      query: { match: { content: query } }
    });

    // Relational data via Prisma
    return prisma.post.findMany({
      where: { id: { in: ids } },
      include
    });
  }
}
```

---

### 3. Constraint-Ignoring Experiments

Testing assumptions that "can't be done".

#### Techniques

| Technique | Description | Risk |
|-----------|-------------|------|
| Limit Testing | Push past documented limits | High |
| Alternative Protocols | Use unexpected communication methods | Medium |
| Resource Pooling | Share what's usually isolated | Medium |
| Lazy Loading Extreme | Defer everything possible | Low |

#### Example: Connection Limit Bypass

```typescript
// Assumption: "Max 100 WebSocket connections"
// Experiment: Multiplexing over fewer connections

class ConnectionPool {
  private connections: WebSocket[] = [];
  private channels = new Map<string, MessageChannel>();

  // Multiplex multiple logical channels over few physical connections
  createChannel(id: string): MessageChannel {
    const conn = this.connections[this.getNextConnection()];
    const channel = new MultiplexedChannel(conn, id);
    this.channels.set(id, channel);
    return channel;
  }
}
```

---

## Creative Thinking Framework

### Inversion

Ask: "What if we did the opposite?"

| Normal | Inverted |
|--------|----------|
| Client pulls data | Server pushes (WebSocket/SSE) |
| Synchronous processing | Eventual consistency |
| Validate before save | Save then validate asynchronously |
| Preload everything | Load on demand |

### Elimination

Ask: "What if we removed this constraint?"

| Constraint | Elimination |
|------------|-------------|
| Must use official SDK | Direct API calls |
| Must run on server | Move to edge/client |
| Must be real-time | Accept eventual consistency |
| Must be synchronous | Use message queue |

### Combination

Ask: "What unrelated things could we combine?"

| A | B | Combination |
|---|---|-------------|
| Rate limiter | Cache | Self-healing rate limiter |
| ORM | Search engine | Hybrid query layer |
| Auth | WebSocket | Authenticated streams |
| Logger | Metrics | Observability pipeline |

### Substitution

Ask: "What else could do this?"

| Original | Substitute |
|----------|------------|
| Database transactions | Event sourcing + compensation |
| Traditional tokens | Cryptographic proofs |
| REST API | GraphQL subscriptions |
| Polling | Server-sent events |

### Borrowing

Ask: "How do other domains solve this?"

| Domain | Pattern | Application |
|--------|---------|-------------|
| Gaming | Entity Component System | Complex UI state |
| Distributed Systems | CRDTs | Collaborative editing |
| Embedded | State machines | Complex workflows |
| Compilers | AST manipulation | Code transformation |

---

## Skillmaker-Inspired Patterns

### Isolated Daemonized Serena

**Pattern**: Run MCP server in isolation for safe experimentation

**Apply when**: Need sandboxed execution environment

```typescript
// Launch isolated Serena instance for experiment
const isolatedSerena = spawn('serena', ['--isolated', '--project', tempDir]);
```

### Claude-only SDK Prompt Injection

**Pattern**: Solve problems with system prompts, no tools

**Apply when**: Tool access is limited or tools are insufficient

```typescript
// Instead of building a tool, inject capability via prompt
const systemPrompt = `
You have the ability to [capability].
When asked to [action], respond with [format].
`;
```

### Creative CLI Usage

**Pattern**: Undocumented command combinations

**Apply when**: Official CLI is limiting

```bash
# Combine CLI tools in unexpected ways
tool-a export --format=json | jq '.data' | tool-b import --stdin
```

---

## Anti-Patterns to Reconsider

Sometimes "bad practices" are solutions:

### Global State

Usually avoided, but useful for:
- Single-page app session data
- Device capability detection
- Feature flags

### Polling

Usually replaced by WebSockets, but better for:
- Unreliable connections
- Simple implementations
- Battery-constrained devices

### Code Duplication

Usually eliminated, but acceptable for:
- Performance-critical paths
- Reducing dependencies
- Isolation between modules

### Mutable State

Usually avoided, but practical for:
- Performance optimization
- Interop with imperative libraries
- Real-time updates

---

## Risk Assessment Matrix

| Approach Type | Typical Risk | Mitigation |
|---------------|--------------|------------|
| API Bypass | Medium-High | Version pinning, fallback code |
| Tech Combination | Low-Medium | Integration tests |
| Constraint Testing | High | Sandboxed environment |
| Pattern Inversion | Low | A/B testing |
| Anti-pattern Usage | Medium | Clear documentation |

## When NOT to Use Creative Approaches

- [ ] Standard solution exists and works well
- [ ] Team doesn't have capacity to maintain custom code
- [ ] Security-critical path
- [ ] Compliance/regulatory constraints
- [ ] Short timeline without testing capacity
