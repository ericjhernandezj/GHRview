"""
GHRview - GitHub Repo View
Author: Eric J. Hernandez J. (hello@ericjhernandezj.com)
"""

import requests
import base64

from textual.app import App, ComposeResult
from textual.screen import Screen

from textual.containers import VerticalScroll, Center
from textual.widgets import Label, Markdown, Header


def get_repo_info(owner_name: str, repo_name: str) -> dict:
    base_url = "https://api.github.com"

    repo = requests.get(f'{base_url}/repos/{owner_name}/{repo_name}')
    repo_content_readme = requests.get(f'{base_url}/repos/{owner_name}/{repo_name}/contents/README.md')
    owner = requests.get(f'{base_url}/users/{owner_name}')

    if repo.status_code != 200:
        raise Exception()

    repo_info = {
        "repo_name" : repo.json()["name"],
        "owner_name" : owner.json()["name"],
        "owner_username" : owner.json()["login"],
        "repo_description" : repo.json()["description"],
        "repo_homepage" : repo.json()["homepage"],
        "repo_license": repo.json()["license"]["name"],
        "repo_readme": base64.b64decode(repo_content_readme.json()["content"]).decode('utf-8'),
    }

    return repo_info


data = get_repo_info("facebook", "react")

class MainScreen(Screen):
    DEFAULT_CSS = '''
        Header {
            margin-bottom: 1;
        }

        #main-column {
            margin-top: 1;
        }
        
        .readme-render {
            margin: 1 3 0 3;
        }
    '''

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)

        yield Center(
                Label(
                    renderable=f"[bold]{data['repo_name']}[/bold] by [bold]{data['owner_name']} (@{data['owner_username']})[/bold]",
                    shrink=True
                )
        )
        yield Center(
                Label(
                    renderable=f"\"[italic]{data['repo_description']}[/italic]\"",
                    shrink=True
                )
        )
        yield Center(
                Label(
                    renderable=f"{data['repo_homepage']}",
                    shrink=True
                )
        )
        yield Center(
                Label(
                    renderable=f"License: {data['repo_license']}",
                    shrink=True
                )
        )

        with VerticalScroll(id="main-column"):
            yield Center(
                Label(
                    renderable="[bold]README[/bold]",
                    shrink=True
                )
            )
            yield Markdown(
                data["repo_readme"],
                open_links=False,
                classes="readme-render"
            )


class GHRviewApp(App):
    def on_mount(self) -> None:
        self.push_screen(MainScreen())
        self.theme = "tokyo-night"


if __name__ == "__main__":
    app = GHRviewApp()
    app.run()
