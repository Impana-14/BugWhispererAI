
import pytest

from app.memory import ConversationMemory


def test_add_and_get_messages():
    memory = ConversationMemory()

    memory.add_message("chat-1", "user", "My code has an error.")
    memory.add_message("chat-1", "assistant", "Please share the traceback.")

    messages = memory.get_messages("chat-1")

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["content"] == "Please share the traceback."


def test_conversations_are_separate():
    memory = ConversationMemory()

    memory.add_message("chat-1", "user", "First conversation")
    memory.add_message("chat-2", "user", "Second conversation")

    assert len(memory.get_messages("chat-1")) == 1
    assert memory.get_messages("chat-1")[0]["content"] == "First conversation"


def test_memory_keeps_only_recent_messages():
    memory = ConversationMemory(max_messages=2)

    memory.add_message("chat-1", "user", "First")
    memory.add_message("chat-1", "assistant", "Second")
    memory.add_message("chat-1", "user", "Third")

    messages = memory.get_messages("chat-1")

    assert len(messages) == 2
    assert messages[0]["content"] == "Second"
    assert messages[1]["content"] == "Third"


def test_clear_conversation():
    memory = ConversationMemory()

    memory.add_message("chat-1", "user", "Temporary message")
    memory.clear_conversation("chat-1")

    assert memory.get_messages("chat-1") == []


def test_invalid_role_is_rejected():
    memory = ConversationMemory()

    with pytest.raises(ValueError):
        memory.add_message("chat-1", "system", "Invalid role")
