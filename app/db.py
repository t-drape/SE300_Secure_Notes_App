import sqlite3
from datetime import datetime
from typing import Optional


class _DbConnectError(Exception):
    """Internal exception for database operation failures. Not intended for external use."""

    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(self.msg)


class DbConnect:
    """Manages all SQLite database interactions for the notes application."""

    def __init__(self, db_name: str = "notes.db"):
        self._con = sqlite3.connect(db_name)
        self._con.row_factory = sqlite3.Row
        self.cur = self._con.cursor()

    def __enter__(self) -> "DbConnect":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self._con.commit()
        self._con.close()

    def _commit(self) -> None:
        """Commits the current transaction."""
        self._con.commit()

    def create_directory(self, dname: str) -> bool:
        """
        Creates a new directory, represented as a separate table in the database.

        Args:
            dname: The name of the directory (table) to create.

        Returns:
            True if the directory was created successfully.

        Raises:
            _DbConnectError: If the directory could not be created or verified.
        """
        try:
            self.cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {dname} (
                    idx      INTEGER PRIMARY KEY AUTOINCREMENT,
                    note_name TEXT NOT NULL UNIQUE,
                    date     TEXT NOT NULL,
                    content  TEXT NOT NULL
                )
                """
            )
            self._commit()
        except sqlite3.Error as e:
            raise _DbConnectError(f"Failed to create directory '{dname}': {e}")

        result = self.cur.execute(
            "SELECT name FROM sqlite_master WHERE name = ?", (dname,)
        ).fetchone()

        if result and result[0] == dname:
            return True

        raise _DbConnectError(f"Directory '{dname}' could not be verified after creation.")

    def create_note(self, dname: str, note_name: str, content: str) -> Optional[int]:
        """
        Creates a new note in the specified directory.

        Args:
            dname:     The directory (table) to insert the note into.
            note_name: A unique name/identifier for the note.
            content:   The text content of the note.

        Returns:
            The integer index (idx) of the newly created note, or None if retrieval failed.

        Raises:
            _DbConnectError: If the insert operation fails.
        """
        today = datetime.today().isoformat()

        try:
            self.cur.execute(
                f"INSERT INTO {dname} (note_name, date, content) VALUES (?, ?, ?)",
                (note_name, today, content),
            )
            self._commit()
        except sqlite3.Error as e:
            raise _DbConnectError(f"Failed to create note '{note_name}': {e}")

        return self.cur.lastrowid

    def get_directories(self) -> list[str]:
        """
        Retrieves all user-created directories (tables) in the database.

        Returns:
            A list of directory names, excluding internal SQLite tables.
        """
        self.cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        return [row[0] for row in self.cur.fetchall()]

    def delete_note(self, dname: str, note_name: str) -> bool:
        """
        Hard-deletes a note from the specified directory.

        Args:
            dname:     The directory (table) containing the note.
            note_name: The name of the note to delete.

        Returns:
            True if a note was deleted, False if no matching note was found.

        Raises:
            _DbConnectError: If the delete operation fails.
        """
        try:
            self.cur.execute(
                f"DELETE FROM {dname} WHERE note_name = ?", (note_name,)
            )
            self._commit()
        except sqlite3.Error as e:
            raise _DbConnectError(f"Failed to delete note '{note_name}': {e}")

        return self.cur.rowcount > 0

    def update_note(self, dname: str, note_name: str, content: str) -> bool:
        """
        Updates the content of an existing note.

        Args:
            dname:     The directory (table) containing the note.
            note_name: The name of the note to update.
            content:   The new content to replace the existing note body.

        Returns:
            True if the note was updated, False if no matching note was found.

        Raises:
            _DbConnectError: If the update operation fails.
        """
        try:
            self.cur.execute(
                f"UPDATE {dname} SET content = ? WHERE note_name = ?",
                (content, note_name),
            )
            self._commit()
        except sqlite3.Error as e:
            raise _DbConnectError(f"Failed to update note '{note_name}': {e}")

        return self.cur.rowcount > 0

    def display_note(self, dname: str, note_name: str) -> Optional[str]:
        """
        Retrieves the content of a note by name.

        Args:
            dname:     The directory (table) to search in.
            note_name: The name of the note to retrieve.

        Returns:
            The note's content as a string, or None if no matching note was found.

        Raises:
            _DbConnectError: If the query fails.
        """
        try:
            self.cur.execute(
                f"SELECT content FROM {dname} WHERE note_name = ? LIMIT 1",
                (note_name,),
            )
        except sqlite3.Error as e:
            raise _DbConnectError(f"Failed to retrieve note '{note_name}': {e}")

        result = self.cur.fetchone()
        return result[0] if result else None
