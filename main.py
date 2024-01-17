from parcial import Parcial
from time import strftime as st, sleep
from datetime import datetime as dt
from os import system

class BackEnd:
    def __init__(self) -> None:
        self.horaInicio = 8
        self.horaInicioFixed = self.horaInicio
        self.horaFinal = 18

    def run(self):
        ent = input('Horario: ')
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

            else:
                print(st('%X'))
                sleep(1)
                system('cls')

if __name__ == '__main__':
    p = Parcial()
    BackEnd().run()