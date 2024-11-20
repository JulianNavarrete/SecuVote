import flet as ft
from services.api import login


class LoginView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.initialize_view()

    def initialize_view(self):
        self.dni_field = ft.TextField(
            label="DNI",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_icon=ft.icons.PERSON_OUTLINE,
            helper_text="Ingresa tu DNI"
        )

        self.password_field = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.icons.LOCK_OUTLINE,
        )

        self.login_button = ft.ElevatedButton(
            text="Iniciar Sesión",
            width=200,
            on_click=self.handle_login
        )

        self.register_button = ft.TextButton(
            text="¿No tienes cuenta? Regístrate",
            on_click=lambda _: self.page.go("/register")
        )

        self.controls = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("SecuVote", size=32, weight=ft.FontWeight.BOLD),
                        ft.Text("Sistema de votación seguro", size=16),
                        self.dni_field,
                        self.password_field,
                        self.login_button,
                        self.register_button
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                padding=ft.padding.all(30),
                alignment=ft.alignment.center
            )
        ]

    async def handle_login(self, e):
        try:
            dni = int(self.dni_field.value)
            password = self.password_field.value

            if not dni or not password:
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Por favor complete todos los campos"))
                )
                return

            result = await login(dni, password)
            
            if result:
                # Save the token in the local storage
                self.page.client_storage.set("access_token", result["access_token"])
                self.page.client_storage.set("refresh_token", result["refresh_token"])
                self.page.go("/home")
            else:
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("DNI o contraseña incorrectos"))
                )

        except ValueError:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("El DNI debe ser un número"))
            )

