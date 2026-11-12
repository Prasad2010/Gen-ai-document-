GENERIC AGENTIC AI
VARIANCE ANALYSIS PLATFORM
Solution architecture, user experience, analytical approach and one-week proof of concept

Executive recommendation
Build a configurable variance analysis platform with a reusable analytical engine and product-specific adapters. Use Python and statistical methods for calculations, an agentic orchestrator to plan and run investigations, and an LLM to explain evidence-backed findings. Start with the known Loans use case; do not hardcode the platform to loans.


Prepared as a solution concept


1. Executive summary
The objective is to automate and standardise the work performed by financial analysts during variance analysis. The platform should compare entities or reporting periods, identify material contributors, investigate underlying drivers, detect unusual movements and produce explanations that analysts can validate.
The first known methodology is for Loans. Other products and their business methodologies have not yet been confirmed with the data science and product teams. The recommended approach is therefore to build a generic framework around common capabilities while keeping product-specific calculations, dimensions, thresholds and rules configurable.
Core design principle
Keep financial calculations deterministic and reproducible. Use the LLM for orchestration and explanation—not as the source of truth for numbers.


Recommended design decisions
Dashboard-first user experience, supported by a drill-down investigation workspace and an optional chat assistant.
Python, Pandas and statistical techniques as the initial analytical foundation; introduce ML only when a specific use case justifies it.
One orchestrator with specialised tools and conditional workflow steps for the initial POC, rather than multiple independent LLM agents.
A canonical data contract, product adapters and version-controlled product configurations to support future onboarding.
A one-week POC focused on autonomous investigation using the existing 12 months of loan data.
2. Business problem and target outcome
The current analyst-led process typically involves comparing two entities or periods, identifying the largest sources of variance, drilling into counterparties and ISINs, assessing the drivers, reviewing historical movements and documenting a conclusion.
Target analyst workflow
Select product, reporting period, entities and comparison dimensions.
Validate the input data and identify missing, duplicated or inconsistent records.
Calculate overall and granular variances.
Rank counterparties, ISINs or other dimensions by contribution to the total movement.
Investigate the drivers and compare movements with historical behaviour.
Classify findings as expected, unusual but explainable, unexplained or potential data-quality issue.
Generate an evidence-backed explanation and supporting report for analyst review.
3. Generic solution architecture
The architecture is organised into five layers. Product-specific logic is isolated from the common analytical and orchestration capabilities.
Layer
Responsibility
Illustrative components

1. User interface
Configure and launch analysis; review findings; drill down; export reports.
Product selection, comparison setup, dashboard, investigation workspace, chat panel.

2. Agentic orchestration
Plan the analysis, select tools, route exceptions and decide whether further investigation is required.
Workflow orchestrator, data-quality step, analysis planner, investigation and validation steps.

3. Analytical engine
Perform reproducible calculations and statistical tests.
Python functions, contribution analysis, variance decomposition, trend analysis, anomaly detection.

4. Product configuration
Define product-specific schema mappings, dimensions, measures, drivers, formulas and thresholds.
YAML/JSON configuration, business rules, product adapters, version control.

5. Data layer
Provide source and historical data; persist outputs, evidence and audit logs.
Approved data sources, standardised tables, historical snapshots, audit store.


High-level workflow
User submits an analysis request through the UI.
The workflow validates data and loads the applicable product configuration.
The planner selects the required analytical tools and execution sequence.
The analytical engine calculates variance and contribution results.
The investigation step drills into material or unusual movements where evidence is available.
The LLM drafts a plain-language explanation using structured calculation outputs and supporting records.
A validation step checks that the explanation is consistent with the evidence.
The analyst reviews, accepts, amends or rejects the conclusion.
4. User experience and UI recommendation
The UI should be dashboard-first rather than chatbot-first. Financial analysts need a clear numerical overview, traceable drill-downs and control over the investigation. A chat assistant is useful as a secondary interface for asking questions about the analysis.
Screen 1 — Product selection and analysis setup
Product selector (Loans initially; future products added through onboarding).
Reporting period and comparison period or entity selection.
Analysis level and dimensions (for example, counterparty, ISIN, stage or entity).
Historical lookback period and data source/upload selection.
Run analysis action, with pre-run data and configuration checks.
Screen 2 — Variance dashboard
UI component
Purpose

Total variance KPI
Show the overall absolute and percentage movement.

Positive and negative contributors
Show which items increase or reduce the net movement.

Top contributors
Rank counterparties, ISINs or other configured dimensions.

Historical trend
Compare the current movement with prior months.

Heatmap or driver matrix
Highlight concentration and unusual areas.

Analysis status
Show completed, needs investigation, data issue or analyst review.


Screen 3 — Investigation workspace
Provide a drill-down path such as Product → Entity → Counterparty → ISIN → Variance driver. Show source values, comparison values, calculated movement, contribution, historical context and supporting record references.
Screen 4 — AI investigation assistant
Offer a collapsible side panel that can answer questions using the current analysis context. Example questions include: “Why has the variance increased?”, “Which counterparties contribute most?”, “Is this movement unusual compared with the last 12 months?” and “Explain the top three drivers.” The assistant must call approved analytical tools and must not invent figures.
5. Technology approach: statistics, ML and LLMs
Start with deterministic calculations, business rules and statistical analysis. Machine learning should be introduced only when there is a defined problem that simpler methods cannot address adequately.
Technology
Role in the solution
Initial recommendation

Python / Pandas / NumPy
Data processing, calculations, reconciliation and reusable analytical functions.
Essential from day one.

Statistical analysis
Historical comparison, trend analysis, outlier detection and movement assessment.
Essential from day one.

Business rules
Product methodology, materiality, tolerances and classification logic.
Essential from day one.

LLM
Convert structured findings into readable explanations; interpret analyst questions.
Use with strict grounding.

Agentic orchestration
Choose tools, sequence analysis, route exceptions and decide when to investigate further.
Core POC differentiator.

Machine learning
Predict expected values, learn complex patterns or classify recurring cases.
Defer until justified by data and use case.


Initial statistical toolkit
Technique
Potential use

Absolute and percentage variance
Quantify the movement between periods or entities.

Contribution analysis
Identify the records or dimensions driving the total movement.

Mean, standard deviation and Z-score
Flag observations that are unusual relative to a suitable historical baseline.

Moving averages and trend analysis
Provide context on recurring and directional movements.

Correlation
Explore relationships between drivers; correlation does not prove causation.

Variance decomposition / attribution
Attribute a movement to underlying factors where a valid methodology exists.


Important distinction
A statistical anomaly is not automatically an error or a break. The platform should distinguish financial materiality from statistical unusualness and should not label a movement as incorrect without supporting business evidence.


6. What makes the solution agentic?
The agentic capability is the ability to plan and adapt the investigation—not simply to provide a chat interface. An orchestrator can select tools, inspect outputs, follow conditional paths and request human input when evidence is insufficient.
Workflow step
Action
Decision or agentic behaviour

Data-quality check
Check missing values, duplicates, schema and completeness.
Stop or route to remediation if critical checks fail.

Configuration selection
Load the product definition and applicable methodology.
Ask for clarification if product or configuration is ambiguous.

Analysis planning
Select calculations and dimensions.
Choose tools based on the configured product and analysis request.

Variance calculation
Calculate totals and granular movements.
Use deterministic functions; no LLM arithmetic.

Investigation
Rank contributors and inspect drivers and history.
Continue deeper analysis for material or unusual movements.

Explanation
Draft evidence-backed narrative.
Cite calculated outputs and supporting records.

Validation
Check numerical consistency and evidence coverage.
Flag unsupported explanations or send for rework.

Human review
Present findings for approval.
Retain analyst decision and feedback.


For the initial build, use one orchestrator with specialised tools or workflow nodes. Avoid creating several autonomous LLM agents until the workflow complexity and value justify them.
7. Generic product onboarding framework
The platform should separate common analytical capabilities from product-specific definitions. A new product should be onboarded by mapping its data, defining its methodology and adding only the specialised calculations that are genuinely required.
Canonical data contract
Record identifier and product identifier.
Entity identifier and reporting period.
Comparison dimensions (product-specific, such as counterparty, ISIN or stage).
Measures to compare.
Driver fields used to explain the movement.
Source lineage and data-quality metadata.
Illustrative product configuration — Loans
product:
  name: Loans

comparison:
  dimensions:
    - entity
    - counterparty
    - isin
    - stage

measures:
  - loan_balance

drivers:
  - number_of_days
  - interest_margin
  - drawn_amount
  - undrawn_amount

analysis:
  - absolute_variance
  - percentage_variance
  - contribution_analysis
  - historical_anomaly_detection

thresholds:
  materiality: configurable
  anomaly_method: z_score
Illustrative product configuration — Bonds
A future Bonds configuration might use dimensions such as entity, counterparty and ISIN, with measures such as accrued interest and drivers such as face value, coupon and market price. This is illustrative only; the product team must confirm the actual methodology.
Reusable framework components
Common functions: absolute variance, percentage variance, aggregation, contribution ranking and historical trend.
Product adapters: map source-specific columns into the canonical data contract.
Specialised functions: implement product-specific formulas or attribution methods where required.
Configuration and governance: version-control dimensions, thresholds, formulas and approval status.
Onboarding process: document and validate each product's methodology against analyst outputs.
8. One-week proof of concept
POC objective
Given two loan datasets, the system validates the data, identifies material variances, investigates leading contributors and drivers, checks historical context, and produces an evidence-backed explanation for analyst review.


POC scope
Capability
Implementation
Demonstration value

Data validation
Python checks for missing values, duplicates, schema mismatch and completeness.
Agent decides whether analysis can proceed.

Variance calculation
Deterministic Python functions.
Reproducible numbers.

Contribution analysis
Rank counterparties and configured dimensions.
Identifies where to investigate.

Historical analysis
Compare against available 12-month history using suitable statistical methods.
Adds context to current movements.

Investigation workflow
Conditional tool calls based on materiality and unusualness.
Demonstrates autonomous next-step selection.

Explanation
LLM narrative grounded in structured results.
Reduces manual write-up effort.

Validation and report
Numerical/evidence checks and analyst-ready output.
Supports review and traceability.


Five-day execution plan
Day
Work items
Deliverable

Day 1
Confirm loan schema, comparison logic, dimensions, drivers, materiality and acceptance criteria.
Agreed POC specification.

Day 2
Build data checks, variance calculations, contribution analysis and historical analysis.
Tested analytical functions.

Day 3
Implement the orchestrated workflow, tool interfaces and conditional investigation paths.
Working agent workflow.

Day 4
Build a lightweight UI with setup, dashboard, drill-down and explanation panel.
End-to-end prototype.

Day 5
Test against historical examples and analyst outcomes; fix issues; prepare demonstration.
Validated POC and demo script.


What to exclude from the first-week POC
Training a new ML model without a validated use case and labelled outcomes.
Building multiple independent LLM agents.
Implementing RAG before there is a defined need for methodology or knowledge retrieval.
Onboarding multiple real products before their methodologies are agreed.
Building a sophisticated production frontend or full enterprise deployment.
Allowing the LLM to calculate financial results or alter source data.
9. Suggested technology stack
Component
Suggested option
Notes

UI
Streamlit for POC; approved enterprise frontend later.
Fast to demonstrate; separate UI from core logic.

Orchestration
LangGraph or bank-approved equivalent.
Conditional routing, state and tool invocation.

LLM
Bank-approved enterprise model.
Use only approved endpoints and data classifications.

Analytical engine
Python, Pandas, NumPy, SciPy.
Deterministic, unit-tested calculations.

Visualisation
Plotly or approved charting library.
Contribution charts, trends and heatmaps.

Configuration
YAML/JSON with schema validation and version control.
Product definitions and thresholds.

Deployment
Approved Domino environment or bank platform.
Follow model, data and operational controls.


10. Role of RAG
RAG is not required for the first POC. It becomes useful when the agent must retrieve internal methodology documents, standard operating procedures, business definitions, approved investigation guidance or historical analyst conclusions.
Technology roles
Python calculates. Statistics contextualise. ML learns patterns when justified. RAG retrieves institutional knowledge. The agent orchestrates. The LLM explains.


11. Banking governance and controls
All calculations must be reproducible, versioned and independently testable.
Every AI-generated explanation should be linked to supporting calculations and source records.
The LLM must not modify source data or silently change calculation logic.
Unsupported or low-confidence conclusions must be flagged for analyst review.
Product configurations, formulas and thresholds must be version-controlled and approved.
Record agent actions, tool calls, configuration versions, model versions and analyst decisions.
Apply role-based access, data minimisation, retention controls and approved deployment boundaries.
Separate statistical unusualness, financial materiality and business classification.
12. Product onboarding questions for the data science and business teams
Question
Why it matters

Can each product provide a common minimum data contract, or are product adapters required?
Determines integration and standardisation design.

Which calculations are common and which are product-specific?
Defines reusable functions versus specialised logic.

How do analysts identify material counterparties, drivers and breaks today?
Captures the real investigation methodology.

Is 12–24 months of historical data available, and are analyst-validated outcomes retained?
Supports historical baselines and future ML evaluation.

Which LLMs, libraries, orchestration frameworks and deployment patterns are approved?
Ensures the design fits bank technology and risk controls.


13. Success measures for the POC
Agree measurable acceptance criteria with analysts before the demonstration. Suggested measures include:
Calculation accuracy against independently verified analyst calculations.
Coverage of material contributors identified by the analyst.
Precision of unusual-movement flags and rate of false positives.
Percentage of generated explanations supported by traceable evidence.
Time taken to complete an investigation compared with the current process.
Analyst acceptance, amendment and rejection rates for generated explanations.
Ability to add a second illustrative product configuration without changing the core orchestration and common engine.
14. Recommended roadmap
Phase
Focus
Expected outcome

Phase 1 — One-week POC
Loan workflow, Python/statistical engine, one orchestrator, evidence-backed explanations and basic UI.
Demonstrate autonomous investigation on a known product.

Phase 2 — Generic framework
Canonical data model, adapters, product configuration, reusable functions and onboarding process.
Establish a repeatable path for new products.

Phase 3 — Advanced intelligence
ML where justified, RAG for internal knowledge, analyst feedback and advanced investigation.
Improve detection and explanation quality.

Phase 4 — Enterprise deployment
Multi-product rollout, access controls, auditability, monitoring and operational support.
Scale securely across products.


15. Final recommendation
Build a Loan Variance Investigation Agent on top of a generic Product Configuration Framework. The first release should validate the known loan methodology, demonstrate autonomous selection of investigation steps and produce explanations grounded in calculated evidence.
Do not make the chatbot the centre of the product. Make the analytical workflow the centre, with a dashboard for review and a conversational assistant as an additional way to interrogate results.
The strategic advantage
Separating the common analytical engine from product-specific business logic prevents the team from rebuilding the solution for every new product. New onboarding should primarily require data mapping, configuration, methodology validation and only those specialised functions that are genuinely new.



Document status: Solution concept for discussion. Product-specific methodologies, thresholds, data contracts and bank technology approvals remain subject to confirmation.


Appendix A — Confirmed scope and refined multi-product strategy
The following points have been confirmed by the initiative owner and should govern the target design:
All 17 analytical requirements listed for Financial Assets at Amortised Cost belong to the same product; they are not separate product use cases.
Some of the 17 requirements are already supported by the current dashboard, while others are still planned and need to be delivered.
The strategic objective is a reusable variance analysis solution that can be adopted by other products and teams, reducing manual effort and cost while improving adaptability.
Refined strategic objective
Build a multi-product Variance Analysis Platform with a common analytical and agentic foundation, configurable product methodologies and reusable investigation capabilities. Financial As
