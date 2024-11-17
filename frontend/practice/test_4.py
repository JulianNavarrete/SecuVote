import flet as ft


def main(page: ft.Page):
    page.title = "Sticky-note board"
    page.bgcolor = ft.colors.BLUE_GREY_800
    page.padding = 20
    page.theme_mode = "light"

    def add_note(text):
        new_note = create_note("New note")
        grid.controls.append(new_note)
        page.update()
    
    def delete_note(note):
        grid.controls.remove(note)
        page.update()

    '''    
    def create_note(text):
        return ft.Container(
            content=ft.TextField(value=text, multiline=True),
            width=200,
            height=200,
            bgcolor=ft.colors.YELLOW_900,
            border_radius=10,
            padding=10,
            # expand=1
        )
    '''

    def create_note(text):
        note_content = ft.TextField(value=text, multiline=True,
                                    bgcolor=ft.colors.BLUE_GREY_50)
        note = ft.Container(
            content=ft.Column([note_content, ft.IconButton(icon=ft.icons.DELETE, on_click=lambda _: delete_note(note))]),
            width=200,
            height=200,
            bgcolor=ft.colors.YELLOW_900,
            border_radius=10,
            padding=10,
        )
        return note

    # note = ft.TextField(value="My first note", multiline=True, width=400, height=400)
    # note = create_note("Hi there!")
    # note2 = create_note("My second enhanced note")
    
    grid = ft.GridView(
        expand=True,
        max_extent=220,
        # horizontal=True,
        child_aspect_ratio=1,
        spacing=10, # between rows
        run_spacing=10, # between columns
    )
    
    notes = [
        "Buy milk",
        "Buy eggs",
        "Meeting 3 PM",
        "Buy a super high end desktop PC with a RTX 4090 GPU",
    ]

    # page.add(ft.Row(notes))
    for note in notes:
        grid.controls.append(create_note(note))
    
    
    page.add(ft.Row([
        ft.Text("My sticky notes", size=24, weight="bold",
                color=ft.colors.WHITE),
        ft.IconButton(icon=ft.icons.ADD, on_click=add_note, icon_color=ft.colors.WHITE),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), grid)


ft.app(target=main)
