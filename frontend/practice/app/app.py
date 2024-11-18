import flet as ft
import os
import base64


def create_product(name, price, color, picture_name):
    picture_path = os.path.join("assets", picture_name)
    try:
        with open(picture_path, "rb") as picture_file:
            picture_bytes = base64.b64encode(picture_file.read()).decode()
    except FileNotFoundError:
        print(f"Picture file {picture_name} not found")
        picture_bytes = None
    return ft.Container(
        content=ft.Column([
            ft.Image(
                src_base64=picture_bytes,
                width=150,
                height=150,
                fit=ft.ImageFit.CONTAIN,
                error_content=ft.Text("Picture not found", color=ft.colors.WHITE)) if picture_bytes else ft.Text("Picture not found", color=ft.colors.WHITE),
            ft.Text(value=name, size=16, weight=ft.FontWeight.BOLD),
            ft.Text(value=price, size=14),
            ft.ElevatedButton(text="Add to Cart", color=ft.colors.WHITE),
        ]),
        bgcolor=color,
        border_radius=10,
        padding=20,
        alignment=ft.alignment.center,
    )


def main(page: ft.Page):
    page.title = "Responsive Products Gallery" # This is for the browser tab
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.colors.BLUE_GREY_900

    title = ft.Text(value="Products Gallery", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)

    products = [
        create_product("Product 1", "$19.99", ft.colors.BLUE_500, "product1.jpg"),
        create_product("Product 2", "$29.99", ft.colors.GREEN_500, "product2.jpeg"),
        create_product("Product 3", "$39.99", ft.colors.RED_500, "product3.jpg"),
        create_product("Product 4", "$49.99", ft.colors.PURPLE_500, "product4.jpg"),
        create_product("Product 5", "$59.99", ft.colors.YELLOW_500, "product5.jpg"),
        create_product("Product 6", "$69.99", ft.colors.ORANGE_500, "product6.jpg"),
        create_product("Product 7", "$79.99", ft.colors.PINK_500, "product7.jpeg"),
        create_product("Product 8", "$89.99", ft.colors.PURPLE_500, "product8.webp"),
    ]

    gallery = ft.ResponsiveRow(
        [ft.Container(product, col={"sm": 12, "md": 6, "lg": 3}) for product in products],
        spacing=20,
        run_spacing=20,
    )

    content = ft.Column(controls=[
        ft.Text(value="Products Gallery", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ft.Divider(height=20, color=ft.colors.BLUE_GREY_900),
        gallery,
    ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    page.add(content)

ft.app(target=main)
