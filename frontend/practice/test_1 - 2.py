import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "SecuVote"

    text = ft.Text(value="Hello, World!", size=24, color=ft.colors.BLUE_100)
    text2 = ft.Text(value="Hello, World 2!", size=24, color=ft.colors.BLUE_100)
    text3 = ft.Text(value="Hello, World 3!", size=24, color=ft.colors.BLUE_100)
    # page.add(text, text2, text3)

    text_rows = ft.Row(
        controls=[text, text2, text3],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(text_rows)

    button1 = ft.FilledButton(text="Button 1")
    button2 = ft.FilledButton(text="Button 2")
    button3 = ft.FilledButton(text="Button 3")

    button_row = ft.Row(
        controls=[button1, button2, button3],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50,
    )
    page.add(button_row)

    column_texts1 = [
        ft.Text(value="Columna 1 - Fila 1", size=20, color=ft.colors.WHITE),
        ft.Text(value="Columna 1 - Fila 2", size=20, color=ft.colors.WHITE),
        ft.Text(value="Columna 1 - Fila 3", size=20, color=ft.colors.WHITE),
    ]

    column_text1 = ft.Column(
        controls=column_texts1,
        alignment=ft.MainAxisAlignment.CENTER,
    )


    column_texts2 = [
        ft.Text(value="Columna 2 - Fila 1", size=20, color=ft.colors.WHITE),
        ft.Text(value="Columna 2 - Fila 2", size=20, color=ft.colors.WHITE),
        ft.Text(value="Columna 2 - Fila 3", size=20, color=ft.colors.WHITE),
    ]

    column_text2 = ft.Column(
        controls=column_texts2,
    )

    row_columns = ft.Row(
        controls=[column_text1, column_text2],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50,
    )
    page.add(row_columns)

    
ft.app(target=main)

