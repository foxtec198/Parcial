import sys
from textual.app import App
from textual.widgets import Button, Input, Label, Header, Footer
from textual.containers import Container

class WAuth(App):
    BINDINGS = [('s ','sair()','Sair da Aplicação')]
    CSS = """
    Container{
        layout: vertical;
        align: center middle;
        text-align: center;
    }
    Label {
        margin: 5 50;
        text-align: center;
        align: center middle;
        width: 100%;
    }
    Input{
        margin: 5 50;
        width: 100%;
    }
    Button {
        align: center middle;
        width: 100%;
        margin: 0 70;
    }
    """
    def compose(self):
        with Container():
            yield Header(show_clock=True)
            yield Label('Digite o horário que deseja iniciar os envios de parciais!', id = 'texto')
            yield Input('08')
            yield Button('Iniciar')
            yield Footer()

    def action_sair(self):
        sys.exit()
class BackEnd:
    ...

if __name__ == '__main__':
    WAuth().run()