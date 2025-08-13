import flet as ft

from typing import Callable

from views.login_view import build as build_login
from views.signup_view import build as build_signup
from views.home_view import build as build_home
from views.election_view import build as build_election
from views.vote_view import build as build_vote
from views.profile_view import build as build_profile
from services.api_client import ApiClient
from app_state import AppState


def main(page: ft.Page):
    state = AppState()
    api = ApiClient()

    page.title = "SecuVote"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 800
    page.window_resizable = False
    page.padding = 20

    builders: dict[str, Callable[[], ft.View]] = {
        "/login": lambda: build_login(page, state, api),
        "/signup": lambda: build_signup(page, state, api),
        "/home": lambda: build_home(page, state, api),
        "/election": lambda: build_election(page, state, api),
        "/vote": lambda: build_vote(page, state, api),
        "/profile": lambda: build_profile(page, state, api),
    }

    def handle_route_change(e: ft.RouteChangeEvent):
        route = e.route
        page.views.clear()
        build = builders.get(route, builders["/login"])  # vista por defecto
        page.views.append(build())
        page.update()

    page.on_route_change = handle_route_change
    page.go("/login")


if __name__ == "__main__":
    ft.app(target=main)



