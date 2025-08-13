import flet as ft

from app_state import AppState
from services.api_client import ApiClient


def build(page: ft.Page, state: AppState, api: ApiClient) -> ft.View:
    if not state.current_election:
        return _error_view("Elección no encontrada")

    candidates_list = ft.ListView(expand=True, spacing=10, padding=20)

    def load():
        ok, data = api.election_candidates(state.current_election["id"])  # type: ignore[index]
        candidates_list.controls.clear()
        if not ok or not isinstance(data, list):
            candidates_list.controls.append(_error_card(str(data)))
        else:
            for c in data:
                candidates_list.controls.append(_vote_card(page, state, api, c))
        page.update()

    app_bar = ft.AppBar(title=ft.Text("Votar"), leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: page.go("/election")))

    view = ft.View(
        "/vote",
        [
            app_bar,
            ft.Container(
                content=ft.Column([
                    ft.Text("Selecciona tu candidato:", size=22, weight=ft.FontWeight.BOLD),
                    candidates_list,
                ]),
                padding=20,
            ),
        ],
    )

    load()
    return view


def _vote_card(page: ft.Page, state: AppState, api: ApiClient, candidate: dict) -> ft.Card:
    def on_vote(_: ft.ControlEvent) -> None:
        ok, msg = api.vote(state.access_token or "", candidate.get("id", ""), state.current_election.get("id", ""))  # type: ignore[arg-type]
        if ok:
            page.snack_bar = ft.SnackBar(content=ft.Text("¡Voto registrado!"), action="OK")
            page.snack_bar.open = True
            page.update()
            page.go("/election")
        else:
            message = str(msg)
            if "already voted" in message.lower():
                page.snack_bar = ft.SnackBar(content=ft.Text("Ya has votado en esta elección"), action="OK")
                page.snack_bar.open = True
                page.update()
                page.go("/election")
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text(message), action="OK")
                page.snack_bar.open = True
                page.update()

    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PERSON),
                        title=ft.Text(candidate.get("name", ""), weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"Partido: {candidate.get('party', '')}"),
                    ),
                    ft.Row([
                        ft.ElevatedButton(text="Votar por este candidato", on_click=on_vote)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ]
            ),
            padding=10,
        )
    )


def _error_card(msg: str) -> ft.Card:
    return ft.Card(content=ft.Container(content=ft.Text(msg), padding=10))


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


