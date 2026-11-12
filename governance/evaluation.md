---
type: EvaluationProtocol
title: Evaluating AI answers about Tempfind
description: How to test whether AI assistants answer Tempfind questions correctly, using the cases in evaluations/cases.yaml.
generated:
  by: claude/okf-restructure
  at: '2026-11-12T13:55:00Z'
status: draft
review_required: true
audience: reference
sources:
- id: cases
  resource: ../evaluations/cases.yaml
id: tempfind:governance/evaluation
---

# Evaluating AI answers about Tempfind

The cases in `evaluations/cases.yaml` hold prompts, expected answers and sources. They measure whether an assistant answers Tempfind questions accurately, with or without the bundle attached. No run has been executed yet.[^cases]

## Modes

| Mode | Setup | Measures |
|---|---|---|
| Open web | Ask the assistant with web search, no files | What public AI answers say today |
| Bundle attached | Attach `dist/okf/` or point the assistant at `https://tempfind.com/okf/index.md` | Whether the bundle improves accuracy |
| Baseline | No search, no files | Model prior knowledge |

## Procedure

1. Use the exact prompt text from the case.
2. Record the model, version, date, mode and repository commit in a copy of `evaluations/result-template.json`.
3. Mark each required fact present or missing, each checkable claim correct or incorrect, and any unsupported guarantee.
4. A critical case fails if the answer states a wrong fee, a wrong employment relationship, or a coverage claim the Terms do not support.

## Cadence

Run the open-web mode monthly and after major site changes, and compare results by case ID.

[^cases]: Evaluation cases, ../evaluations/cases.yaml.
