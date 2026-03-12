```mermaid
classDiagram
    class Menu {
        -string password
        -get_password()
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
        +act(selected_action)
    }
```
