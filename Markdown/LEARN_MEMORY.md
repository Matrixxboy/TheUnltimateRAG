# Dual-Memory System Architecture

This document explains the conceptual and technical implementation of the Short-Term + Long-Term memory system in TheUltimateRAG.

## Concept

To maintain context over long conversations without exceeding token limits or incurring high costs, we implement a **Dual-Memory** strategy involves two distinct storage mechanisms:

1.  **Short-Term Memory (STM)**:

    - **Type**: Exact Recall.
    - **Storage**: In-Memory (Active Session).
    - **Limit**: Fixed number of turns (Default: 5 User pairs, configurable via `SHORT_TERM_MEMORY_LIMIT`).
    - **Purpose**: Handles immediate context, follow-up questions, and recent topics.

2.  **Long-Term Memory (LTM)**:
    - **Type**: Summarized Recall.
    - **Storage**: PostgreSQL Database (`long_term_memories` table).
    - **Trigger**: When STM exceeds the limit.
    - **Purpose**: Retains high-level key facts and context from past interactions indefinitely.

## The Consolidation Process

When the user interacts with the system, the following pipeline executes:

1.  **Interaction**: User sends a message -> RAG Pipeline processes it -> AI responds.
2.  **Check**: The system checks the number of messages in the current session.
3.  **Trigger**: If `User Messages > SHORT_TERM_MEMORY_LIMIT`:
    - **Step A (Summarize)**: The entire Short-Term Memory history is sent to an LLM with a prompt to "Summarize the conversation into a concise paragraph/word chunks".
    - **Step B (Archive)**: This summary is inserted into the PostgreSQL database associated with the `session_id`.
    - **Step C (Forget)**: The Short-Term Memory is wiped clean (starts fresh).

## Configuration

You can adjust the behavior in `config/settings.py` or `.env`:

```env
# Number of user messages before consolidation (N)
SHORT_TERM_MEMORY_LIMIT=5
```

## How to Test

1.  Set `SHORT_TERM_MEMORY_LIMIT=2` in your environment.
2.  Start a conversation (Session ID X).
3.  Chat for 3 turns.
4.  Observe that after the 3rd turn, the detailed history in your debug logs (or if you inspect the `MemoryManager`) is reset.
5.  Check the database:
    ```sql
    SELECT * FROM long_term_memories ORDER BY created_at DESC;
    ```
    You should see a new summary entry for Session ID X.

## Future Improvements

- **Retrieval**: Currently, LTM is stored but not actively retrieved for context injection. Future updates should query `long_term_memories` (or vector embed them) to provide "Generic Context" to the LLM alongside RAG documents.
