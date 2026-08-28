# AI Application Engineering Roadmap

A practical, production-focused learning roadmap for becoming an AI Application Engineer.

This repository documents my progression from foundational large-language-model integration to designing, testing, securing, deploying, and operating production-ready AI applications.

The course contains:

- 8 modules
- 32 core lessons
- 8 integrated capstone milestones
- One progressively developed production-style application
- Approximately 42–60 hours of required work
- Optional extensions for deeper practice

## Primary Goal

The goal is not simply to learn how to call an AI API or write prompts.

By completing this roadmap, I should be able to build AI-powered applications that are:

- Structured and testable
- Provider-neutral
- Secure by design
- Grounded in trusted data
- Protected by authorization and validation
- Observable and measurable
- Reliable under failure
- Deployable and maintainable
- Defensible during technical interviews and architecture reviews

## Learning Approach

Each lesson combines focused theory with implementation.

The roadmap follows these principles:

1. Build one evolving application instead of disconnected demos.
2. Treat model output as untrusted input.
3. Use deterministic code for authorization, validation, and business rules.
4. Introduce testing, security, and observability early.
5. Measure quality instead of judging outputs only by appearance.
6. Keep provider-specific code behind application-owned interfaces.
7. Record failures, tradeoffs, and engineering decisions.
8. Use synthetic data throughout the course.

## Capstone Project

The capstone is a production-style **AI-assisted clinic operations system**.

It is an educational system built entirely with synthetic clinic and patient data. It must not provide medical diagnoses or treatment recommendations.

The application will progressively support:

- Structured patient-intake extraction
- Missing-information detection
- Appointment slot lookup
- Human-approved appointment booking
- Conversation and workflow persistence
- Controlled long-term memory
- Clinic-policy document ingestion
- Permission-aware retrieval-augmented generation
- Evidence-backed answers with citations
- Automated evaluation and release gates
- Adversarial security testing
- Logging, tracing, and operational monitoring
- Background jobs and failure recovery
- Containerized deployment
- Backup, rollback, and recovery procedures

Every module ends with a capstone milestone. Later milestones improve the same system rather than replacing it.

## Technology Direction

The roadmap is provider-neutral and may use multiple implementations where comparison is valuable.

Expected technologies include:

- Python
- TypeScript where appropriate
- PostgreSQL
- `pgvector`
- Docker
- JSON Schema
- Pydantic and/or Zod
- Automated testing
- CI/CD
- Large-language-model and embedding APIs

Specific providers and models may change over time. Application logic should depend on internal interfaces rather than directly depending on one provider throughout the codebase.

---

# Course Roadmap

## Module 1 — AI Application Contracts and Boundaries

This module establishes the application boundary between probabilistic model behavior and deterministic software behavior.

| Lesson | Topic |
|---:|---|
| 1 | Provider-Neutral AI Boundaries, Model Capabilities, Cost, and Latency |
| 2 | Instruction Hierarchy, Context Construction, Ambiguity, and Untrusted Input |
| 3 | Structured Outputs: JSON Schema, Zod/Pydantic, and Runtime Validation |
| 4 | Semantic Validation, Business Rules, Safe Abstention, and Failure Classification |

### Milestone 1 — Architecture and Structured Intake

Build the initial capstone foundation:

- Application skeleton
- Provider interface
- Synthetic clinic configuration
- Structured intake extraction
- Missing-information handling
- Trust-boundary documentation
- Deterministic validation tests

Expected result: the application can convert synthetic intake messages into validated structured data without allowing model output to directly control business logic.

---

## Module 2 — Secure Tools and Stateful Workflows

This module introduces tool calling and safe multi-step actions.

| Lesson | Topic |
|---:|---|
| 5 | Tool Calling, Typed Arguments, and Server-Side Validation |
| 6 | Authorization, Resource Permissions, Confirmation, and Idempotency |
| 7 | Explicit State Machines and Multi-Step AI Workflows |
| 8 | Retry Boundaries, Timeouts, Fallbacks, Compensation, and Recovery |

### Milestone 2 — Human-Approved Appointment Workflow

Add:

- Authorized appointment-slot lookup
- Patient-identity matching
- Explicit booking states
- Human confirmation
- Duplicate-action prevention
- Idempotency keys
- Audit events
- Safe retry behavior
- Compensation for partial failures

Expected result: the system can assist with appointment booking, but deterministic application code retains control of authorization and mutations.

---

## Module 3 — PostgreSQL State, Conversation, and Memory

This module makes the application persistent and multi-user safe.

| Lesson | Topic |
|---:|---|
| 9 | PostgreSQL Data Modeling, Migrations, Tenants, Users, and Audit Records |
| 10 | Conversation State, Context Selection, Summarization, and Token Budgets |
| 11 | Persistent Memory, Provenance, Correction, Deletion, and Retention |
| 12 | Privacy-Aware State Access and Cross-User Isolation Testing |

### Milestone 3 — Persistent Intake and Follow-Up

Add:

- PostgreSQL persistence
- Tenant and user ownership
- Persistent workflow state
- Conversation summaries
- Editable memory
- Memory provenance
- Correction and deletion
- Retention metadata
- Reminder and follow-up drafts
- Resumable review queues
- Cross-user and cross-tenant isolation tests

Expected result: conversations and workflows can be resumed safely without exposing one user’s information to another.

---

## Module 4 — Search and Production RAG

This module introduces document ingestion and grounded retrieval.

| Lesson | Topic |
|---:|---|
| 13 | Embeddings, Vector Similarity, PostgreSQL, and `pgvector` |
| 14 | Document Ingestion, Chunking, Metadata, Versioning, and Deletion |
| 15 | Semantic, Keyword, and Hybrid Search with Permission Filters |
| 16 | Reranking, Context Construction, Evidence, Citations, and Abstention |

### Milestone 4 — Permission-Aware Clinic-Policy RAG

Build:

- Clinic-policy ingestion pipeline
- Versioned document and embedding records
- Chunking and metadata strategy
- Semantic retrieval
- Keyword retrieval
- Hybrid search
- Tenant and permission filtering
- Reranking
- Evidence-aware context construction
- Verifiable citations
- Insufficient-evidence behavior

Expected result: policy answers must be based on accessible source documents and must abstain when evidence is insufficient.

---

## Module 5 — Evaluation and Release Decisions

This module turns AI quality into something measurable and repeatable.

| Lesson | Topic |
|---:|---|
| 17 | Evaluation Goals, Datasets, Failure Categories, and Ground Truth |
| 18 | Retrieval Evaluation: Recall, Precision, MRR, and Failure Analysis |
| 19 | Generation Evaluation: Deterministic, Rubric, Model, and Human Review |
| 20 | Regression Testing, Release Thresholds, and Model Selection Experiments |

### Milestone 5 — Evaluation-Gated Release Candidate

Create:

- Held-out intake dataset
- Retrieval evaluation dataset
- Grounded-generation dataset
- Citation checks
- Abstention cases
- Adversarial cases
- Retrieval evaluation reports
- Generation evaluation reports
- Regression tests
- CI-enforced release thresholds
- Model-selection experiment report

Expected result: model or prompt changes cannot be released solely because a few manually inspected examples appear good.

---

## Module 6 — Security, Privacy, and Human Oversight

This module tests how the application behaves against hostile or unsafe input.

| Lesson | Topic |
|---:|---|
| 21 | Threat Modeling, Assets, Trust Boundaries, Secrets, and Data Minimization |
| 22 | Direct and Indirect Prompt Injection and Untrusted Retrieved Content |
| 23 | Tenant Isolation, Tool Abuse, Sensitive Data, and Adversarial Authorization |
| 24 | Human Oversight, Medical-Scope Boundaries, Auditability, and Red-Team Review |

### Milestone 6 — Security and Safety Gate

Test:

- Direct prompt injection
- Indirect prompt injection
- Malicious retrieved documents
- Cross-user access
- Cross-tenant access
- Unauthorized tool calls
- Unauthorized mutations
- Duplicate actions
- Sensitive-data exposure
- Medical diagnosis and treatment boundaries
- Human-escalation behavior

Document:

- Threat model
- Security controls
- Test results
- Known limitations
- Residual risks
- Required remediation

Expected result: the application fails safely and does not rely on prompts alone for security.

---

## Module 7 — Reliability, Observability, and Performance

This module prepares the application for real operational conditions.

| Lesson | Topic |
|---:|---|
| 25 | Structured Logging, Request IDs, Correlation IDs, Traces, and Error Taxonomy |
| 26 | Latency, Token, Cost, Quality, Error Monitoring, and Alert Design |
| 27 | Caching, Context Reduction, Concurrency, Rate Limits, and Load Testing |
| 28 | Background Jobs, Queues, Idempotent Workers, Dead Letters, and Recovery |

### Milestone 7 — Operational Readiness and Incident Drill

Add:

- Structured logs
- Request and correlation IDs
- Distributed traces
- Classified errors
- Latency monitoring
- Token and cost monitoring
- Quality monitoring
- Alert rules
- Caching
- Context reduction
- Rate-limit handling
- Concurrency controls
- Background reminder processing
- Idempotent workers
- Dead-letter handling
- Failure injection
- Recovery exercise
- Incident report

Expected result: important failures can be detected, understood, retried, and recovered without relying on manual guesswork.

---

## Module 8 — Deployment, Operations, and Portfolio Defense

This module completes the production lifecycle.

| Lesson | Topic |
|---:|---|
| 29 | Docker, Configuration, Secrets, Database Migrations, and Environment Separation |
| 30 | Automated Tests, CI/CD, Staging, and Release Gates |
| 31 | Deployment Verification, Rollback, Backup, and Recovery |
| 32 | Architecture, Security, Evaluation, Operations, and Portfolio Documentation |

### Milestone 8 — Production Release and Final Defense

Complete:

- Containerized application
- Environment-specific configuration
- Secure secret handling
- Automated database migrations
- Automated test pipeline
- Evaluation release gates
- Staging deployment
- Production deployment
- Deployment verification
- Rollback procedure
- Backup procedure
- Recovery exercise
- Architecture documentation
- Security documentation
- Evaluation documentation
- Operations runbook
- Demonstration recording
- Portfolio case study
- Final technical review

Expected result: the application is deployed, documented, recoverable, and explainable as a complete engineering project.

---

# Repository Structure

The repository will use `README.md` only at the root.

```text
.
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── modules/
│   ├── 01-ai-application-contracts/
│   │   ├── MODULE.md
│   │   ├── lesson-01/
│   │   │   ├── LESSON.md
│   │   │   ├── RESULTS.md
│   │   │   └── ASSESSMENT.md
│   │   ├── lesson-02/
│   │   ├── lesson-03/
│   │   ├── lesson-04/
│   │   └── milestone-01/
│   │       └── MILESTONE.md
│   ├── 02-secure-tools-and-workflows/
│   ├── 03-state-conversation-and-memory/
│   ├── 04-search-and-production-rag/
│   ├── 05-evaluation-and-release-decisions/
│   ├── 06-security-privacy-and-oversight/
│   ├── 07-reliability-and-observability/
│   └── 08-deployment-and-portfolio-defense/
├── capstone/
├── docs/
├── src/
├── tests/
├── evaluations/
├── scripts/
└── docker/
```

## Documentation Naming Convention

| File | Purpose |
|---|---|
| `README.md` | Repository introduction and complete roadmap |
| `MODULE.md` | Module objectives, prerequisites, and completion criteria |
| `LESSON.md` | Lesson instructions and exercises |
| `RESULTS.md` | Commands, outputs, measurements, experiments, and observations |
| `ASSESSMENT.md` | Knowledge check, review findings, and completion decision |
| `MILESTONE.md` | Integrated capstone milestone requirements and acceptance criteria |

Additional production documentation will be added as the application develops:

- `ARCHITECTURE.md`
- `SECURITY.md`
- `EVALUATION.md`
- `OPERATIONS.md`

## Lesson Completion Standard

A lesson is complete only when:

1. Required implementation work is finished.
2. Relevant tests pass.
3. Commands and important outputs are recorded.
4. Results are analyzed rather than merely copied.
5. Knowledge-check questions are answered.
6. Known limitations are documented.
7. The lesson’s acceptance criteria are satisfied.
8. Changes are committed to Git.

## Milestone Completion Standard

A milestone may take multiple learning sessions.

Each milestone must provide safe stopping points and must not be considered complete until:

- Required functionality works
- Deterministic tests pass
- Integration tests pass
- Security-sensitive behavior is tested
- Relevant documentation is updated
- Known limitations are recorded
- Acceptance criteria are reviewed

## Evaluation Minimums

Before graduation, the project must include at least:

- 40 intake or generation evaluation cases
- 30 retrieval questions
- 10 insufficient-evidence cases
- 15 security or adversarial cases

Initial release targets include:

- 100% passing critical authorization and safety tests
- `Recall@5 >= 0.90` for the defined retrieval evaluation set
- Verified citations for released evidence-backed answers
- No unsupported policy answers for insufficient-evidence cases
- No successful cross-tenant disclosure
- No unauthorized mutation
- No medical diagnosis or treatment recommendation

Targets may be revised only when the reason and supporting failure analysis are documented.

## Graduation Criteria

To complete this roadmap, I must be able to demonstrate that:

1. All 32 core lessons are complete.
2. All 8 capstone milestones pass their acceptance criteria.
3. The application runs from a clean environment using documented commands.
4. Provider-specific integrations are isolated behind an application-owned interface.
5. Model-derived values affecting business logic pass runtime, semantic, and business validation.
6. Mutating operations require authorization, confirmation, and idempotency protection.
7. Invalid workflow transitions and duplicate actions are rejected deterministically.
8. Conversation state and memory respect user and tenant boundaries.
9. RAG answers are permission-aware, evidence-based, and citation-verified.
10. Insufficient-evidence cases safely abstain.
11. Evaluation thresholds are enforced during CI.
12. Security tests show no cross-tenant disclosure or unauthorized mutation.
13. Provider, parsing, network, timeout, and rate-limit failures have tested safe behavior.
14. Logs and traces expose system behavior without exposing prohibited sensitive data.
15. Deployment, rollback, backup, and recovery procedures have been demonstrated.
16. Architecture, security, evaluation, and operational documentation match the actual implementation.
17. Major engineering decisions and tradeoffs can be explained during a technical review.

## Estimated Duration

| Work | Estimated time |
|---|---:|
| 32 core lessons | 24–32 hours |
| 8 capstone milestones | 14–20 hours |
| Reviews and remediation | 4–8 hours |
| **Required total** | **42–60 hours** |
| Optional extensions | Additional 12–20 hours |

At 30 minutes to 2 hours per day, the expected completion time is approximately 6–8 weeks.

## Data and Privacy Rules

This repository must use synthetic data only.

Do not commit:

- Real patient information
- Real medical records
- API keys
- Database credentials
- Access tokens
- Private certificates
- Production secrets
- Confidential client information

Local secrets must be placed in ignored environment files. A sanitized `.env.example` should document required variables without containing real credentials.

## Current Progress

- [ ] Module 1 — AI Application Contracts and Boundaries
- [ ] Milestone 1 — Architecture and Structured Intake
- [ ] Module 2 — Secure Tools and Stateful Workflows
- [ ] Milestone 2 — Human-Approved Appointment Workflow
- [ ] Module 3 — PostgreSQL State, Conversation, and Memory
- [ ] Milestone 3 — Persistent Intake and Follow-Up
- [ ] Module 4 — Search and Production RAG
- [ ] Milestone 4 — Permission-Aware Clinic-Policy RAG
- [ ] Module 5 — Evaluation and Release Decisions
- [ ] Milestone 5 — Evaluation-Gated Release Candidate
- [ ] Module 6 — Security, Privacy, and Human Oversight
- [ ] Milestone 6 — Security and Safety Gate
- [ ] Module 7 — Reliability, Observability, and Performance
- [ ] Milestone 7 — Operational Readiness and Incident Drill
- [ ] Module 8 — Deployment, Operations, and Portfolio Defense
- [ ] Milestone 8 — Production Release and Final Defense

## Status

The revised roadmap and repository conventions are established.

The next step is:

**Module 1, Lesson 1 — Provider-Neutral AI Boundaries, Model Capabilities, Cost, and Latency**