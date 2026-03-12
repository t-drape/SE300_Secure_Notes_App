```mermaid
classDiagram
    class Menu {
        -string password
        -save(file)
        -generate_filename()
        -choose_file()
        -confirm_delete()
        -new_note(file)
        -display(file)
        -append(file)
        -summarize(file)
        -delete(file)
        -select()
        +get_password()
        +act(selected_action)
    }
```
