# MCP Isolation Solution: Serena Context Optimization

## Problem Statement

Serena MCP 서버가 메인 세션의 컨텍스트를 과도하게 사용 (~22k tokens, 전체 MCP의 37%)하여 비효율 발생.

**증상**:
- 28개 Serena 도구가 매 세션마다 로드됨
- 도구 설명과 스키마가 컨텍스트 윈도우를 점유
- serena-refactor 에이전트가 호출될 때만 필요하지만 항상 로드됨

## Root Cause Analysis

1. **Claude Code Plugin Architecture**: 플러그인이 번들한 MCP 서버는 에이전트 레벨이 아닌 세션 레벨에서 로드됨
2. **MCP Server Scope**: `allowedMcpServers` 같은 에이전트별 MCP 격리 옵션이 없음
3. **No Native Solution**: 현재 Claude Code에서 에이전트별 MCP 격리를 직접 지원하지 않음

## Solution: SDK-based MCP Isolation

### Core Insight

`claude-only-sdk`가 CLI를 subprocess로 실행하며, `mcp_config` 파라미터로 별도 세션에 특정 MCP만 로드 가능:

```
Main Session (no Serena MCP)
    │
    ▼
serena_gateway.py (SDK wrapper)
    │
    ▼
asyncio.create_subprocess_exec("claude", "--mcp-config", "serena.mcp.json", ...)
    │
    ▼
Isolated Session (only Serena MCP)
```

### Implementation

**1. Global Serena Disable** (`~/.claude/settings.json`):
```json
"serena@claude-plugins-official": false
```

**2. Serena-only MCP Config** (`config/serena.mcp.json`):
```json
{
  "mcpServers": {
    "serena": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server"]
    }
  }
}
```

**3. SDK Wrapper** (`scripts/serena_gateway.py`):
- `ClaudeAdvancedConfig(mcp_config="...")` 사용
- 별도 세션에서 Serena만 로드
- 결과를 JSON으로 반환

## Expected Benefits

| Metric | Before | After |
|--------|--------|-------|
| MCP tools tokens | ~59k | ~37k |
| Serena overhead | ~22k (always) | 0 (on-demand) |
| Context efficiency | 70% | 100% |

## Verification Steps

### Completed
1. [x] Serena MCP 토큰 사용량 측정: ~22k tokens
2. [x] SDK 래퍼 스크립트 작성
3. [x] Serena 기능 테스트 (find_symbol, write_memory 등)

### Completed
1. [x] Claude Code 재시작하여 settings.json 적용
2. [x] 새 세션에서 `/context`로 토큰 절약량 확인 (MCP tools: 1.9k tokens)
3. [x] serena-gateway 에이전트를 래퍼 패턴으로 업데이트
4. [x] 종속 에이전트 호환성 검증 (인터페이스 유지됨)

## Test Commands

```bash
# 래퍼 동작 테스트
python3 scripts/serena_gateway.py \
  --prompt "Use list_memories to list available memories" \
  --project "." \
  --json

# 심볼 분석 테스트
python3 scripts/serena_gateway.py \
  --prompt "Use find_symbol to find 'run_serena_task' function" \
  --project "." \
  --json
```

## llm-sdk-guide Skill Contribution

이 해결책에서 `llm-sdk-guide` 스킬이 제공한 핵심 정보:

1. **CLI 기반 아키텍처 인식**: SDK가 API가 아닌 CLI subprocess임을 명시
2. **mcp_config 파라미터**: `--mcp-config` CLI 플래그로 변환됨을 설명
3. **컨텍스트 분리**: 별도 세션이 독립 컨텍스트 윈도우를 가짐

## Files Created/Modified

- `config/serena.mcp.json` - Serena 전용 MCP 설정
- `scripts/serena_gateway.py` - SDK 기반 격리 래퍼
- `~/.claude/skills/llm-sdk-guide/SKILL.md` - CLI 아키텍처 및 MCP Isolation 패턴 추가
- `~/.claude/settings.json` - `serena@claude-plugins-official: false`

---

*문서 생성일: 2025-12-26*
