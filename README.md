# udise-student-progression-automation
An enterprise-grade headless automation framework using Playwright to handle the annual UDISE+ student data validation and progression workflows. The system automatically cycles through student profiles, updates data parameters.

# Core Design
Loop Iteration: For each student in a given class section, the script sequences through sequential UI tabs:
1. GP (General Profile): Validates and saves identity records.
2. EP (Enrollment Profile): Commits academic registration data.
3. FP/PP (Facility/Productive Profile): Assigns state-provided infrastructure metrics.

[Dashboard] ──> [Select Class] ──> [Loop Students] ──> [Verify GP -> EP -> FP/PP] ──> [Confirm Progression]
     ▲                                                                                       │
     └─────────────────────────── [Last Student Processed] ──────────────────────────────────┘
# Architectural Benefits
1. Auto-Wait Resiliency: Replaces fragile time.sleep()
2. Network Interception: Captures API responses
3. Parallel Execution: allowing multiple class modules to run concurrently.

