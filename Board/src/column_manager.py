import flet as ft

class ColumnManager(ft.Container):
    def __init__(self):
        super().__init__()
        self.columns = []
        
    def add_column(self, column_name, color):
        if not column_name:
            raise ValueError("Column name cannot be empty")
            
        new_column = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        expand=True,
                        controls=[
                            ft.Text(column_name, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                        ],
                    ),
                    bgcolor=color,
                ),
                ft.Column(controls=[], expand=True)  # Container for lists
            ],
        )
        self.columns.append(new_column)
        return new_column
        
    def add_list_to_column(self, column_index, board_list, page):
        if 0 <= column_index < len(self.columns):
            self.columns[column_index].controls[1].controls.append(board_list)
            self.columns[column_index].controls[1].update()  # Update the column
            page.update()  # Update the page
            print(f"List added to column at index {column_index}")
            return True
        raise IndexError("Invalid column index")
        
    def edit_column(self, index, new_name):
        if not new_name:
            raise ValueError("Column name cannot be empty")
            
        if 0 <= index < len(self.columns):
            self.columns[index].controls[0].content.value = new_name
            return True
        raise IndexError("Invalid column index")
        
    def delete_column(self, index):
        if 0 <= index < len(self.columns):
            self.columns.pop(index)
            return True
        raise IndexError("Invalid column index")
        
    def get_columns(self):
        return self.columns
        
    def update_column_list(self, selector):
        selector.options = [
            ft.dropdown.Option(str(i)) for i in range(len(self.columns))
        ]
        selector.value = str(len(self.columns) - 1) if self.columns else None