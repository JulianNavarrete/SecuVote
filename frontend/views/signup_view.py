import flet as ft

from app_state import AppState
from services.api_client import ApiClient


def build(page: ft.Page, state: AppState, api: ApiClient) -> ft.View:
    email_field = ft.TextField(label="Email", hint_text="Ingresa tu email", width=300, keyboard_type=ft.KeyboardType.EMAIL)
    dni_field = ft.TextField(label="DNI", hint_text="Ingresa tu DNI", width=300, keyboard_type=ft.KeyboardType.NUMBER)
    password_field = ft.TextField(label="Contraseña", password=True, width=300)
    confirm_field = ft.TextField(label="Confirmar contraseña", password=True, width=300)

    def on_signup(_: ft.ControlEvent) -> None:
        if not all([email_field.value, dni_field.value, password_field.value, confirm_field.value]):
            _snack(page, "Completa todos los campos")
            return
        if password_field.value != confirm_field.value:
            _snack(page, "Las contraseñas no coinciden")
            return
        try:
            dni_int = int(dni_field.value)
        except ValueError:
            _snack(page, "DNI inválido")
            return

        ok, data = api.signup(email_field.value, dni_int, password_field.value)
        if ok:
            _snack(page, "Usuario registrado. Inicia sesión")
            page.go("/login")
        else:
            _snack(page, str(data))

    return ft.View(
        "/signup",
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Registro", size=28, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        email_field,
                        dni_field,
                        password_field,
                        confirm_field,
                        ft.Container(height=10),
                        ft.ElevatedButton(text="Registrarse", width=300, on_click=on_signup),
                        ft.TextButton(text="Volver al login", on_click=lambda e: page.go("/login")),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def _snack(page: ft.Page, msg: str) -> None:
    page.snack_bar = ft.SnackBar(content=ft.Text(msg), action="OK")
    page.snack_bar.open = True
    page.update()



