import flet as ft
from services.api import register


class RegisterView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.initialize_view()

    def initialize_view(self):
        self.email_field = ft.TextField(
            label="Email",
            keyboard_type=ft.KeyboardType.EMAIL,
            prefix_icon=ft.icons.EMAIL_OUTLINED,
            helper_text="ejemplo@correo.com"
        )

        self.dni_field = ft.TextField(
            label="DNI",
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_icon=ft.icons.BADGE_OUTLINED,
            helper_text="Ingresa tu DNI"
        )

        self.password_field = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.icons.LOCK_OUTLINE,
            helper_text="Mínimo 5 caracteres"
        )

        self.confirm_password_field = ft.TextField(
            label="Confirmar Contraseña",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.icons.LOCK_OUTLINE,
        )

        self.register_button = ft.ElevatedButton(
            text="Registrarse",
            width=200,
            on_click=self.handle_register
        )

        self.login_button = ft.TextButton(
            text="¿Ya tienes cuenta? Inicia Sesión",
            on_click=lambda _: self.page.go("/login")
        )

        self.controls = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Registro", size=32, weight=ft.FontWeight.BOLD),
                        self.email_field,
                        self.dni_field,
                        self.password_field,
                        self.confirm_password_field,
                        self.register_button,
                        self.login_button
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                padding=ft.padding.all(30),
                alignment=ft.alignment.center
            )
        ]

    async def handle_register(self, e):
        try:
            if not all([
                self.email_field.value,
                self.dni_field.value,
                self.password_field.value,
                self.confirm_password_field.value
            ]):
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Por favor completa todos los campos"))
                )
                return

            if self.password_field.value != self.confirm_password_field.value:
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Las contraseñas no coinciden"))
                )
                return

            dni = int(self.dni_field.value)
            result = await register(
                email=self.email_field.value,
                dni=dni,
                password=self.password_field.value
            )

            if result:
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Registro exitoso"))
                )
                self.page.go("/login")
            else:
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Error en el registro"))
                )

        except ValueError:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("El DNI debe ser un número"))
            )

