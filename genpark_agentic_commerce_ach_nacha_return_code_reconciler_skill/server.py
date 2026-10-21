# -*- coding: utf-8 -*-
"""MCP Server for NACHA ACH Micro-Deposit Settlement & Return Code Reconciler Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import ACHNACHAReturnCodeReconciler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "triage_nacha_return_code",
        "description": "Triage NACHA return code (e.g. R01 Insufficient Funds, R07 Authorization Revoked) and formulate automated resolution route.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "nacha_code": {
                    "type": "string"
                },
                "days_since_settlement": {
                    "type": "integer"
                }
            },
            "required": [
                "nacha_code"
            ]
        }
    },
    {
        "name": "reconcile_micro_deposit_verification",
        "description": "Validate 2 random micro-deposit amounts submitted by user against ledger records within expiration window.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "deposit_1_cents": {
                    "type": "integer"
                },
                "deposit_2_cents": {
                    "type": "integer"
                },
                "user_entry_1_cents": {
                    "type": "integer"
                },
                "user_entry_2_cents": {
                    "type": "integer"
                },
                "elapsed_hours": {
                    "type": "number"
                }
            },
            "required": [
                "deposit_1_cents",
                "deposit_2_cents",
                "user_entry_1_cents",
                "user_entry_2_cents"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-ach-nacha-return-code-reconciler-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(ACHNACHAReturnCodeReconciler, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-ach-nacha-return-code-reconciler-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
