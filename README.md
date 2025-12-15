This repository provides actionable code, templates, and analysis tools to implement advanced FinOps strategies for high-cost Artificial Intelligence (AI) and Machine Learning (ML) workloads on **AWS**.

The focus is on **Day 5 FinOps Optimization**: moving beyond reporting to strategically reducing spend through cost arbitrage and AWS-native features like Savings Plans, Reserved Instances, and Spot Fleets.

---

## 🎯 Key Strategies Covered

1.  **Resource Tagging (The Foundation):** Establishing an enforced tagging standard across AWS resources for accurate cost allocation and unit economics (Cost per Inference, Cost per Training Epoch).
2.  **Spot Arbitrage:** Leveraging high-discount, interruptible **EC2 Spot Fleet** capacity (up to 90% savings) for fault-tolerant workloads like model training and batch processing.
3.  **Committed Use Arbitrage:** Analyzing and purchasing long-term commitments (**Savings Plans/RIs**) for stable, production AI inference clusters.

## 📂 Directory Guide

| Directory | Purpose | Key File(s) |
| :--- | :--- | :--- |
| `1-Tagging-Templates/` | Defines the required metadata and enforcement for every AWS AI resource. | `tagging-schema.json`, `aws-config-rule.yaml` |
| `2-Cost-Arbitrage/` | Contains the code and templates for optimization strategies. | `aws-spot-ml-launcher.py`, `ri-cfo-analysis.csv` |

---

## 💡 Recommended Next Steps

1.  Review and adopt the `tagging-schema.json` in your organization.
2.  Deploy the `aws-config-rule.yaml` to enforce tagging compliance.
3.  Test the `aws-spot-ml-launcher.py` with a non-critical model training workload.
4.  Use the `ri-cfo-analysis.csv` to calculate the breakeven point for your production inference cluster Savings Plan.
