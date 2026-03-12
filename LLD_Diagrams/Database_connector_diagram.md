classDiagram
    class DbConnect {
        -connection
        -cursor
        +db_name
        -log_access()
        -send_note()
        +create_directory(dir_name)
        +create_note(contents)
        +get_directories()
        +delete_note(id)
        +append_note(id)
        +display_note(id)
    }
