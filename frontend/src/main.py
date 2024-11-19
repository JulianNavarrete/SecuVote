import flet as ft
from views.login import LoginView
# from views.register import RegisterView
# from views.home import HomeView
# from views.vote import VoteView


def main(page: ft.Page):
    # Basic configuration of the page
    page.title = "SecuVote"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    page.window.width = 400
    page.window.height = 800
    
    def route_change(route):
        page.views.clear()
        
        if page.route == "/login":
            page.views.append(LoginView(page))
    #     elif page.route == "/register":
    #         page.views.append(RegisterView(page))
    #     elif page.route == "/home":
    #         page.views.append(HomeView(page))
    #     elif page.route == "/vote":
    #         page.views.append(VoteView(page))
    #     else:
    #         page.views.append(LoginView(page))
            
        page.update()

    page.on_route_change = route_change
    page.go('/login')

ft.app(target=main, assets_dir="assets")

