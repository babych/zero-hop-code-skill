# Zero-Hop Code Skill

This extension provides a **zero-dependency, offline BM25/IDF + AST-boundary codebase search engine** via `scripts/code_memory.py`. It snaps results to `{ }` / HTML structure boundaries and returns exact line numbers, enabling single-hop surgical edits without extra file reads.

## When to Use (MANDATORY — prefer over Grep + Read)

- Large files (>300 lines) or monolithic HTML/Vue/React templates
- Multi-word concept queries (e.g. `"jwt refresh token expiry middleware"`)
- UI & i18n audits (hardcoded strings, missing translation keys)
- Finding all call-sites before renaming a symbol

## When NOT to Use

- Exact file & line already known → use `view_file` directly
- Files <300 lines → read directly
- Git diff/PR reviews → use `git diff` / `git log`

## Commands

```bash
# Search (auto-indexes on first run, ~0.15s delta refresh)
python scripts/code_memory.py search "<query>"

# All call-sites for a symbol
python scripts/code_memory.py refs "<symbolName>"

# File or repo outline (signatures + line numbers)
python scripts/code_memory.py outline [file]
```

### Key flags
- `--top <N>` / `-k <N>` — number of results (default: 3)
- `--full` — expand all matches to full slices (not just #1)
- `--brief` — 4-line previews for all matches
- `--path <dir>` / `-p <dir>` — target repo root

## Output Format

```
📍 src/middleware/auth.ts (Lines 42–48 of 210) [Score: 0.82] [TOP MATCH - FULL SLICE]
   L42  | export async function verifyRefreshToken(token: string) {
   ...
   L48  | }
```

The `[TOP MATCH - FULL SLICE]` block is fully self-contained — use it directly with `replace_file_content` / `Edit` without an additional `view_file` call.
