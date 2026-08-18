# AI Application Engineering Roadmap

A structured, hands-on course for learning how to design, build, evaluate, secure, and deploy production-quality AI applications.

The course uses TypeScript and provider-neutral application architecture. Google Gemini’s free API tier is used by default. OpenAI or another provider may be introduced when a lesson requires capabilities unavailable through Gemini’s free tier.

Provider capabilities, model availability, free-tier access, and expected costs are rechecked at the beginning of relevant lessons.

# Course Structure

The course contains:

- **7 phases**
- **15 numbered modules**
- **75 planned module lessons**
- **8 capstone milestones**
- **83 planned lessons and milestones in total**

Each numbered module contains five planned lessons. Supplemental remediation may be added when an assessment identifies an area requiring more practice.

# Phase 1 — Foundations

## Module 1 — How Production LLM Applications Work

Learn how model requests behave and how to observe, validate, and evaluate basic AI operations.

| Lesson | Topic |
|---|---|
| 1 | Anatomy of a Production LLM Request |
| 2 | Reliable Structured Outputs and Validation |
| 3 | Tokens, Context Windows, Latency, and Cost |
| 4 | Probabilistic Behavior, Hallucinations, and Failure Modes |
| 5 | Reliability Lab and Module Assessment |

Topics include:

- Models and model capabilities
- Inputs, instructions, and generated outputs
- Tokens and token usage
- Context windows and context limits
- Latency measurement
- API cost estimation
- Probabilistic generation
- Deterministic application logic
- Model strengths and limitations
- Hallucinations
- Common AI failure modes
- Minimal TypeScript AI applications
- Structured logging
- Token-usage monitoring
- Error recording
- Output-quality assessment

Module 1 introduces structured outputs early because they provide a practical foundation for validation. Module 3 revisits structured outputs at a deeper production level.

## Module 2 — Prompt and Context Engineering

Learn how to construct reliable instructions and provide models with the right information while treating external content as untrusted data.

| Lesson | Topic |
|---|---|
| 1 | Instruction Hierarchy and Prompt Anatomy |
| 2 | Reusable Prompt Templates and Ambiguity Handling |
| 3 | Few-Shot Examples and Behavioral Guidance |
| 4 | Context Selection and Untrusted-Data Separation |
| 5 | Prompt Injection Lab and Prompt Evaluation |

Topics include:

- Instruction hierarchy
- System instructions
- Developer and application instructions
- User instructions
- Separating instructions from user-provided content
- Treating retrieved content as untrusted data
- Reusable prompt templates
- Variable interpolation
- Clear task definitions
- Output requirements
- Few-shot examples
- Positive and negative examples
- Context selection
- Context relevance
- Context ordering
- Handling ambiguous requests
- Asking clarification questions
- Avoiding unsupported assumptions
- Introductory prompt-injection defense
- Small prompt test datasets
- Prompt regression testing

## Module 3 — Production Structured Outputs

Design typed AI interfaces that remain reliable when outputs are malformed, incomplete, or semantically incorrect.

| Lesson | Topic |
|---|---|
| 1 | JSON Schema and Response-Schema Design |
| 2 | Constrained Generation and Zod Validation |
| 3 | Semantic Validation and Business Rules |
| 4 | Invalid Outputs, Retries, and Fallbacks |
| 5 | Structured-Output Test Harness and Assessment |

Topics include:

- JSON output
- JSON Schema
- Supported schema types
- Required and optional fields
- Nullable values
- Enumerations
- Nested objects and arrays
- Constrained generation
- Zod validation
- TypeScript type inference
- Response-schema design
- Schema evolution
- Backward compatibility
- Syntactic validation
- Schema validation
- Semantic validation
- Business-rule validation
- Invalid-output handling
- Parse failures
- Missing-field handling
- Retry strategies
- Repair attempts
- Fallback behavior
- Safe failure responses
- Automated structured-output tests
- Adversarial test cases

# Phase 2 — Tools and Workflows

## Module 4 — Tool and Function Calling

Connect models to application capabilities without giving the model unrestricted authority.

| Lesson | Topic |
|---|---|
| 1 | Structured Outputs Versus Tool Calling |
| 2 | Typed Tool Definitions and Argument Validation |
| 3 | Executing Tools and Returning Results |
| 4 | Authorization, Idempotency, and Safe Actions |
| 5 | Secure Tool-Calling Lab and Assessment |

Topics include:

- Structured outputs versus tool calling
- Tool and function definitions
- Tool descriptions
- Typed parameters
- Required and optional arguments
- Argument-schema design
- Tool selection
- Tool-call parsing
- Server-side validation
- Business-rule validation
- Tool execution
- Returning tool results to the model
- Multi-tool requests
- Parallel tool calls
- Tool authorization
- User-level permissions
- Resource-level permissions
- Preventing unauthorized actions
- Idempotency
- Duplicate-call prevention
- Confirmation requirements
- Read-only versus mutating tools
- Audit logging
- Tool errors and safe recovery

## Module 5 — Multi-Step AI Workflows

Combine deterministic application logic with probabilistic AI operations through explicit workflow orchestration.

| Lesson | Topic |
|---|---|
| 1 | Deterministic and Probabilistic Workflow Steps |
| 2 | State Machines for AI Applications |
| 3 | Multi-Step Orchestration and Data Flow |
| 4 | Retries, Compensation, and Human Checkpoints |
| 5 | Workflow Reliability Lab and Assessment |

Topics include:

- Single-step versus multi-step operations
- Deterministic workflow steps
- Probabilistic workflow steps
- Explicit workflow states
- State machines
- Valid state transitions
- Invalid transition prevention
- Workflow orchestration
- Passing validated data between steps
- Conditional branches
- Parallel operations
- Sequential dependencies
- Multi-stage validation
- Retry boundaries
- Partial failure handling
- Compensation actions
- Rollback strategies
- Recovery paths
- Timeouts
- Workflow cancellation
- Human approval checkpoints
- Resumable workflows
- Workflow audit history

## Module 6 — Conversation State and Memory

Manage conversation history and persistent memory without creating privacy, accuracy, or isolation problems.

| Lesson | Topic |
|---|---|
| 1 | Short-Term Conversation State |
| 2 | Persistent Memory and Data Modeling |
| 3 | Context Summarization and Token Budgets |
| 4 | Privacy, Retention, and Cross-User Isolation |
| 5 | Stateful Assistant Lab and Assessment |

Topics include:

- Conversation messages
- Conversation identifiers
- Short-term state
- Persistent application state
- Persistent memory
- Session state
- Database-backed memory
- Memory data models
- Context-window limits
- Context summarization
- Summary accuracy
- Token budgets
- Selecting relevant history
- Removing irrelevant history
- User-editable memory
- Memory correction
- Memory deletion
- Data-retention policies
- Privacy controls
- User consent
- Cross-user information leakage
- Tenant isolation
- Stale-memory handling
- Conflicting-memory resolution

# Phase 3 — Retrieval and RAG

## Module 7 — Embeddings and Semantic Search

Represent content as vectors and retrieve relevant information using semantic similarity.

| Lesson | Topic |
|---|---|
| 1 | Embeddings and Vector Similarity |
| 2 | Document Chunking and Metadata |
| 3 | PostgreSQL and `pgvector` |
| 4 | Semantic, Keyword, and Hybrid Search |
| 5 | Search Quality Lab and Assessment |

Topics include:

- Embedding models
- Embedding dimensions
- Vector representations
- Similarity measures
- Cosine similarity
- Semantic similarity
- Document preparation
- Document chunking
- Chunk size
- Chunk overlap
- Metadata design
- PostgreSQL
- `pgvector`
- Vector columns
- Vector indexes
- Similarity queries
- Metadata filtering
- Access-control filtering
- Semantic search
- Keyword search
- Hybrid search
- Result ranking
- Search relevance
- Empty-result handling

## Module 8 — Production RAG Pipelines

Build retrieval-augmented generation pipelines that produce evidence-backed answers from controlled information sources.

| Lesson | Topic |
|---|---|
| 1 | Document Ingestion and Indexing |
| 2 | Retrieval and Context Construction |
| 3 | Reranking and Relevance Improvement |
| 4 | Evidence-Backed Answers and Citations |
| 5 | Production RAG Pipeline Lab and Assessment |

Topics include:

- Retrieval-augmented generation
- Document ingestion
- File parsing
- Text normalization
- Chunking strategies
- Embedding generation
- Indexing
- Source metadata
- Document versioning
- Retrieval queries
- Query transformation
- Metadata filtering
- Permission-aware retrieval
- Context construction
- Context ordering
- Context-size management
- Reranking
- Relevance scoring
- Evidence-backed generation
- Source attribution
- Inline citations
- Citation metadata
- Insufficient-evidence responses
- Unsupported-claim prevention
- Updating indexed content
- Deleting indexed content
- Re-embedding changed documents
- Multi-tenant RAG isolation

## Module 9 — Retrieval Evaluation

Measure whether a retrieval system finds the correct evidence and whether the generated answer remains grounded in it.

| Lesson | Topic |
|---|---|
| 1 | Building Retrieval Evaluation Datasets |
| 2 | Recall, Precision, and Relevance Metrics |
| 3 | Groundedness and Citation Correctness |
| 4 | Retrieval Failure Analysis and Tuning |
| 5 | RAG Evaluation Lab and Assessment |

Topics include:

- Retrieval evaluation datasets
- Representative user questions
- Expected source documents
- Relevant-chunk labeling
- Recall
- Precision
- Precision at K
- Recall at K
- Mean reciprocal rank
- Relevance evaluation
- Retrieval coverage
- Groundedness
- Faithfulness
- Citation correctness
- Citation completeness
- Unsupported-answer detection
- No-answer evaluation
- Retrieval failure categories
- Chunking failure analysis
- Metadata-filter failure analysis
- Query-transformation evaluation
- Reranking evaluation
- Retrieval tuning
- Regression testing

# Phase 4 — Evaluation and Reliability

## Module 10 — AI Evaluation Systems

Create repeatable methods for determining whether an AI feature is ready for production.

| Lesson | Topic |
|---|---|
| 1 | Evaluation Goals, Datasets, and Acceptance Criteria |
| 2 | Deterministic Checks and Rubric-Based Evaluation |
| 3 | Model-Based Evaluators and Human Review |
| 4 | Regression Testing and Release Thresholds |
| 5 | Automated Evaluation Harness and Assessment |

Topics include:

- Evaluation goals
- Quality dimensions
- Task-specific quality criteria
- Golden datasets
- Representative test cases
- Edge cases
- Adversarial cases
- Deterministic checks
- Schema checks
- Keyword and pattern checks
- Business-rule checks
- Rubric-based evaluation
- Model-based evaluators
- Evaluator prompts
- Evaluator bias
- Human evaluation
- Inter-rater agreement
- Error categorization
- Prompt comparison
- Model comparison
- A/B evaluation
- Regression testing
- Baseline results
- Release acceptance thresholds
- Quality gates
- Evaluation reports

## Module 11 — Failure Handling and Observability

Detect, classify, investigate, and recover from API failures, quality failures, and workflow failures.

| Lesson | Topic |
|---|---|
| 1 | Structured Logging and Distributed Tracing |
| 2 | AI Error Taxonomy and Failure Classification |
| 3 | Timeouts, Retries, and Exponential Backoff |
| 4 | Fallback Models, Circuit Breakers, and Recovery |
| 5 | Production Incident Lab and Assessment |

Topics include:

- Structured logging
- Request identifiers
- Correlation identifiers
- Distributed tracing
- Workflow spans
- Model-call spans
- Token-usage logging
- Latency monitoring
- Cost monitoring
- API failures
- Authentication failures
- Rate limits
- Timeouts
- Network failures
- Invalid responses
- Schema failures
- Semantic failures
- Quality failures
- Business-rule failures
- Retry classification
- Exponential backoff
- Jitter
- Retry limits
- Model fallbacks
- Provider fallbacks
- Circuit breakers
- Graceful degradation
- Dead-letter handling
- Alerting
- Production incident investigation
- Root-cause analysis
- Recovery verification

# Phase 5 — Security and Responsible Design

## Module 12 — AI Application Security

Protect AI systems from malicious instructions, unauthorized actions, sensitive-data exposure, and tenant-isolation failures.

| Lesson | Topic |
|---|---|
| 1 | Threat Modeling for AI Applications |
| 2 | Prompt Injection and Untrusted Content |
| 3 | Tool Authorization and Action Security |
| 4 | Data Isolation, Secrets, and Sensitive Information |
| 5 | AI Security Red-Team Lab and Assessment |

Topics include:

- AI threat modeling
- Assets and trust boundaries
- Attack surfaces
- Prompt injection
- Direct prompt injection
- Indirect prompt injection
- Untrusted retrieved content
- Malicious documents
- Instruction-data separation
- Input validation
- Output validation
- Tool argument validation
- Tool authorization
- Resource-level permissions
- Least-privilege access
- Read-only versus mutating operations
- Human approval for sensitive actions
- Data isolation
- Tenant isolation
- Cross-user data leakage
- Secret management
- Environment variables
- Sensitive-data handling
- Logging redaction
- Abuse prevention
- Rate limiting
- Security testing
- Red-team scenarios

## Module 13 — Human Oversight and Responsible Design

Design systems that keep people in control of sensitive, consequential, or irreversible operations.

| Lesson | Topic |
|---|---|
| 1 | Human-in-the-Loop Approval Patterns |
| 2 | Reversible and Irreversible Actions |
| 3 | Privacy, Retention, and Audit Records |
| 4 | Escalation, Disclosure, and AI Limitations |
| 5 | Responsible Design Review and Assessment |

Topics include:

- Human-in-the-loop design
- Approval queues
- Confirmation interfaces
- Human review
- Reversible actions
- Irreversible actions
- Consequence-based approval
- Escalation rules
- Escalation thresholds
- Manual overrides
- Safe defaults
- Privacy
- User consent
- Data minimization
- Data retention
- Data deletion
- Audit records
- Decision history
- AI disclosure
- Communicating uncertainty
- Communicating AI limitations
- Responsible automation
- Safe administrative assistance
- Preventing unsupported clinical advice
- Avoiding medical diagnosis
- Professional-review requirements

# Phase 6 — Production Engineering

## Module 14 — Performance and Cost Engineering

Improve response time and control operational costs without silently reducing application quality.

| Lesson | Topic |
|---|---|
| 1 | Model Selection and Token Budgeting |
| 2 | Context Reduction and Caching |
| 3 | Concurrency, Queues, and Batch Processing |
| 4 | Cost Monitoring and Quality Trade-Offs |
| 5 | Performance Optimization Lab and Assessment |

Topics include:

- Model selection
- Capability requirements
- Latency requirements
- Cost requirements
- Quality requirements
- Token budgeting
- Input-token reduction
- Output-token limits
- Context reduction
- Context compression
- Prompt optimization
- Reusable instructions
- Response caching
- Embedding caching
- Context caching
- Cache invalidation
- Concurrency
- Parallel requests
- Request queues
- Background jobs
- Batch processing
- Rate-limit management
- Throughput measurement
- Latency measurement
- Cost monitoring
- Cost allocation
- Per-feature cost tracking
- Quality-versus-cost trade-offs
- Performance benchmarking
- Load testing

## Module 15 — Deployment and Operations

Deploy and operate an AI application using production infrastructure and recoverable release practices.

| Lesson | Topic |
|---|---|
| 1 | Production Architecture and Environment Configuration |
| 2 | PostgreSQL, Persistence, and Database Migrations |
| 3 | Docker, Background Workers, and Queues |
| 4 | Automated Testing and CI/CD |
| 5 | Monitoring, Deployment, Rollback, and Assessment |

Topics include:

- Production application architecture
- TypeScript backend integration
- API boundaries
- Provider-neutral interfaces
- Environment configuration
- Secret management
- Development environments
- Staging environments
- Production environments
- PostgreSQL
- Database persistence
- Database migrations
- Migration safety
- Connection management
- Docker
- Container configuration
- Background workers
- Job queues
- Scheduled jobs
- Automated testing
- Unit tests
- Integration tests
- End-to-end tests
- CI/CD
- Build pipelines
- Deployment pipelines
- Health checks
- Monitoring
- Alerts
- Error tracking
- Operational dashboards
- Rollback procedures
- Database rollback considerations
- Backup and recovery
- Disaster recovery
- Deployment verification
- Production-readiness reviews

# Phase 7 — Capstone

## Production AI-Assisted Administrative Application

The preferred capstone is an **AI-assisted clinic administration and patient-intake system**.

The application is explicitly administrative. It must not diagnose conditions, recommend clinical treatments, or replace professional medical judgment.

| Milestone | Topic |
|---|---|
| 1 | Requirements, Architecture, and Threat Model |
| 2 | Application Foundation and PostgreSQL Data Model |
| 3 | Structured Patient Intake and Missing-Information Detection |
| 4 | Clinic-Policy RAG with Evidence and Citations |
| 5 | Authorized Scheduling Tools and Human-Approved Booking |
| 6 | Evaluation, Security Testing, and Failure Handling |
| 7 | Docker Deployment, Monitoring, and Operational Readiness |
| 8 | Documentation, Demonstration, and Portfolio Case Study |

Potential application capabilities include:

- Structured patient-intake extraction
- Missing-information detection
- Inquiry classification
- Non-clinical inquiry summaries
- Evidence-backed clinic-policy answers
- Clinic-policy RAG
- Source citations
- Authorized appointment-slot lookup
- Patient-identity matching
- Human-approved appointment booking
- Duplicate-booking prevention
- Reminder drafts
- Follow-up drafts
- Escalation workflows
- Human-review queues
- Audit records
- Request tracing
- Latency tracking
- Token-usage tracking
- Cost tracking
- Error monitoring

The completed capstone must demonstrate:

- Typed and validated model outputs
- Structured-output schemas
- Business-rule validation
- Secure tool execution
- Tool authorization
- PostgreSQL persistence
- Conversation or workflow state
- Evaluated retrieval
- Evidence-backed responses
- Citation verification
- Human approval for meaningful actions
- Prompt-injection defenses
- Tenant and user isolation
- Sensitive-data protection
- Structured logging
- Distributed tracing
- Latency and cost monitoring
- Failure recovery
- Automated tests
- Docker deployment
- CI/CD
- Technical documentation
- Architecture documentation
- Security documentation
- Evaluation results
- A portfolio-ready case study

# Lesson Format

Every lesson follows the same structure:

- **Required core:** approximately 30 minutes
- **Optional extension:** up to approximately 60 minutes
- **Optional deep work:** up to approximately 120 minutes
- Only one lesson is active at a time
- Missed days resume the current lesson
- No artificial catch-up lessons are created
- Progress continues after submission, review, and explicit completion

The required 30-minute core is designed to be independently valuable. Optional extensions provide additional implementation, testing, evaluation, and production-hardening work.

# Assessment and Review

Each major phase may include:

- A conceptual assessment
- A practical implementation exercise
- A debugging scenario
- A testing or evaluation exercise
- Deliverable review
- Identification of weak areas
- Supplemental remediation when needed

A typical learning rhythm includes:

1. Concept introduction
2. Guided implementation
3. Independent application
4. Failure analysis and debugging
5. Testing and evaluation
6. Project integration
7. Review or catch-up

# Repository Structure

```text
modules/
├── 01-llm-foundations/
│   ├── lesson-01/
│   ├── lesson-02/
│   └── ...
├── 02-prompt-context-engineering/
├── 03-structured-outputs/
├── 04-tool-calling/
├── 05-multi-step-workflows/
├── 06-conversation-state-memory/
├── 07-embeddings-semantic-search/
├── 08-production-rag/
├── 09-retrieval-evaluation/
├── 10-ai-evaluation-systems/
├── 11-failure-handling-observability/
├── 12-ai-application-security/
├── 13-human-oversight/
├── 14-performance-cost/
├── 15-deployment-operations/
└── capstone/
```

Each completed lesson generally contains:

```text
lesson-XX/
├── src/
│   └── index.ts
├── README.md
├── results.md
├── package.json
├── package-lock.json
└── tsconfig.json
```

API keys, environment files, generated dependencies, logs, and build outputs must not be committed.