# Multi-Skill Orchestration Patterns

When a workflow coordinates multiple skills, follow these patterns to keep things clean.

## Pattern 1: Sequential Delegation

The simplest pattern. The workflow calls skills one after another, passing output from one as input to the next.

```
Workflow: create-feature
  Step 1: naming-and-slugging → generate names for all artifacts
  Step 2: rule-forge → create governance rules for the feature
  Step 3: workflow-forge → create automation workflows
  Step 4: verify all artifacts are consistent
```

Each skill runs independently. The workflow's job is to coordinate the handoffs.

## Pattern 2: Parallel with Merge

When skills don't depend on each other, run them in parallel and merge results.

```
Workflow: audit-project
  Step 1: Load project context
  Step 2 (parallel):
    a) naming-and-slugging → audit file names
    b) rule-forge → validate existing rules
  Step 3: Merge findings into single report
  Step 4: Verify report completeness
```

This is faster but requires a merge step to reconcile the outputs.

## Pattern 3: Parent-Child Workflows

For complex orchestrations, the parent workflow delegates entire phases to child workflows.

```
Workflow: bootstrap-project (parent)
  Step 1: Gather requirements
  Step 2: Run setup-structure.md (child workflow)
  Step 3: Run create-governance.md (child workflow)
  Step 4: Run create-automation.md (child workflow)
  Step 5: Verify everything connects
```

**Key rule**: Child workflows must be independently runnable. If a child can't execute on its own, it's not a proper sub-workflow — it's just a group of steps that should stay in the parent.

## Handoff Contracts

When one step produces output that another step consumes, be explicit about the contract:

```markdown
### 3. Generate component  // turbo
Creates `src/components/{name}/{name}.tsx`
**Output**: File path written to `.workflow/last-created-file`

### 4. Create test for component  // turbo
Reads path from `.workflow/last-created-file`
Creates matching test file at `{path}.test.tsx`
```

The key insight: don't rely on "the previous step created something." Name exactly what was produced and where the next step can find it.

## Common Mistakes

**Implicit dependencies**: Step 5 assumes Step 3 created a file, but doesn't check. Always verify before consuming.

**Skill overloading**: Trying to do everything in one skill call instead of letting each skill do its job. If you need naming AND rules AND workflows, call each skill separately.

**Missing verification**: After orchestrating multiple skills, always verify that the combined output is consistent — names match, references are valid, no conflicts between artifacts.
