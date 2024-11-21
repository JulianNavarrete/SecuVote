import flet as ft
from services.api import get_elections, get_candidates


class HomeView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.initialize_view()

    def initialize_view(self):
        self.app_bar = ft.AppBar(
            title=ft.Text("SecuVote"),
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(
                    icon=ft.icons.LOGOUT,
                    tooltip="Cerrar sesión",
                    on_click=self.handle_logout
                ),
            ],
        )

        self.elections_list = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
        )

        self.refresh_button = ft.FloatingActionButton(
            icon=ft.icons.REFRESH,
            on_click=self.load_elections
        )

        self.controls = [
            self.app_bar,
            ft.Text(
                "Elecciones Disponibles",
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            ),
            self.elections_list,
            self.refresh_button
        ]

        # Load elections on startup
        self.page.add(ft.ProgressRing())
        self.load_elections(None)

    async def load_elections(self, e):
        self.elections_list.controls.clear()
        elections = await get_elections()
        
        if elections:
            for election in elections:
                self.elections_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.HOW_TO_VOTE),
                                        title=ft.Text(election["name"]),
                                        subtitle=ft.Text(election["description"]),
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.TextButton(
                                                text="Ver candidatos",
                                                on_click=lambda e, id=election["id"]: 
                                                    self.show_candidates(id)
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.END,
                                    ),
                                ],
                            ),
                            padding=10,
                        )
                    )
                )
        else:
            self.elections_list.controls.append(
                ft.Text("No hay elecciones disponibles")
            )
        
        self.page.update()

    async def show_candidates(self, election_id: str):
        candidates = await get_candidates(election_id)
        
        if not candidates:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Error al cargar candidatos"))
            )
            return

        # Navigate to the vote view with the necessary data
        self.page.go(f"/vote?election_id={election_id}")

    def handle_logout(self, e):
        self.page.session.remove("access_token")
        self.page.session.remove("refresh_token")
        self.page.go("/login")

