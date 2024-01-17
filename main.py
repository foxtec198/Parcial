from tkinter import *
from tkinter import PhotoImage
from parcial import Parcial
from time import strftime as st, sleep
from datetime import datetime as dt

class FrontEnd:
    def __init__(self):
        self.win = Tk()
        self.bg = '#333'
        self.fg = '#fff'
        self.win['bg'] = self.bg
        self.win.resizable(False, False)
        self.win.geometry('300x200')
        self.widgets()
        self.place_widgets()
        self.win.mainloop()

    def widgets(self):
        self.lbl = Label(
            self.win,
            text='Digite em qual horario deseja iniciar o servidor!',
            bg = self.bg, fg = self.fg
        )
        self.horaEnt = Entry(self.win)
        self.btn = Button(
            self.win,
            text='INICIAR',
            command=self.action,
        )

    def place_widgets(self):
        self.lbl.place(x=20, y=50)
        self.horaEnt.place(x=80, y=100)
        self.btn.place(x= 120, y = 160)

    def action(self):
        b.play(self.horaEnt.get())

class BackEnd:
    def __init__(self) -> None:
        self.horaInicio = 8
        self.horaInicioFixed = self.horaInicio
        self.horaFinal = 18

    def play(self, ent):
        if ent != '':
            self.horaInicio = int(ent)
            self.hash()
    
    def hash(self):
        while True:
            hora = int(st('%H'))
            horario = st('%H:%M:%S')
            day = st('%d')
            month = st('%m')
            year = st('%Y')
            nameOfMonth = st('%h')
            now = st('%d/%m/%Y - %H:%M')
            
            # MOZIN
            if horario == '08:30:00':
                p.msg(nome='97908929', mensagem='''Bom diaaaaa meu amor, meu tudo 🥰❤
        Não esqueça de pegar a aliança, de tomar seu café.
        O ônibus passa *08:40* você tem 5min pra sair, se não ira perder o ônibus.''')
            
            # DIURNO
            if hora == self.horaInicio and hora <= 18:
                p.atalho('alt','tab')
                # FIEP - DENISE
                p.make(nome='ENCARREGADAS GPS',
                    legenda=f'Segue realizado até o momento {now} - *FIEP*',
                    consulta=f"""SELECT
                    (CASE WHEN T.Status = 10 THEN 'ABERTA' ELSE
                    (CASE WHEN T.Status = 85 THEN 'FINALIZADA' ELSE
                    (CASE WHEN T.Status = 25 THEN 'INICIADA' END) END) END) as 'status',
                    T.Nome, 
                    COUNT(T.Nome) as 'Total'
                    FROM Tarefa T
                    INNER JOIN Dw_vista.dbo.DM_ESTRUTURA ES ON ES.ID_ESTRUTURA = T.EstruturaId
                    WHERE ES.CRNo = 13223           
                    AND T.Nome LIKE '%INSPEÇÃO%'
                    AND DAY(T.Disponibilizacao) = {day}
                    AND MONTH(T.Disponibilizacao) = {month}
                    AND YEAR(T.Disponibilizacao) = {year}
                    GROUP BY T.[Status], T.Nome
                    ORDER BY T.[Status], [Total] DESC""")
                #FIEP - JOSIEL
                p.make(nome='Liderança GPS/FIEP',
                    legenda=f'Segue tarefas Realizadas/Abertas *FIEP* {now}',
                    consulta=f"""SELECT
                    (CASE WHEN T.Status = 10 THEN 'ABERTA' ELSE
                    (CASE WHEN T.Status = 85 THEN 'FINALIZADA' ELSE
                    (CASE WHEN T.Status = 25 THEN 'INICIADA' END) END) END) as 'status',
                    T.Nome, 
                    COUNT(T.Nome) as 'Total'
                    FROM Tarefa T
                    INNER JOIN Dw_vista.dbo.DM_ESTRUTURA ES ON ES.ID_ESTRUTURA = T.EstruturaId
                    WHERE ES.CRNo = 11930
                    AND T.Nome LIKE '%INSPEÇÃO%'
                    AND DAY(T.Disponibilizacao) = {day}
                    AND MONTH(T.Disponibilizacao) = {month}
                    AND YEAR(T.Disponibilizacao) = {year}
                    GROUP BY T.[Status], T.Nome
                    ORDER BY T.[Status], [Total] DESC""")
                # Visitas
                p.make(nome='GPS Vista - Projetos Londrina',
                    legenda=f'Segue Visitas Realizadas Até o Momento - {now}',
                    consulta=f"""select R.Nome as 'Sup', Es.Nivel_03 as 'CR ', TerminoReal as 'Data de Finalização' 
                    from Tarefa T
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join DW_Vista.dbo.DM_Estrutura Es on Es.Id_Estrutura = T.EstruturaId
                    inner join DW_Vista.dbo.DM_CR cr on cr.Id_CR = Es.ID_Cr
                    where T.Nome LIKE '%Visita%'
                    and Cr.Gerente = 'DENISE DOS SANTOS DIAS SILVA'
                    and DAY(T.TerminoReal) = {day}
                    and MONTH(T.TerminoReal) = {month}
                    and YEAR(T.TerminoReal) = {year}""")

                self.horaInicio += 1
                p.atalho('alt','tab')
            # FINAL
            if self.horaInicio > 23:
                self.horaInicio = self.horaInicioFixed

if __name__ == '__main__':
    p = Parcial()
    b = BackEnd()
    FrontEnd()