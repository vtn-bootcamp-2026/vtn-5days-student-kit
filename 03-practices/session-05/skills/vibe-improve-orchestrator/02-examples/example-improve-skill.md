# Example: Improve một Skill hiện có

## Kịch bản

User nói: *"vibe-improve-orchestrator: improve skill vibe-opc-orchestrator — workflow phần delivery đang không handle đúng case khi QA reject"*

---

## Phase 1: IDENTIFY

```
Skill path: ~/.claude/skills/vibe-opc-orchestrator/SKILL.md
Issue type: BUG — Workflow không handle QA reject case
Severity: HIGH
Affected layers: Workflow + Rules
```

## Phase 2: RESEARCH

```
Upstream: vibe-opc_sample-delivery-pm, vibe-opc_sample-ceo
Downstream: vibe-opc_sample-delivery-qa, vibe-opc_sample-delivery-tech
Impact: Modify delivery workflow — affects 3 downstream skills
```

## Phase 3: SURFACE REVIEW (vibe-review --quick)

```
Score: 72/100 — Acceptable
Issues found:
- Missing QA reject handling in workflow
- No escalation path for rejected deliveries
- Rules lack validation for QA feedback format
```

## Phase 4: DEEP TEST (Baseline)

```
Layer 1 Unit: 8/10 PASS (2 FAIL — QA reject steps)
Layer 2 Integration: 3/5 PASS (delivery→QA handoff broken on reject)
Layer 3 Functional: 4/7 PASS (reject scenario fails)
Overall: 15/22 = 68%
```

## Phase 5: PLAN (KWSR Priority)

```
K1: Add QA rejection criteria knowledge — S
W1: Add reject→rework loop in workflow — M
W2: Add escalation path for 3rd reject — S
S1: Add reject handling to delivery-qa skill — M
R1: Add rule: QA feedback must include reason + severity — S
T1: Add test cases for reject scenarios — S

Execution: Batch 1 (K1+W1+W2) → Batch 2 (S1+R1) → Batch 3 (T1)
```

## Phase 6: EXECUTE

```
Applied K1: Added QA rejection criteria section ✅
Applied W1: Added reject→rework loop in workflow diagram ✅
Applied W2: Added escalation after 3rd consecutive reject ✅
Applied S1: Updated delivery-qa skill with reject handling ✅
Applied R1: Added QA feedback validation rule ✅
Applied T1: Added 5 new test cases for reject scenarios ✅
```

## Phase 7: VERIFY

```
Before → After:
Pass Rate: 68% → 95% (+27%)
Critical failures: 2 → 0
Regressions: 0

Test-by-test:
- QA reject happy path: FAIL → PASS ✅
- QA reject with reason: FAIL → PASS ✅
- 3rd reject escalation: N/A → PASS 🆕
- Normal delivery flow: PASS → PASS ✅ (no regression)

Verdict: IMPROVED ✅
```
