from parcial import Parcial
from time import strftime as st, sleep
from os import system

class BackEnd:
    def __init__(self):
        self.horaInicio = 8
        self.horaFinal = 7
        self.horaInicioFixed = self.horaInicio

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
                p.msg(nome='Meu Amor ❤❤❤', mensagem='''Bom diaaaaa meu amor, meu tudo 🥰❤ Não esqueça de pegar a aliança, de tomar seu café. O ônibus passa *08:40* você tem 5min pra sair, se não ira perder o ônibus.''')
            
            # DIURNO
            if hora == self.horaInicio and hora <= 18:
                p.atalho('alt','tab')
                p.make(
                    nome = 'GPS Vista - PR - Regional Denise' ,
                    legenda= f'Aqui esta as tarefas escalonadas do app GPS Vista, nivel Denise na {now}',
                    consulta= '''
                    select cr.Gerente, Es.Nivel_03 as 'CR', count(cr.Gerente) as 'Escalonadas'
                    from Tarefa T with(nolock)
                    inner join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
                    inner join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
                    where cr.GerenteRegional = 'denise dos santos dias silva'
                    and T.Escalonado > 0
                    and T.Status <> 85
                    GROUP BY cr.Gerente, Es.Nivel_03
                    ORDER BY cr.Gerente, [Escalonadas] DESC
                    ''',
                )
                #FIEP - DENISE
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
                #Visitas
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
                #Visitas Mes
                p.make(
                    nome='GPS Vista - Projetos Londrina',
                    legenda=f'Segue Visitas Realizas Mes de {nameOfMonth}',
                    consulta=f"""
                    select R.Nome as Sup, COUNT(R.Nome)  as Realizado
                    from Tarefa T
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura Es on Es.Id_Estrutura = T.EstruturaId
                    inner join dw_vista.dbo.DM_CR c on c.Id_cr = Es.Id_cr
                    where c.Gerente = 'DENISE DOS SANTOS DIAS SILVA'
                    and T.Nome LIKE '%Visita %' 
                    and month(Disponibilizacao) = {month}
                    and YEAR(T.Disponibilizacao) = {year}
                    GROUP BY R.Nome
                    ORDER BY COUNT(R.Nome) DESC""")
                #LOGGI
                p.make(nome='Gps/ loggi',
                    legenda=f"Segue rondas realizadas até {now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 24158
                    and DAY(TerminoReal) = {day}
                    and MONTH(TerminoReal) = {month}
                    and YEAR(TerminoReal) = {year}
                    and R.Nome <> 'Sistema'
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True
                    )
                #LONGPING
                p.make(nome='Longping - GPS',
                    legenda=f"Segue rondas realizadas até {now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 42610
                    and DAY(TerminoReal) = {day}
                    and MONTH(TerminoReal) = {month}
                    and R.Nome <> 'Sistema'
                    and YEAR(TerminoReal) = {year}
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True)
                # M DIAS
                p.make(nome='Seg Patrimonial Paraná',
                    legenda=f"Segue rondas realizadas até {now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 15073
                    and DAY(TerminoReal) = {day}
                    and MONTH(TerminoReal) = {month}
                    and YEAR(TerminoReal) = {year}
                    and R.Nome <> 'Sistema'
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True)
                # CARGILL MARINGA 
                p.make(nome='Cargill Maringá',
                    legenda=f"Segue rondas realizadas até {now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 35900
                    and DAY(TerminoReal) = {day}
                    and MONTH(TerminoReal) = {month}
                    and YEAR(TerminoReal) = {year}
                    and R.Nome <> 'Sistema'
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True)
                
                p.atalho('alt','tab')
                self.horaInicio += 1

            if hora == self.horaInicio and hora >= 19:
                p.atalho('alt','tab')
                #LOGGI
                p.make(nome='Gps/ loggi',
                    legenda=f"Segue rondas realizadas até {now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 24158
                    and DAY(TerminoReal) = {day}
                    and MONTH(TerminoReal) = {month}
                    and YEAR(TerminoReal) = {year}
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True)
                #LONGPING
                p.make(nome='Longping - GPS',
                    legenda=f"Segue rondas realizadas até {now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 42610
                    and DAY(TerminoReal) = {day}
                    and MONTH(TerminoReal) = {month}
                    and YEAR(TerminoReal) = {year}
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True)
                # M DIAS
                p.make(nome='Seg Patrimonial Paraná',
                    legenda=f"Segue rondas realizadas até {now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 15073
                    and DAY(TerminoReal) = {day}
                    and MONTH(TerminoReal) = {month}
                    and YEAR(TerminoReal) = {year}
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True)
                # cargill maringa
                p.make(nome='Cargill Maringá',
                    legenda=f"Segue rondas realizadas até {now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 35900
                    and DAY(TerminoReal) = {day}
                    and MONTH(TerminoReal) = {month}
                    and YEAR(TerminoReal) = {year}
                    and R.Nome <> 'Sistema'
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True)
                
                self.horaInicio += 1
                p.atalho('alt','tab')

            # FINAL
            if hora == self.horaFinal:
                self.horaInicio = self.horaInicioFixed

            else:
                print(st('%X'))
                sleep(1)
                system('cls')

if __name__ == '__main__':
    p = Parcial()
    BackEnd().run()