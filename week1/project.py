import os
import sqlite3
from getpass import getpass
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI

DB_FILE = "app_data.db"


def init_db():
    """Creates the users table and LangChain's message store schema if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Simple table to store user credentials
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def register_user():
    print("\n---  Create a New Account ---")
    username = input("Choose a username: ").strip().lower()
    if not username:
        print("Username cannot be blank.")
        return False

    password = getpass("Choose a password: ")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password),
        )
        conn.commit()
        print("✨ Account created successfully! You can now log in.")
        return True
    except sqlite3.IntegrityError:
        print(" Username already exists. Please choose a different one.")
        return False
    finally:
        conn.close()


def login_user():
    print("\n---  User Login ---")
    username = input("Username: ").strip().lower()
    password = getpass("Password: ")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password),
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f" Welcome back, {username}!")
        return username
    else:
        print(" Invalid username or password.")
        return None


def get_sqlite_history(session_id: str) -> SQLChatMessageHistory:
    """Dynamically links the execution session to a row-isolated table structure in SQLite."""
    return SQLChatMessageHistory(
        session_id=session_id, connection_string=f"sqlite:///{DB_FILE}"
    )


def build_conversational_chain():
    # Uses the official environment variable GEMINI_API_KEY
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an advanced AI companion. Rely on the provided conversation history to maintain context.",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    base_chain = prompt | llm | StrOutputParser()

    # The wrapper binds the SQLite history loader to the chain execution process
    return RunnableWithMessageHistory(
        runnable=base_chain,
        get_session_history=get_sqlite_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )


def main():
    init_db()

    print("=============================================")
    print("Welcome to the Secure Gemini CLI Client")
    print("=============================================")

    # Handle entry state
    current_user = None
    while not current_user:
        choice = (
            input("\nSelect an option:\n1. Login\n2. Register\n3. Exit\n> ")
            .strip()
            .lower()
        )

        if choice in ["1", "login"]:
            current_user = login_user()
        elif choice in ["2", "register"]:
            register_user()
        elif choice in ["3", "exit", "quit"]:
            print("Goodbye!")
            return
        else:
            print("Invalid selection. Please choose 1, 2, or 3.")

    
    user_session_id = f"session_default_user_{current_user}"

    chain = build_conversational_chain()
    config = {"configurable": {"session_id": user_session_id}}

    print(f"\n Chat session activated for '{current_user}'.")
    print("Type 'exit' to log out. Your history will be preserved automatically!\n")

    while True:
        try:
            user_input = input(" You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print(f"\nLogged out from user session: {current_user}")
                break

            print(" Gemini: ", end="", flush=True)

            response = chain.invoke({"input": user_input}, config=config)
            print(response + "\n")

        except KeyboardInterrupt:
            print("\nSession safely closed.")
            break
        except Exception as e:
            print(f"\nAn error occurred running the chain: {e}\n")


if __name__ == "__main__":
    main()