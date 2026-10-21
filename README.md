# NACHA ACH Micro-Deposit Settlement & Return Code Reconciler Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

NACHA ACH return code triage (R01-R85), micro-deposit verification timeout, settlement float projection, and ledger matching. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `triage_nacha_return_code`: Triage NACHA return code (e.g. R01 Insufficient Funds, R07 Authorization Revoked) and formulate automated resolution route.
- `reconcile_micro_deposit_verification`: Validate 2 random micro-deposit amounts submitted by user against ledger records within expiration window.

## 🚀 Installation & Usage
```bash
python -m genpark_agentic_commerce_ach_nacha_return_code_reconciler_skill.server --test
```
