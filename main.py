from parcial import *

p = Parcial()

class BackEnd:
    def run(self):
        horaInicio = p.getHour()
        while True:
            p.init() # Inicializa o App

            if p.horaC >= "08:00:00" and p.horaC <= "08:00:05": # Eventos
                p.msg(nome='Eventos', mensagem='Segue seus eventos mais recentes! 📆', img= p.event.criar_imagem())

            if p.horaC >= "08:30:00" and p.horaC <= "08:30:10": # Mozin
                p.msg(nome='Meu Amor ❤❤', mensagem='Bom diaaaaa meu amor ❤ \n\nNão se esqueça de pegar a aliança e tomar café ☕💍 \nSeu busão passa 08:40 então esteja pronta 🚋 \nTih Amuhhh ❤❤')
                
            if p.hora == horaInicio and p.hora <= mudarTurno: # DIURNO
                # ESCALONADAS
                p.make(
                    nome = 'GPS Vista - PR - Regional Denise' ,
                    legenda= f'Aqui esta as tarefas escalonadas do app GPS Vista, nivel Denise na {p.now}',
                    consulta= '''select cr.Gerente, Es.Nivel_03 as 'CR', count(cr.Gerente) as 'Escalonadas'
                    from Tarefa T with(nolock)
                    inner join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
                    inner join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
                    where cr.GerenteRegional = 'DENISE DOS SANTOS DIAS SILVA'
                    and T.Escalonado > 0
                    and T.Status <> 85
                    GROUP BY cr.Gerente, Es.Nivel_03
                    ORDER BY cr.Gerente, [Escalonadas] DESC
                    ''', fimDeSemana=True)

                #FIEP - DENISE
                p.make(nome='ENCARREGADAS GPS',
                    legenda=f'Segue Realizadas/Abertas {p.now} - *FIEP* 🧹🧼',
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
                    AND DAY(T.Disponibilizacao) = {p.day}
                    AND MONTH(T.Disponibilizacao) = {p.month}
                    AND YEAR(T.Disponibilizacao) = {p.year}
                    GROUP BY T.[Status], T.Nome
                    ORDER BY T.[Status], [Total] DESC""")
                
                #FIEP - JOSIEL
                p.make(nome='Liderança GPS/FIEP',
                    legenda=f'Segue tarefas Realizadas/Abertas *FIEP* {p.now} 🧹🧼',
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
                    AND DAY(T.Disponibilizacao) = {p.day}
                    AND MONTH(T.Disponibilizacao) = {p.month}
                    AND YEAR(T.Disponibilizacao) = {p.year}
                    GROUP BY T.[Status], T.Nome
                    ORDER BY T.[Status], [Total] DESC""")
                
                # VISITAS DIA - LDA
                p.make(nome='GPS Vista - LDA',
                    legenda=f'Segue Visitas Realizadas Até o Momento - {p.now}',
                    consulta=f"""select R.Nome as 'Sup', Es.Nivel_03 as 'CR ', TerminoReal as 'Data de Finalização' 
                    from Tarefa T
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join DW_Vista.dbo.DM_Estrutura Es on Es.Id_Estrutura = T.EstruturaId
                    inner join DW_Vista.dbo.DM_CR cr on cr.Id_CR = Es.ID_Cr
                    where T.Nome LIKE '%Visita %'
                    and R.Nome <> 'Sistema'
                    and Cr.Gerente = 'CLAYTON MARTINS DAMASCENO'
                    and DAY(T.TerminoReal) = {p.day}
                    and MONTH(T.TerminoReal) = {p.month}
                    and YEAR(T.TerminoReal) = {p.year}""")

                # VISITA MES LDA
                p.make(
                    nome='GPS Vista - LDA',
                    legenda=f'Segue Visitas Realizas Mes de {p.nameOfMonth}',
                    consulta=f"""
                    select R.Nome as Sup, COUNT(R.Nome)  as Realizado
                    from Tarefa T
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura Es on Es.Id_Estrutura = T.EstruturaId
                    inner join dw_vista.dbo.DM_CR c on c.Id_cr = Es.Id_cr
                    where c.Gerente = 'CLAYTON MARTINS DAMASCENO'
                    and T.Nome LIKE '%Visita %' 
                    and month(TerminoReal) = {p.month}
                    and YEAR(TerminoReal) = {p.year}
                    GROUP BY R.Nome
                    ORDER BY COUNT(R.Nome) DESC""")

                # VISITAS ABERTAS/INICIADAS - LDA
                p.make(
                    nome='GPS Vista - LDA',
                    legenda=f'Segue Visitas Operacionais *ABERTAS/INICIADAS* para {p.nameOfMonth}! 🚧',
                    consulta=f"""select Cliente, COUNT(Cliente) as 'Total'
                    from Tarefa T with(nolock)
                    inner join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
                    inner join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
                    where cr.Gerente = 'CLAYTON MARTINS DAMASCENO'
                    and T.Nome = 'Visita Oper. Liderança'
                    and MONTH(Disponibilizacao) = {p.month}
                    and YEAR(Disponibilizacao) = {p.year}
                    and T.Status >= 10
                    and T.Status <= 25
                    GROUP BY Cliente
                    ORDER BY [Total] DESC""")
                
                # VISITAS DIA - MGA
                p.make(nome='GPS Vista - MGA',
                    legenda=f'Segue Visitas Realizadas Até o Momento - {p.now}',
                    consulta=f"""select R.Nome as 'Sup', Es.Nivel_03 as 'CR ', TerminoReal as 'Data de Finalização' 
                    from Tarefa T
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join DW_Vista.dbo.DM_Estrutura Es on Es.Id_Estrutura = T.EstruturaId
                    inner join DW_Vista.dbo.DM_CR cr on cr.Id_CR = Es.ID_Cr
                    where T.Nome LIKE '%Visita %'
                    and Cr.Gerente = 'DENISE DOS SANTOS DIAS SILVA'
                    and DAY(T.TerminoReal) = {p.day}
                    and MONTH(T.TerminoReal) = {p.month}
                    and YEAR(T.TerminoReal) = {p.year}""")

                # VISITA MES MGA
                p.make(
                    nome='GPS Vista - MGA',
                    legenda=f'Segue Visitas Realizas Mes de {p.nameOfMonth}',
                    consulta=f"""
                    select R.Nome as Sup, COUNT(R.Nome)  as Realizado
                    from Tarefa T
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura Es on Es.Id_Estrutura = T.EstruturaId
                    inner join dw_vista.dbo.DM_CR c on c.Id_cr = Es.Id_cr
                    where c.Gerente = 'DENISE DOS SANTOS DIAS SILVA'
                    and T.Nome LIKE '%Visita %' 
                    and R.Nome <> 'Sistema'
                    and month(TerminoReal) = {p.month}
                    and YEAR(TerminoReal) = {p.year}
                    GROUP BY R.Nome
                    ORDER BY COUNT(R.Nome) DESC""")

                # VISITAS ABERTAS/INICIADAS - MGA
                p.make(
                    nome='GPS Vista - MGA',
                    legenda=f'Segue Visitas Operacionais *ABERTAS/INICIADAS* para {p.nameOfMonth}! 🚧',
                    consulta=f"""select Cliente, COUNT(Cliente) as 'Total'
                    from Tarefa T with(nolock)
                    inner join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
                    inner join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
                    where cr.Gerente = 'DENISE DOS SANTOS DIAS SILVA'
                    and T.Nome = 'Visita Oper. Liderança'
                    and MONTH(Disponibilizacao) = {p.month}
                    and YEAR(Disponibilizacao) = {p.year}
                    and T.Status >= 10
                    and T.Status <= 25
                    GROUP BY Cliente
                    ORDER BY [Total] DESC""")
                
                # VISITAS DIA - JSL
                p.make(nome='GPS Vista - JSL',
                    legenda=f'Segue Visitas Realizadas Até o Momento - {p.now}',
                    consulta=f"""select R.Nome as 'Sup', Es.Nivel_03 as 'CR ', TerminoReal as 'Data de Finalização' 
                    from Tarefa T
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join DW_Vista.dbo.DM_Estrutura Es on Es.Id_Estrutura = T.EstruturaId
                    inner join DW_Vista.dbo.DM_CR cr on cr.Id_CR = Es.ID_Cr
                    where T.Nome LIKE '%Visita %'
                    and Cr.Gerente = 'JOSIEL CESAR RIBAS DE OLIVEIRA'
                    and DAY(T.TerminoReal) = {p.day}
                    and MONTH(T.TerminoReal) = {p.month}
                    and YEAR(T.TerminoReal) = {p.year}""")

                # VISITA MES JSL
                p.make(
                    nome='GPS Vista - JSL',
                    legenda=f'Segue Visitas Realizas Mes de {p.nameOfMonth}',
                    consulta=f"""
                    select R.Nome as Sup, COUNT(R.Nome)  as Realizado
                    from Tarefa T
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura Es on Es.Id_Estrutura = T.EstruturaId
                    inner join dw_vista.dbo.DM_CR c on c.Id_cr = Es.Id_cr
                    where c.Gerente = 'JOSIEL CESAR RIBAS DE OLIVEIRA'
                    and T.Nome LIKE '%Visita %' 
                    and R.Nome <> 'Sistema'
                    and month(TerminoReal) = {p.month}
                    and YEAR(TerminoReal) = {p.year}
                    GROUP BY R.Nome
                    ORDER BY COUNT(R.Nome) DESC""")

                # VISITAS ABERTAS/INICIADAS - JSL
                p.make(
                    nome='GPS Vista - JSL',
                    legenda=f'Segue Visitas Operacionais *ABERTAS/INICIADAS* para {p.nameOfMonth}! 🚧',
                    consulta=f"""select Cliente, COUNT(Cliente) as 'Total'
                    from Tarefa T with(nolock)
                    inner join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
                    inner join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
                    where cr.Gerente = 'JOSIEL CESAR RIBAS DE OLIVEIRA'
                    and T.Nome = 'Visita Oper. Liderança'
                    and MONTH(Disponibilizacao) = {p.month}
                    and YEAR(Disponibilizacao) = {p.year}
                    and T.Status >= 10
                    and T.Status <= 25
                    GROUP BY Cliente
                    ORDER BY [Total] DESC""")
                
                # PRESENTEISMO BK
                p.make(
                    nome='Alinhamentos BK - Londrina e Maringá',legenda='Segue *Tarefas Inicias BK* Realizadas!',
                    consulta=f"""select Es.Descricao,
                    (CASE WHEN R.Nome = 'Sistema' THEN 'FINALIZADO PELO SISTEMA' END) as 'Colaborador', 
                    T.TerminoReal as 'Data de Realização'
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
                    inner join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
                    where cr.GerenteRegional = 'DENISE DOS SANTOS DIAS SILVA'
                    and cr.Gerente <> 'JOSIEL CESAR RIBAS DE OLIVEIRA'
                    and T.Nome = 'TAREFA INICIAL BK'
                    and DAY(TerminoReal) = {p.day}
                    and MONTH(TerminoReal) = {p.month}
                    and YEAR(TerminoReal) = 2024""", fimDeSemana=True)
                
                # LOGGI
                p.make(nome='Gps/ loggi',
                    legenda=f"Segue rondas realizadas até {p.now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 24158
                    and DAY(TerminoReal) = {p.day}
                    and MONTH(TerminoReal) = {p.month}
                    and YEAR(TerminoReal) = {p.year}
                    and R.Nome <> 'Sistema'
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True
                    )
                
                # LONGPING
                p.make(nome='Longping - GPS',
                    legenda=f"Segue rondas realizadas até {p.now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 42610
                    and DAY(TerminoReal) = {p.day}
                    and MONTH(TerminoReal) = {p.month}
                    and R.Nome <> 'Sistema'
                    and YEAR(TerminoReal) = {p.year}
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True)
                
                # M DIAS - SEG
                p.make(nome='Seg Patrimonial Paraná',
                    legenda=f"Segue rondas realizadas até {p.now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 15073
                    and DAY(TerminoReal) = {p.day}
                    and MONTH(TerminoReal) = {p.month}
                    and YEAR(TerminoReal) = {p.year}
                    and R.Nome <> 'Sistema'
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True)
                
                # CARGILL MARINGA 
                p.make(nome='Cargill Maringá',
                    legenda=f"Segue rondas realizadas até {p.now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 35900
                    and DAY(TerminoReal) = {p.day}
                    and MONTH(TerminoReal) = {p.month}
                    and YEAR(TerminoReal) = {p.year}
                    and R.Nome <> 'Sistema'
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True)
                    
                horaInicio += 1
            elif p.hora == horaInicio and p.hora >= 19: # NOTURNO
                #LOGGI
                p.make(nome='Gps/ loggi',
                    legenda=f"Segue rondas realizadas até {p.now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 24158
                    and DAY(TerminoReal) = {p.day}
                    and MONTH(TerminoReal) = {p.month}
                    and YEAR(TerminoReal) = {p.year}
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True)
                #LONGPING
                p.make(nome='Longping - GPS',
                    legenda=f"Segue rondas realizadas até {p.now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 42610
                    and DAY(TerminoReal) = {p.day}
                    and MONTH(TerminoReal) = {p.month}
                    and YEAR(TerminoReal) = {p.year}
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True)
                # M DIAS
                p.make(nome='Seg Patrimonial Paraná',
                    legenda=f"Segue rondas realizadas até {p.now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 15073
                    and DAY(TerminoReal) = {p.day}
                    and MONTH(TerminoReal) = {p.month}
                    and YEAR(TerminoReal) = {p.year}
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True)
                # CARGILL MARINGA
                p.make(nome='Cargill Maringá',
                    legenda=f"Segue rondas realizadas até {p.now}",
                    consulta=f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
                    from Tarefa T with(nolock)
                    inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
                    inner join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
                    where Es.CRNo = 35900
                    and DAY(TerminoReal) = {p.day}
                    and MONTH(TerminoReal) = {p.month}
                    and YEAR(TerminoReal) = {p.year}
                    and R.Nome <> 'Sistema'
                    GROUP BY T.Nome, T.Descricao, R.Nome
                    ORDER BY [Total] DESC""", fimDeSemana=True)
                
                horaInicio += 1
            elif p.hora ==  horaFinal: horaInicio = horaInicioFixed # THE END
            else: p.display() # DISPLAY HOUR

if __name__ == '__main__':
    BackEnd().run()
