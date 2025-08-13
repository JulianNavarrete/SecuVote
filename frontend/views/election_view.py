import flet as ft

from typing import List, Dict
from app_state import AppState
from services.api_client import ApiClient


def build(page: ft.Page, state: AppState, api: ApiClient) -> ft.View:
    if not state.current_election:
        return _error_view("Elección no encontrada")

    candidates_list = ft.ListView(expand=True, spacing=10, padding=20)

    def load():
        candidates_list.controls.clear()
        ok_c, candidates = api.election_candidates(state.current_election["id"])  # type: ignore[index]
        ok_v, votes = api.list_votes()

        vote_counts: dict[str, int] = {}
        if ok_v and isinstance(votes, list):
            for v in votes:
                if v.get("election") == state.current_election.get("id"):
                    cid = v.get("candidate")
                    vote_counts[cid] = vote_counts.get(cid, 0) + 1

        if not ok_c or not isinstance(candidates, list):
            candidates_list.controls.append(_error_card(str(candidates)))
        else:
            for c in candidates:
                count = vote_counts.get(c.get("id"), 0)
                candidates_list.controls.append(_candidate_card(c, count))

            if _can_vote(state, votes if ok_v and isinstance(votes, list) else []):
                candidates_list.controls.append(
                    ft.Container(
                        alignment=ft.alignment.center,
                        padding=20,
                        content=ft.ElevatedButton(text="Votar", width=300, on_click=lambda e: page.go("/vote")),
                    )
                )
            else:
                candidates_list.controls.append(
                    ft.Container(
                        alignment=ft.alignment.center,
                        padding=20,
                        content=ft.Text("Ya has votado en esta elección", color=ft.colors.GREY),
                    )
                )

        page.update()

    app_bar = ft.AppBar(
        title=ft.Text(f"Elección: {state.current_election.get('name', '')}"),
        leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: page.go("/home")),
    )

    view = ft.View(
        "/election",
        [
            app_bar,
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(state.current_election.get("name", ""), size=24, weight=ft.FontWeight.BOLD),
                        ft.Text(state.current_election.get("description", "")),
                        ft.Text("Candidatos:", size=18, weight=ft.FontWeight.BOLD),
                        candidates_list,
                    ]
                ),
                padding=20,
            ),
        ],
    )

    load()
    return view


def _candidate_card(candidate: dict, count: int) -> ft.Card:
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PERSON),
                        title=ft.Text(candidate.get("name", ""), weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"Partido: {candidate.get('party', '')}"),
                    ),
                    ft.Container(content=ft.Text(f"Votos: {count}"), padding=ft.padding.only(left=16, bottom=10)),
                ]
            ),
            padding=10,
        )
    )


def _can_vote(state: AppState, votes: List[Dict]) -> bool:
    if not (state.access_token and state.current_user and state.current_election):
        return False
    for v in votes:
        if v.get("election") == state.current_election.get("id") and v.get("voter") == str(state.current_user.get("user_id")):
            return False
    return True


def _error_card(msg: str) -> ft.Card:
    return ft.Card(content=ft.Container(content=ft.Text(msg), padding=10))


def _error_view(msg: str) -> ft.View:
    return ft.View(
        "/error",
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.ERROR, size=64, color=ft.colors.RED),
                        ft.Text(msg),
                        ft.ElevatedButton(text="Volver", on_click=lambda e: None),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
            )
        ],
    )


