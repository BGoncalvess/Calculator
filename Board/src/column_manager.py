import flet as ft

class ColumnManager(ft.Container):
    def __init__(self, page: ft.Page, board: "Board"):
        super().__init__()
        self.page = page  # Store page reference to access width/height
        self.board = board  # Store the Board reference
        self.columns = []
        
    def add_column(self, column_name, color):
        # Container for lists (starts empty with a placeholder)
        lists_container = ft.Column(
            controls=[ft.Container(height=100, width=250, bgcolor=ft.Colors.TRANSPARENT)],  # Placeholder
            expand=True,  # Takes up available space
            scroll=ft.ScrollMode.AUTO,  # Optional: allows scrolling if lists overflow
        )

        lists_container = ft.Column(
            controls=[],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
       
        new_column = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(column_name, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
                        ],
                    ),
                    bgcolor=color,
                    padding=ft.padding.all(5),
                ),
                ft.DragTarget(
                    group="lists",
                    content=lists_container,
                    on_accept=lambda e: self.board.accept_list_to_column(e, new_column),
                    on_will_accept=lambda e: self.highlight_column(new_column, True),
                    on_leave=lambda e: self.highlight_column(new_column, False),
                ),
            ],
        )
        self.columns.append(new_column)
        return new_column
        
    def add_list_to_column(self, column_index, board_list, page):
        if 0 <= column_index < len(self.columns):
            self.columns[column_index].controls[1].controls.append(board_list)
            self.columns[column_index].controls[1].update()  # Update the inner column
            page.update()  # Update the page
            print(f"List added to column at index {column_index}")
            return True
        raise IndexError("Invalid column index")

    def edit_column(self, index, new_name):
        if not new_name:
            raise ValueError("Column name cannot be empty")
            
        if 0 <= index < len(self.columns):
            self.columns[index].controls[0].content.controls[0].value = new_name
            return True
        raise IndexError("Invalid column index")
        
    def delete_column(self, index):
        if 0 <= index < len(self.columns):
            self.columns.pop(index)
            return True
        raise IndexError("Invalid column index")
        
    def get_columns(self):
        return self.columns
    
    def highlight_column(self, column, highlight):
        container = column.controls[1].content  # The lists_container
        if highlight:
            container.border = ft.border.all(2, ft.Colors.BLUE)
        else:
            container.border = None
        container.update()