# -*- coding: utf-8 -*-
"""NACHA ACH Return Code Reconciler for GenPark Agentic Commerce."""
import json
from typing import Dict, Any

class ACHNACHAReturnCodeReconciler:
    @staticmethod
    def triage_nacha_return_code(nacha_code: str, days_since_settlement: int = 1) -> Dict[str, Any]:
        code = nacha_code.strip().upper()
        catalog = {
            "R01": ("Insufficient Funds", "RETRY_WITH_EXPONENTIAL_BACKOFF", "Automatic re-presentment in 3 business days."),
            "R02": ("Account Closed", "HARD_SUSPEND", "Immediately deactivate bank account; prompt user for backup payment method."),
            "R03": ("No Account / Unable to Locate", "HARD_SUSPEND", "Invalid routing or account number. Freeze customer billing."),
            "R05": ("Unauthorized Debit to Consumer Account", "COMPLIANCE_DISPUTE", "Critical unauthorized return; initiate compliance audit."),
            "R07": ("Authorization Revoked by Customer", "REVOKE_MANDATE", "Remove customer autopay mandate per NACHA guidelines."),
            "R08": ("Payment Stopped", "INVESTIGATE_STOP_PAYMENT", "Contact account holder regarding stop-payment notice."),
            "R10": ("Customer Advises Not Authorized", "CHARGEBACK_HOLD", "Immediate fraud freeze; file proof of consent record.")
        }
        name, action, directive = catalog.get(code, ("Unclassified ACH Return Code", "MANUAL_ESCALATION", "Investigate via ODFI exception desk."))
        return {
            "nacha_return_code": code,
            "description": name,
            "automated_action": action,
            "operational_directive": directive,
            "allowable_retry_flag": action.startswith("RETRY")
        }

    @staticmethod
    def reconcile_micro_deposit_verification(deposit_1_cents: int, deposit_2_cents: int, user_entry_1_cents: int, user_entry_2_cents: int, elapsed_hours: float = 12.0) -> Dict[str, Any]:
        if elapsed_hours > 72.0:
            return {"status": "EXPIRED", "verified": False, "reason": "Micro-deposit verification window exceeded 72 hours."}
        
        expected = sorted([deposit_1_cents, deposit_2_cents])
        actual = sorted([user_entry_1_cents, user_entry_2_cents])
        
        match = (expected == actual)
        return {
            "verified": match,
            "status": "ACCOUNT_VERIFIED_ACTIVE" if match else "AMOUNT_MISMATCH",
            "elapsed_hours": elapsed_hours,
            "cleared_for_origination": match
        }
