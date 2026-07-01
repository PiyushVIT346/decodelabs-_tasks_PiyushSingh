"""
chain.py
--------
LangChain wiring, kept separate from Flask routing. Each call to
`chat(session_id, text)` logs a ledger entry before and after the DB write
so the frontend can show storage activity as it happens.
"""

from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI

import storage

_chain = None  # lazily built singleton


def get_sqlite_history(session_id: str) -> SQLChatMessageHistory:
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string=f"sqlite:///{storage.DB_FILE}",
    )


def _build_chain() -> RunnableWithMessageHistory:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an advanced AI companion. Rely on the provided "
                "conversation history to maintain context.",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    base_chain = prompt | llm | StrOutputParser()

    return RunnableWithMessageHistory(
        runnable=base_chain,
        get_session_history=get_sqlite_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )


def get_chain() -> RunnableWithMessageHistory:
    global _chain
    if _chain is None:
        _chain = _build_chain()
    return _chain


def chat(session_id: str, username: str, user_input: str) -> str:
    """Run one turn and record the two resulting storage writes."""
    storage.append_ledger("insert_message", username=username, detail="role=human")
    response = get_chain().invoke(
        {"input": user_input}, config={"configurable": {"session_id": session_id}}
    )
    storage.append_ledger("insert_message", username=username, detail="role=ai")
    return response


def load_history(session_id: str) -> list[dict]:
    """Return the persisted conversation as plain dicts for the frontend."""
    history = get_sqlite_history(session_id)
    return [{"role": m.type, "content": m.content} for m in history.messages]