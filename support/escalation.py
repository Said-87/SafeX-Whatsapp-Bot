"""
Human Escalation Module
Creates escalation tickets for conversations
that cannot be answered automatically.
"""

import uuid
from datetime import datetime


class EscalationManager:

    def __init__(self):
        self.agent_name = "Human Agent"

    def create_ticket(
        self,
        message,
        language,
        reason="FAQ Not Found",
        user=None
    ):
        """
        Create a human support ticket.
        """

        ticket = {
            "ticket_id": str(uuid.uuid4())[:8].upper(),
            "status": "Escalated",
            "assigned_to": self.agent_name,
            "reason": reason,
            "language": language,
            "message": message,
            "user": user or {},
            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        return ticket


# -----------------------------------------
# Singleton
# -----------------------------------------

manager = EscalationManager()


# -----------------------------------------
# Compatibility Function
# -----------------------------------------

def escalate_to_agent(chat_context):
    """
    Keeps compatibility with app.py
    """

    return manager.create_ticket(
        message=chat_context.get("message", ""),
        language=chat_context.get("language", "en"),
        reason=chat_context.get(
            "reason",
            "FAQ Not Found"
        ),
        user=chat_context.get("user")
    )