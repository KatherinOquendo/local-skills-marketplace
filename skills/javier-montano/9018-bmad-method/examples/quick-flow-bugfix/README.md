# BMAD Example: Quick Flow — CSS Layout Bug Fix

## Scenario

A user reports that the task card titles on the TaskFlow kanban board are
truncated on mobile devices (< 375px width). The text overflows and is hidden
behind the priority badge. This is a clear, well-understood bug that doesn't
need a PRD, architecture review, or epic.

This is exactly what BMAD's **Quick Flow** is for: Barry agent handles small,
well-scoped changes that skip Phases 1-3 entirely.

---

## Step 1: Triage (Barry Agent)

Barry receives the bug report and makes a triage decision:

**Triage checklist**:
- Is this a new feature? **No** — it's a visual bug in existing functionality
- Does it change architecture? **No** — CSS-only change
- Does it affect data models? **No**
- Does it require a PRD update? **No**
- Is the fix scope < 1 day? **Yes** — estimated 1-2 hours
- Is the risk low? **Yes** — CSS change, easy rollback

**Decision**: Quick Flow. No full BMAD cycle needed.

## Step 2: Quick Spec (1 paragraph)

Barry writes a minimal spec directly in the commit or PR description:

> **Bug**: Task card titles truncate on viewports < 375px. The `.task-card-title`
> element uses `overflow: hidden` with a fixed width that doesn't account for the
> priority badge width. **Fix**: Replace the fixed width with `flex: 1` and add
> `min-width: 0` to allow text truncation with ellipsis instead of hard clip.
> Add `text-overflow: ellipsis` for graceful degradation. **Test**: Verify on
> 320px, 375px, and 390px viewports using Playwright visual regression.

That's it. No PRD. No architecture doc. No epic. No story file.

## Step 3: Implementation

Barry makes the change:

```css
/* Before */
.task-card-title {
  width: 200px;
  overflow: hidden;
  white-space: nowrap;
}

/* After */
.task-card-title {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
```

Barry also adds a Playwright test:

```typescript
test('task card title does not overflow on mobile', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto('/project/test-project/board');
  const title = page.locator('.task-card-title').first();
  const badge = page.locator('.priority-badge').first();
  const titleBox = await title.boundingBox();
  const badgeBox = await badge.boundingBox();
  // Title should not overlap with badge
  expect(titleBox!.x + titleBox!.width).toBeLessThanOrEqual(badgeBox!.x);
});
```

## Step 4: Self-Review

Barry runs through a quick self-review checklist:

- [x] Fix addresses the reported issue
- [x] No unrelated changes included
- [x] Visual test added for regression prevention
- [x] Tested on target viewports (320px, 375px, 390px)
- [x] No new linter warnings
- [x] CSS change is scoped (no global side effects)

## Step 5: Merge

PR is opened, CI passes, merged to `main`. Total time: 1.5 hours.

---

## What Would Have Happened in Full BMAD Flow?

If this bug had been forced through the full 4-phase BMAD cycle:

| Phase        | Activity                                    | Time      |
|-------------|---------------------------------------------|-----------|
| Phase 1     | Analyze the bug, write a product brief      | 30 min    |
| Phase 2     | Write a PRD with the fix as a requirement   | 45 min    |
| Phase 3     | Architecture review (unnecessary), story    | 30 min    |
| Gate         | Run 13-point readiness checklist            | 15 min    |
| Phase 4     | Implement the CSS fix                       | 30 min    |
| **Total**   |                                             | **2.5 hr**|

The Quick Flow took **1.5 hours** — a 40% time savings. More importantly, the
overhead of formal artifacts would have been pure waste for a 3-line CSS fix.

## When Quick Flow Is NOT Appropriate

Barry should escalate to the full flow if any of these are true:

- The "bug fix" actually requires a data model change
- The fix touches authentication or authorization logic
- The scope grows beyond 1 day during implementation
- The fix requires coordinating with another team
- The change affects a public API contract

The triage step is the critical gate. A wrong triage decision (using Quick
Flow for something that needed full BMAD) is caught by code review and can
be escalated retroactively.

## Files Produced

```
# Quick Flow produces NO BMAD artifact files.
# All context lives in the PR description and commit message.

git log --oneline:
  a1b2c3d fix: task card title truncation on mobile viewports (#42)
```

<!-- NOTE: This example is intentionally minimal to demonstrate that BMAD does not
     force ceremony on small changes. The triage step is the critical decision point —
     if Barry had found that the bug required a layout refactor touching 10+ files,
     he would have escalated to full flow. -->

## Lessons Learned

- **What went right**: The triage checklist prevented over-engineering. The initial instinct was to refactor the entire task card component, but the checklist constraint ("touches fewer than 5 files") kept scope tight. A 3-line CSS fix was sufficient.
- **What was tricky**: Writing the Playwright visual regression test required understanding the page layout structure. The test verifies the title does not overlap the priority badge — this is a spatial assertion, not a simple text check.
- **Key insight**: Quick Flow's value is not just speed — it is discipline. By explicitly checking "does this need architecture changes?" and "does this need new API endpoints?", Barry avoids the common trap of starting a "quick fix" that spirals into a refactor.

## Decisions Made

- **CSS fix over component refactor**: Chose `flex: 1` with `min-width: 0` instead of restructuring the component's HTML. Trade-off: addresses the symptom (truncation) but the underlying fixed-width pattern may recur in other components. Logged as a tech debt item for future sprint.
- **Visual regression test**: Added a Playwright spatial test rather than a unit test. Trade-off: slower to run (browser-based), but catches the actual visual issue that users reported. A unit test could verify CSS classes but not layout rendering.
