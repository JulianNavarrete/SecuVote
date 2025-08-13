import flet as ft

from app_state import AppState
from services.api_client import ApiClient


def build(page: ft.Page, state: AppState, api: ApiClient) -> ft.View:
    elections_list = ft.ListView(expand=True, spacing=10, padding=20)

    def load():
        elections_list.controls.clear()
        ok, data = api.list_elections()
        if not ok:
            elections_list.controls.append(_error_card(str(data)))
        else:
            for election in data:
                elections_list.controls.append(_election_card(page, state, election))
        page.update()

    app_bar = ft.AppBar(
        title=ft.Text("Elecciones disponibles"),
        actions=[
            ft.IconButton(icon=ft.Icons.PERSON, on_click=lambda e: page.go("/profile")),
            ft.IconButton(icon=ft.Icons.LOGOUT, on_click=lambda e: _logout(page, state)),
        ],
    )

    view = ft.View(
        "/home",
        [
            app_bar,
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Bienvenido a SecuVote", size=22, weight=ft.FontWeight.BOLD),
                        ft.Text("Selecciona una elección para ver detalles"),
                        elections_list,
                    ]
                ),
                padding=20,
            ),
        ],
    )

    load()
    return view


def _logout(page: ft.Page, state: AppState) -> None:
    state.set_token(None)
    state.set_user(None)
    state.set_election(None)
    page.go("/login")


def _election_card(page: ft.Page, state: AppState, election: dict) -> ft.Card:
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.HOW_TO_VOTE),
                        title=ft.Text(election.get("name", ""), weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(election.get("description", "")),
                    ),
                    ft.Row(
                        [
                            ft.TextButton(
                                text="Ver detalles",
                                on_click=lambda e, el=election: _go_election(page, state, el),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ]
            ),
            padding=10,
        )
    )


def _go_election(page: ft.Page, state: AppState, election: dict) -> None:
    state.set_election(election)
    page.go("/election")


def _error_card(msg: str) -> ft.Card:
    return ft.Card(content=ft.Container(content=ft.Text(msg), padding=10))



