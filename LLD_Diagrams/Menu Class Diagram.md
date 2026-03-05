```mermaid
classDiagram
    class Menu {
        +int select_action
        -save(file)
        -generate_filename()
        -act(selected_action)
        -confirm_delete()
        +new_note(file)
        +display(file)
        +append(file)
        +summarize(file)
        +delete(file)
        +select()
    }
```
