# V1 Fixture — Independently Derived Expected Results (SAMPLE)

> These expectations are derived by hand from what each fixture *should* produce given
> its written Terraform/IAM content — NOT copied from SKYNEX's actual output. Once you
> run each fixture against the real engines, compare results here; any mismatch is a
> candidate defect, not an automatic "update the expectation" situation. If SKYNEX's
> actual behavior differs, decide deliberately whether the expectation or the code is
> wrong.

## 01_minimal_valid.tf
- Resources: 1 (`aws_s3_bucket.minimal_bucket`)
- Relationships: 0
- Findings: 0 (no policy attached, no public access configured)
- Risk score: minimal/none
- Attack path: none
- Blast radius: N/A (no findings to radiate from)

## 02_multi_resource_valid.tf
- Resources: 4 (2 buckets, 1 IAM user, 1 security group)
- Relationships: 0 (no cross-references in the HCL)
- Findings: 0 (no dangerous config present)

## 03_relationships.tf
- Resources: 4 (SG, IAM role, instance profile, EC2 instance)
- Relationships: 3 — instance→SG, instance→instance profile, instance profile→role
- Findings: 0 (no public ingress, no wildcard IAM)

## 04_attack_path.tf
- Resources: 6
- Findings: ≥2 — public SG ingress (0.0.0.0/0, all ports) AND wildcard IAM policy (`*`:`*`)
- Attack path: internet → public_sg → public_server → overprivileged_role → wildcard_policy → sensitive_data bucket
- Severity: HIGH (public entry point + full-admin IAM chained to sensitive data)

## 05_blast_radius.tf
- Resources: 5 (role, profile, 3 instances)
- Relationships: 3 instance→profile edges, all pointing to the same role
- Blast radius of `shared_role`: exactly {server_1, server_2, server_3} — 3 resources, no more, no fewer

## 06_high_risk.tf
- Resources: 2 (bucket, bucket policy)
- Findings: 1 — public bucket policy (`Principal: "*"`, `Action: "s3:*"`)
- Severity: HIGH

## 07_medium_risk.tf
- Resources: 1 (SG)
- Findings: 1 — single non-standard port (8080) open to 0.0.0.0/0
- Severity: MEDIUM (single port, non-privileged service port, vs. 04/06's broader exposure)

## 08_low_risk.tf
- Resources: 1 (SG)
- Findings: 0 or LOW informational only — ingress restricted to RFC1918 CIDR (10.0.0.0/16)

## 09_no_findings.tf
- Resources: 2 (role, policy)
- Findings: 0 — policy is scoped to a single read-only action on a specific bucket path

## 10_invalid_syntax.tf
- Expected: ingestion rejects with a 400-class validation error citing the malformed
  block. No partial resources created. No 500.

## 11_empty.tf
- Expected: defined, documented behavior — either 400 ("no resources found") or 200
  with an empty resource set. Must NOT crash or hang. Whichever behavior SKYNEX
  implements must be consistent and documented — this fixture's job is to catch
  whichever one it *doesn't* do consistently.

## 12_missing_structure.tf
- Expected: valid HCL parse, but zero resource blocks recognized → same empty-result
  handling as 11_empty.tf should apply (0 resources, not an error, unless resource-less
  input is explicitly disallowed by spec).

## 13_duplicate_resources.tf
- Expected: rejected as invalid Terraform (duplicate resource address) OR explicitly
  documented dedup behavior. Silent silent acceptance of both as separate resources
  with no warning is a defect.

## 14_disconnected_resources.tf
- Resources: 3
- Relationships: 0 — relationship engine must NOT invent edges between unrelated resources

## 15_cyclic_relationships.tf
- Resources: 2 SGs + 2 rules
- Relationship graph contains a cycle (cycle_a ↔ cycle_b)
- Expected: traversal engine terminates in bounded time, does not infinite-loop or
  stack-overflow; cycle is either represented once (deduplicated) or traversal has an
  explicit visited-node guard

## 16_complex_environment.tf
- Resources: 10 (3 SGs, role, policy, profile, 2 instances, RDS instance, S3 bucket)
- Findings: ≥1 — wildcard `s3:*` on `*` resource attached to `app_role`
- Attack path: web_sg (public 443) → app_server → app_role → app_policy (wildcard s3) → app_data bucket
- Relationships: SG chain (web→app→db via security_groups references), instance→profile→role

## 17_remediation.tf
- Resources: 1 (SG)
- Findings: 1 — SSH (22) open to 0.0.0.0/0
- Remediation: must reference this specific finding's ID and suggest restricting the
  CIDR block or replacing with bastion/SSM access — remediation text must not be generic
  boilerplate disconnected from the actual finding

## 18_cross_resource_reference.tf
- Resources: 3 (bucket, role, lambda)
- Relationships: lambda→role (execution role) AND lambda→bucket (via environment variable
  reference) — tests that relationship discovery isn't limited to SG/IAM-instance-profile
  patterns only

## 19_boundary_case.tf
- Resources: 2
- Findings: 0 (no dangerous config)
- Must not crash on the long resource name or the zero-rule security group

## 20_large_reasonable_environment.tf
- Resources: 13 (SG, role, profile, 10 instances via `count`)
- Relationships: 10 instance→profile edges (all to the same role)
- Must complete ingestion + all engine passes within a reasonable time bound (define
  and record actual wall-clock time — this is a stability/smoke signal, not a hard
  perf gate unless SKYNEX defines one)

---

## IAM Fixtures

### iam_minimal.json
- Single read-only, resource-scoped statement — expect 0 findings

### iam_least_privilege.json
- Scoped read access with a condition — expect 0 findings; this is the "good example"
  baseline

### iam_overprivileged.json
- `Action: "*"`, `Resource: "*"` AND unrestricted `iam:PassRole` — expect ≥2 findings,
  at least one CRITICAL/HIGH severity for the wildcard admin statement

### iam_invalid.json
- Malformed JSON (missing closing braces) — expect 400 validation error, not a crash

### iam_empty.json
- `{}` — expect a defined validation error (missing required `Statement`/`Version`
  keys), not a silent "0 findings" success

### iam_complex.json
- 5 statements mixing Allow/Deny, wildcards, and conditions — expect the engine to
  correctly identify the `lambda:InvokeFunction` wildcard-resource statement as a
  finding while NOT flagging the correctly-scoped or explicitly-denied statements
