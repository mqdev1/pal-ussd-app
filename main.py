import flet as ft
from views.test_view import test_view

def main(page: ft.Page):
    page.title = "Mobile Routing Example"
    
    # 1. Handle Route Changes (Pushing Views)
    def route_change(e: ft.RouteChangeEvent):
        # Clear existing stack to rebuild cleanly based on the path
        page.views.clear()
        
        # Always keep the root/home view at the bottom of the stack
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.AppBar(title=ft.Text("Home Screen"), bgcolor=ft.Colors.SURFACE_TINT),
                    ft.ElevatedButton("Go to Settings", on_click=lambda _: page.go("/settings")),
                    ft.ElevatedButton("Go to Test", on_click=lambda _: page.go("/test")),
                ],
            )
        )
        
        # Push the Settings view on top if matched
        if page.route == "/settings":
            page.views.append(
                ft.View(
                    route="/settings",
                    controls=[
                        ft.AppBar(title=ft.Text("Settings"), bgcolor=ft.Colors.SURFACE_TINT),
                        ft.Text("Welcome to the settings screen!"),
                        ft.ElevatedButton("Go Back", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        
        if page.route == '/test':
            page.views.append(test_view(page))
        
        page.update()

    # 2. Handle Mobile Back Button (Popping Views)
    def view_pop(e: ft.ViewPopEvent):
        # Remove the top view from the stack
        page.views.pop()
        # Find the route of the new top view
        top_view = page.views[-1]
        # Update current page route and refresh UI
        page.go(top_view.route)

    # Assign event listeners
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Initialize the app on the starting route
    page.go(page.route)

ft.app(target=main)
