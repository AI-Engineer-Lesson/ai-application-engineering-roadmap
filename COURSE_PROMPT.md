I want to restart and redesign my AI Application Engineering learning roadmap from the beginning.

My primary goal is to become genuinely production-ready as quickly as reasonably possible while keeping the curriculum comprehensive. Do not make it artificially short by removing essential production topics. Instead, reduce repetition, combine closely related concepts, and teach concepts through integrated projects.

## My Background

I am a software engineer with approximately two years of professional experience.

My experience includes:

- Full-stack and backend development
- PHP and Laravel
- React and TypeScript
- Next.js and TypeScript
- ASP.NET and C#
- PostgreSQL
- MariaDB
- Prisma
- Docker
- REST APIs
- Business systems
- Direct client communication
- Agentic coding using OpenAI Codex

Treat me as an experienced application developer learning AI engineering—not as a beginner programmer.

I am relatively new to Python, so introduce Python concepts clearly when they first appear, preferably with brief TypeScript comparisons. Do not over-explain general software-engineering concepts I should already understand.

## Existing Repository

GitHub repository:

https://github.com/AI-Engineer-Lesson/ai-application-engineering-roadmap

The existing roadmap contains 83 planned lessons and milestones, which is more time than I want to spend.

I previously completed Lessons 1–8, but I am willing to restart, renumber, replace, archive, or consolidate them. Inspect the repository before designing the replacement roadmap.

Reuse anything valuable, but do not preserve the existing structure merely for consistency.

Do not delete or overwrite prior work without first recommending a safe migration or archival approach and receiving my approval.

## Primary Goal

Create the shortest roadmap that still provides comprehensive, production-relevant AI application engineering competency.

Optimize for:

- Complete production coverage
- Minimal repetition
- Strong practical ability
- Progressive project development
- Efficient use of time
- Portfolio value
- Job readiness

Do not optimize for the smallest possible lesson count if doing so would make lessons overloaded or superficial.

Do not expand the roadmap merely to give every concept its own lesson. Combine concepts that naturally belong in the same implementation.

## Time and Pace

I can study for approximately 30 minutes to 2 hours daily.

Design each session with:

- A required 30–60 minute core
- Optional extension work when I have more time
- Occasional longer implementation or assessment sessions when genuinely necessary
- Clear stopping points so a longer lesson can be continued safely

I want a roadmap that can realistically be completed in approximately 5–8 weeks with consistent daily work.

You may recommend a different duration if you can justify it based on production-readiness requirements.

Do not choose an arbitrary lesson count first. Determine the minimum number of well-designed sessions required to achieve the production outcome.

## Required Final Outcome

By the end, I should be able to independently design, build, test, secure, deploy, monitor, maintain, and explain a production-quality AI application.

The completed roadmap and capstone must demonstrate:

- Provider-neutral AI integration boundaries
- Model selection based on capability, cost, and latency
- Prompt and context engineering
- Instruction hierarchy
- Untrusted-input separation
- Ambiguity handling
- Structured outputs
- JSON Schema or equivalent schema design
- Runtime schema validation
- Semantic validation
- Business-rule validation
- Tool and function calling
- Server-side tool-argument validation
- Authorization and least privilege
- Resource-level permissions
- Idempotency
- Duplicate-action prevention
- Read-only versus mutating operations
- Confirmation requirements
- Multi-step workflows
- Explicit workflow states
- State machines
- Valid state transitions
- Retry boundaries
- Timeouts
- Fallbacks
- Compensation and recovery
- Human checkpoints
- Conversation state
- Persistent memory
- Memory correction and deletion
- Context summarization
- PostgreSQL persistence
- Embeddings
- Vector similarity
- Document chunking
- Metadata design
- PostgreSQL with `pgvector`
- Semantic search
- Keyword search
- Hybrid search
- Production RAG
- Permission-aware retrieval
- Context construction
- Reranking
- Evidence-backed answers
- Citation verification
- Insufficient-evidence handling
- Retrieval evaluation
- Generation evaluation
- Evaluation datasets
- Deterministic checks
- Rubric-based evaluation
- Model-based evaluation where appropriate
- Human evaluation
- Regression testing
- Release thresholds
- Prompt-injection defenses
- Direct and indirect prompt injection
- Untrusted retrieved-content handling
- Sensitive-data protection
- Tenant isolation
- User isolation
- Privacy and data minimization
- Retention and deletion policies
- Human approval for sensitive actions
- Audit trails
- Structured logging
- Request and correlation identifiers
- Distributed tracing
- Error classification
- Latency monitoring
- Token monitoring
- Quality monitoring
- Cost monitoring
- Caching
- Performance optimization
- Concurrency
- Background jobs or queues
- Rate-limit handling
- Docker
- Automated tests
- CI/CD
- Staging and production configuration
- Deployment verification
- Monitoring and alerting
- Rollback
- Backup and recovery considerations
- Technical documentation
- Architecture documentation
- Security documentation
- Evaluation documentation
- A strong portfolio-ready case study

## Meaning of Production-Ready

Do not use “production-ready” to mean that I have merely seen every topic once.

Graduation should require evidence that I can:

1. Build the complete application.
2. Explain its architecture and trust boundaries.
3. Validate model output before it affects business logic.
4. Prevent unauthorized or duplicate tool actions.
5. Evaluate retrieval and generation independently.
6. Detect and safely handle insufficient evidence.
7. Defend against common prompt-injection scenarios.
8. Preserve tenant and user isolation.
9. Recover from provider, network, parsing, and workflow failures.
10. Monitor quality, latency, token usage, errors, and cost.
11. Deploy the system through a repeatable process.
12. Demonstrate automated tests and release checks.
13. Document limitations and operational procedures.
14. Defend major engineering decisions during a final review.

Be realistic: completing the roadmap should make me capable of developing and contributing to production AI applications. It does not need to imply mastery of every AI framework, research topic, or enterprise-scale infrastructure system.

## Progressive Capstone

Use one progressive capstone throughout the roadmap rather than waiting until the final phase to begin it.

Preferred capstone:

**A production AI-assisted clinic administration and patient-intake system**

It must remain administrative and must not:

- Diagnose conditions
- Recommend clinical treatments
- Replace professional medical judgment
- Automatically make consequential clinical decisions

Potential capabilities include:

- Structured patient-intake extraction
- Missing-information detection
- Ambiguity handling
- Non-clinical inquiry classification
- Clinic-policy RAG
- Evidence-backed answers with citations
- Citation verification
- Authorized appointment-slot lookup
- Patient-identity matching
- Human-approved appointment booking
- Duplicate-booking prevention
- Reminder drafts
- Follow-up drafts
- Escalation workflows
- Human-review queues
- Persistent workflow state
- Audit logs
- Evaluation reports
- Request tracing
- Token and latency tracking
- Cost monitoring
- Error monitoring
- Operational dashboards

Use synthetic data only during lessons.

Build the capstone incrementally. Each major topic should improve the same application rather than producing an unrelated throwaway project whenever practical.

Small isolated exercises are acceptable when they teach a concept more clearly, but the knowledge should later be integrated into the capstone.

## Technology Preferences

Choose technology based on practical value:

- Use Python for AI, evaluation, retrieval, data processing, and automation where it provides a real advantage.
- Use TypeScript for Next.js, APIs, application integration, and typed business logic where appropriate.
- Use PostgreSQL and `pgvector` for persistence and retrieval.
- Use Zod or an appropriate Python equivalent for runtime validation.
- Use Docker.
- Prefer current, official SDK patterns and production-supported APIs.
- Verify time-sensitive technical details against official documentation before creating lessons.
- Prefer primary and official technical sources.
- Prefer Gemini’s available free-tier model for experiments.
- Allow a documented fallback model when the preferred model’s free quota is exhausted.
- Use the same model throughout an individual controlled comparison.
- Avoid unnecessary API calls when deterministic local tests can teach the concept.
- Do not require paid infrastructure until it is genuinely necessary.
- Clearly distinguish provider-specific code from provider-neutral application architecture.
- Avoid unnecessary frameworks that hide the underlying concepts before I understand them.

## Teaching Style

Make the course:

- Practical
- Technically rigorous
- Concise
- Production-oriented
- Active rather than lecture-heavy
- Suitable for an experienced software engineer
- Honest about deterministic and probabilistic behavior
- Clear about security, reliability, and operational tradeoffs

Prioritize:

- Implementation
- Experimentation
- Debugging
- Testing
- Failure analysis
- Retrieval practice
- Explaining concepts in my own words
- Production decision-making
- Tradeoff analysis
- Safe failure behavior
- Reviewing actual repository work

Avoid:

- Bloated lectures
- Excessive repetition
- Toy examples with no production relevance
- Framework memorization without underlying understanding
- Overclaiming what a small experiment proves
- Accepting successful output without validating it
- Treating prompt instructions as security controls
- Giving me completed solutions for every required task

Do not accept shallow answers such as “not sure” as lesson completion. Explain the missing concept and require me to correct the answer.

Minor writing or style problems should not block lesson completion unless they make the technical meaning incorrect or unclear.

## Repository Documentation Convention

Only the repository root may contain a file named:

```text
README.md
```

Do not create `README.md` files inside module, lesson, capstone, or milestone directories.

Use role-based filenames so their purpose is clear.

Recommended structure:

```text
README.md
modules/
├── 01-example-module/
│   ├── MODULE.md
│   ├── ASSESSMENT.md
│   ├── lesson-01/
│   │   ├── INSTRUCTIONS.md
│   │   ├── RESULTS.md
│   │   ├── LESSON.md
│   │   ├── requirements.txt
│   │   ├── package.json
│   │   └── src/
│   └── lesson-02/
│       ├── INSTRUCTIONS.md
│       ├── RESULTS.md
│       ├── LESSON.md
│       └── src/
└── 02-another-module/
    ├── MODULE.md
    ├── ASSESSMENT.md
    └── lesson-03/
        ├── INSTRUCTIONS.md
        ├── RESULTS.md
        ├── LESSON.md
        └── src/

capstone/
├── CAPSTONE.md
├── ARCHITECTURE.md
├── SECURITY.md
├── EVALUATION.md
├── OPERATIONS.md
└── milestones/
    └── milestone-01/
        ├── INSTRUCTIONS.md
        ├── RESULTS.md
        └── MILESTONE.md
```

Not every lesson needs both `requirements.txt` and `package.json`. Include only the files appropriate for that lesson’s technology.

## File Responsibilities

### Root `README.md`

The root `README.md` is the repository’s primary entry point.

It should contain:

- Roadmap purpose
- Intended learner
- Prerequisites
- Complete module and lesson outline
- Capstone outline
- Current progress
- Technology overview
- Setup guidance
- Repository-navigation guidance
- Completion and graduation criteria

### `MODULE.md`

Each module’s `MODULE.md` should contain:

- Module purpose
- Production relevance
- Prerequisites
- Required competencies
- Lesson sequence
- Connection to the capstone
- Module completion criteria
- Current progress

### `INSTRUCTIONS.md`

Each lesson’s `INSTRUCTIONS.md` contains the complete active lesson:

- Concepts
- Implementation requirements
- Starter code
- TODOs
- Experiments
- Tests
- Required questions
- Completion criteria
- Submission instructions

### `RESULTS.md`

Each lesson’s `RESULTS.md` contains:

- Actual experiment outputs
- Test results
- Evaluation tables
- Observations
- Reflections
- Knowledge-check answers
- Deviations from the lesson
- Model and environment information
- Known limitations

### `LESSON.md`

Each lesson’s `LESSON.md` is the permanent summary created only after the lesson passes review.

It should contain:

- What was built
- Concepts learned
- Important implementation details
- Experiment findings
- Corrected conclusions
- Production implications
- Setup and run instructions
- Limitations
- Relationship to the capstone

Do not create `LESSON.md` before the lesson passes.

### `ASSESSMENT.md`

Each module’s `ASSESSMENT.md` contains:

- Assessment tasks
- Review criteria
- Test results
- Identified gaps
- Required remediation
- Final completion decision

### Capstone Documentation

Use:

- `CAPSTONE.md` for requirements, scope, progress, and demonstration guidance
- `ARCHITECTURE.md` for system design and important decisions
- `SECURITY.md` for threat models, trust boundaries, defenses, and residual risks
- `EVALUATION.md` for datasets, metrics, results, and release thresholds
- `OPERATIONS.md` for deployment, monitoring, alerts, rollback, backup, and recovery
- `MILESTONE.md` for the permanent summary of a passed capstone milestone

## Lesson Workflow

For every lesson:

1. Give me the complete active lesson as one copy-ready `INSTRUCTIONS.md` block.
2. Do not place conversational explanations inside the block.
3. Include a complete copy-ready `RESULTS.md` template inside the instructions.
4. I implement the lesson and complete `RESULTS.md`.
5. I commit and push the work to GitHub.
6. I say: “Done. Please check Lesson X.”
7. Inspect the actual repository implementation, outputs, answers, and file hygiene.
8. Clearly separate blocking corrections from optional cleanup.
9. Do not consume additional AI API quota merely to review already recorded results unless rerunning is technically necessary.
10. Require corrections for conceptual or implementation errors.
11. After the lesson passes, generate the final copy-ready `LESSON.md`.
12. Update module progress when appropriate.
13. At the end of a module, conduct the assessment recorded in `ASSESSMENT.md`.

Each `INSTRUCTIONS.md` should include:

- Lesson number, module, and title
- Production relevance
- Estimated required duration
- Optional extension duration
- Specific learning objectives
- Prerequisites when needed
- Necessary terminology
- Concise concept explanations
- A concrete implementation
- Starter code with meaningful TODOs
- Experiments or deterministic tests
- Expected conceptual behavior
- A complete `RESULTS.md` template
- Reflection questions
- Knowledge checks with sufficient context
- Completion criteria
- Common mistakes
- Production concerns
- Optional extensions
- Clear submission instructions

Do not generate `LESSON.md` until the implementation and `RESULTS.md` pass review.

## Exercise Design

Do not make lessons simple copy-paste exercises.

Starter code may provide:

- Boilerplate
- New-language syntax
- Interfaces
- Test structure
- Safe configuration
- Comments explaining unfamiliar concepts

Required TODOs should make me implement or reason about the central lesson concepts.

When Python is introduced, explain unfamiliar syntax such as:

- Type hints
- Collections
- Comprehensions
- Dataclasses
- Exceptions
- Context managers
- Async behavior
- Package management

Use concise TypeScript comparisons where they improve understanding.

Do not repeatedly explain Python concepts that I have already demonstrated correctly.

## Assessment Approach

Use multiple forms of evidence:

- Deterministic tests
- Schema checks
- Business-rule tests
- Adversarial cases
- Failure injection
- Retrieval metrics
- Groundedness checks
- Citation checks
- Manual review
- Architecture explanation
- Security review
- Operational-readiness review

A successful API response does not automatically mean a lesson passes.

Evaluate:

- Implementation correctness
- Conceptual understanding
- Safe behavior
- Failure handling
- Test quality
- Production reasoning
- Accuracy of conclusions

## Roadmap Design Requirements

When redesigning the roadmap:

1. Cover every required production competency.
2. Combine related concepts where this improves learning efficiency.
3. Avoid repeating the same concept across multiple lessons without meaningful added depth.
4. Integrate module assessments into practical implementation where possible.
5. Start the capstone early.
6. Extend the capstone throughout the roadmap.
7. Identify dependencies between lessons.
8. Mark which lessons are essential and which extensions are optional.
9. Include periodic integration and remediation checkpoints.
10. Reserve sufficient time for security, evaluation, deployment, and operations.
11. Include portfolio preparation and technical explanation.
12. Define objective graduation criteria.
13. Provide an estimated completion time based on 30 minutes to 2 hours per day.
14. State the exact planned number of lessons and capstone milestones.
15. Explain why that number is sufficient without being unnecessarily long.

Do not assume the previously suggested 44-session structure is automatically correct. Recalculate the appropriate structure from the required competencies.

## Migration Requirements

Inspect the existing repository before recommending changes.

Classify existing material as:

- Reusable without modification
- Reusable with updates
- Valuable as archived prior work
- Redundant
- Technically outdated
- Incorrectly sequenced
- Missing production depth

Recommend a safe migration plan.

Prefer preserving prior work in an archive or clearly named legacy directory rather than deleting it.

Do not move, rename, archive, delete, or overwrite repository content until I explicitly approve the migration.

## First Task

Do not immediately generate Lesson 1.

First:

1. Inspect the existing GitHub repository.
2. Review the existing root roadmap and completed lessons.
3. Identify what is valuable, redundant, missing, misplaced, outdated, or too repetitive.
4. Design a new accelerated production-ready roadmap.
5. State the exact number of core lessons.
6. State the exact number of integrated capstone milestones.
7. Estimate the completion time.
8. Map every required production competency to specific lessons or milestones.
9. Explain how the capstone will grow throughout the roadmap.
10. Define objective graduation criteria.
11. Recommend how to preserve or migrate the existing work.
12. Present the complete revised roadmap for my review.
13. Wait for my approval before modifying the repository or generating the new Lesson 1.

Only generate the new Lesson 1 after I approve the roadmap.
