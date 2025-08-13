import flet as ft

from app_state import AppState
from services.api_client import ApiClient


def build(page: ft.Page, state: AppState, api: ApiClient) -> ft.View:
    dni_field = ft.TextField(label="DNI", hint_text="Ingresa tu DNI", width=300, keyboard_type=ft.KeyboardType.NUMBER)
    password_field = ft.TextField(label="Contraseña", hint_text="Ingresa tu contraseña", password=True, width=300)

    def on_login(_: ft.ControlEvent) -> None:
        if not dni_field.value or not password_field.value:
            _snack(page, "Completa todos los campos")
            return
        ok, data = api.login(dni_field.value, password_field.value)
        if ok:
            token = data.get("access_token")
            state.set_token(token)
            ok_me, me = api.me(token) if token else (False, None)
            if ok_me:
                state.set_user(me)
                page.go("/home")
            else:
                _snack(page, str(me))
        else:
            _snack(page, str(data))

    def on_forgot(_: ft.ControlEvent) -> None:
        _snack(page, "Recuperación no implementada aún")

    login_button = ft.ElevatedButton(text="Iniciar sesión", width=300, on_click=on_login)
    signup_button = ft.TextButton(text="¿No tienes cuenta? Regístrate", on_click=lambda e: page.go("/signup"))
    forgot_button = ft.TextButton(text="¿Olvidaste tu contraseña?", on_click=on_forgot)

    return ft.View(
        "/login",
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("SecuVote", size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Text("Sistema de Votación", size=16, text_align=ft.TextAlign.CENTER),
                        ft.Divider(),
                        ft.Container(height=20),
                        dni_field,
                        ft.Container(height=10),
                        password_field,
                        ft.Container(height=20),
                        login_button,
                        ft.Container(height=10),
                        signup_button,
                        forgot_button,
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



