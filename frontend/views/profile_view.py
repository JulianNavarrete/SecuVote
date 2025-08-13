import flet as ft

from app_state import AppState
from services.api_client import ApiClient


def build(page: ft.Page, state: AppState, api: ApiClient) -> ft.View:
    if not state.current_user:
        return _error_view("Usuario no encontrado")

    email_field = ft.TextField(label="Email", value=state.current_user.get("email", ""), width=300, read_only=True)
    dni_field = ft.TextField(label="DNI", value=str(state.current_user.get("dni", "")), width=300, read_only=True)
    first_field = ft.TextField(label="Nombre", value=state.current_user.get("first_name", ""), width=300)
    last_field = ft.TextField(label="Apellido", value=state.current_user.get("last_name", ""), width=300)

    def on_update(_: ft.ControlEvent) -> None:
        ok, data = api.update_user(state.access_token or "", first_field.value, last_field.value)
        if ok:
            state.set_user(data if isinstance(data, dict) else state.current_user)
            _snack(page, "Perfil actualizado")
        else:
            _snack(page, str(data))

    return ft.View(
        "/profile",
        [
            ft.AppBar(title=ft.Text("Mi perfil"), leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: page.go("/home"))),
            ft.Container(
                content=ft.Column([
                    ft.Text("Información del usuario", size=22, weight=ft.FontWeight.BOLD),
                    email_field,
                    dni_field,
                    first_field,
                    last_field,
                    ft.ElevatedButton(text="Actualizar", width=300, on_click=on_update),
                    ft.TextButton(text="Volver", on_click=lambda e: page.go("/home")),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center,
                padding=20,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def _snack(page: ft.Page, msg: str) -> None:
    page.show_snack_bar(ft.SnackBar(content=ft.Text(msg), action="OK"))


def _error_view(msg: str) -> ft.View:
    return ft.View(
        "/error",
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.icons.ERROR, size=64, color=ft.colors.RED),
                        ft.Text(msg),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
            )
        ],
    )



