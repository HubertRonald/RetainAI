from __future__ import annotations

import json
from typing import Any

SYSTEM_PROMPT = (
    "You are RetainAI Retention Advisor, an HR decision-support assistant.\n"
    "You explain employee attrition risk in a careful, transparent and "
    "non-deterministic way.\n"
    "You must not make automated employment decisions.\n"
    "You must provide practical retention discussion points based only on the "
    "structured payload.\n"
    "You must avoid protected-class assumptions and sensitive personal inferences."
)

USER_PROMPT_TEMPLATE = (
    "Analyze the following RetainAI employee retention explanation payload.\n\n"
    "Return:\n"
    "1. A concise risk summary.\n"
    "2. The top risk drivers in plain language.\n"
    "3. Potential retention actions for an HR partner to consider.\n"
    "4. Caveats and responsible-use notes.\n\n"
    "Payload:\n{payload_json}"
)


def build_retention_advisor_messages(payload: dict[str, Any]) -> list[dict[str, str]]:
    payload_json = json.dumps(payload, indent=2, ensure_ascii=False, default=str)
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": USER_PROMPT_TEMPLATE.format(payload_json=payload_json),
        },
    ]


def build_retention_advisor_prompt(payload: dict[str, Any]) -> str:
    messages = build_retention_advisor_messages(payload)
    return "\n\n".join(
        f"{message['role'].upper()}:\n{message['content']}" for message in messages
    )
