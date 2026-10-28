
from collections import defaultdict


class ConversationMemory:
    """Store debugging context for each conversation."""

    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self._conversations: dict[str, list[dict[str, str]]] = defaultdict(list)

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ) -> None:
        """Add a user or assistant message to a conversation."""
        if role not in {"user", "assistant"}:
            raise ValueError("Role must be 'user' or 'assistant'.")

        messages = self._conversations[conversation_id]
        messages.append({"role": role, "content": content})

        # Keep only the most recent messages.
        self._conversations[conversation_id] = messages[-self.max_messages :]

    def get_messages(self, conversation_id: str) -> list[dict[str, str]]:
        """Return a copy of the conversation history."""
        return list(self._conversations.get(conversation_id, []))

    def clear_conversation(self, conversation_id: str) -> None:
        """Clear one conversation's stored history."""
        self._conversations.pop(conversation_id, None)
