import flet as ft


def main(page: ft.Page):
    page.bgcolor = ft.colors.BLUE_GREY_800
    page.title = "My tasks list"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    title = ft.Text(value="My tasks list with Flet",
                    size=30, weight=ft.FontWeight.BOLD)

    tasks = []

    def add_task(e):
        if task_field.value:
            task = ft.ListTile(title=ft.Text(task_field.value),
                               leading=ft.Checkbox(on_change=select_task))
            tasks.append(task)
            task_field.value = ""
            update_list()

    def select_task(e):
        selected = [t.title.value for t in tasks if t.leading.value]
        selected_tasks.value = "Selected tasks: " + ", ".join(selected)
        page.update()

    def update_list():
        list_tasks.controls.clear()
        list_tasks.controls.extend(tasks)
        page.update()

    task_field = ft.TextField(hint_text="Enter a task", width=1000)
    add_button = ft.FilledButton(text="Add task", on_click=add_task)
    list_tasks = ft.ListView(expand=1, spacing=10)
    selected_tasks = ft.Text(value="", size=20, weight=ft.FontWeight.BOLD)

    page.add(title, task_field, add_button, list_tasks, selected_tasks)

ft.app(target=main)

