from authWA import Parcial, conectar_email

p = Parcial('guilherme.breve', '8458Guilherme','10.56.6.56', 8, 23)
conectar_email('foxtec198@gmail.com','vewmksduxchpjirg')
master = []

# Dias de Semana
dds = (
    lambda: p.whats.enviar_msg(
        'GPS Vista - PR - Regional Denise', # Escalonadas
        f'Aqui esta as tarefas escalonadas do app GPS Vista, nivel Denise na {p.now}',
        p.whats.criar_imagem_SQL("""
        SELECT cr.Gerente, Es.Nivel_03 as 'CR', count(cr.Gerente) as 'Escalonadas'
        FROM Tarefa T WITH(NOLOCK)
        INNER join dw_vista.dbo.DM_ESTRUTURA Es WITH(NOLOCK) on Es.Id_estrutura = T.EstruturaId
        INNER join dw_vista.dbo.DM_CR cr WITH(NOLOCK) on cr.Id_cr = es.Id_cr
        WHERE cr.GerenteRegional = 'DENISE DOS SANTOS DIAS SILVA'
        AND T.Escalonado > 0
        AND T.Status <> 85
        GROUP BY cr.Gerente, Es.Nivel_03
        ORDER BY cr.Gerente, [Escalonadas] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'ENCARREGADAS GPS', # FIEP DENISE
        f'Segue Realizadas/Abertas {p.now} - *FIEP* 🧹🧼',
        p.whats.criar_imagem_SQL(f"""SELECT
        (CASE WHEN T.Status = 10 THEN 'ABERTA' ELSE
        (CASE WHEN T.Status = 85 THEN 'FINALIZADA' ELSE
        (CASE WHEN T.Status = 25 THEN 'INICIADA' END) END) END) as 'status',
        T.Nome, 
        COUNT(T.Nome) as 'Total'
        FROM Tarefa T WITH(NOLOCK)
        INNER JOIN Dw_vista.dbo.DM_ESTRUTURA ES WITH(NOLOCK) ON ES.ID_ESTRUTURA = T.EstruturaId
        WHERE ES.CRNo = 13223
        AND T.Nome LIKE '%INSPEÇÃO%'
        AND DAY(T.Disponibilizacao) = {p.day}
        AND MONTH(T.Disponibilizacao) = {p.month}
        AND YEAR(T.Disponibilizacao) = {p.year}
        GROUP BY T.[Status], T.Nome
        ORDER BY T.[Status], [Total] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'Liderança GPS/FIEP', # FIEP JOSIEL
        f'Segue tarefas Realizadas/Abertas *FIEP* {p.now} 🧹🧼',
        p.whats.criar_imagem_SQL(f"""SELECT
        (CASE WHEN T.Status = 10 THEN 'ABERTA' ELSE
        (CASE WHEN T.Status = 85 THEN 'FINALIZADA' ELSE
        (CASE WHEN T.Status = 25 THEN 'INICIADA' END) END) END) as 'status',
        T.Nome, 
        COUNT(T.Nome) as 'Total'
        FROM Tarefa T WITH(NOLOCK)
        INNER JOIN Dw_vista.dbo.DM_ESTRUTURA ES WITH(NOLOCK) ON ES.ID_ESTRUTURA = T.EstruturaId
        WHERE ES.CRNo = 11930
        AND T.Nome LIKE '%INSPEÇÃO%'
        AND DAY(T.Disponibilizacao) = {p.day}
        AND MONTH(T.Disponibilizacao) = {p.month}
        AND YEAR(T.Disponibilizacao) = {p.year}
        GROUP BY T.[Status], T.Nome
        ORDER BY T.[Status], [Total] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'GPS Vista - LDA & MGA', # VISITAS DIA
        f'Segue Visitas Realizadas Até o Momento - {p.now} 🌇🏦',
        p.whats.criar_imagem_SQL(f"""SELECT R.Nome as 'Sup', Es.Nivel_03 as 'CR ', TerminoReal as 'Data de Finalização' 
        FROM Tarefa T WITH(NOLOCK)
        INNER join Recurso R WITH(NOLOCK) on R.CodigoHash = T.FinalizadoPorHash
        INNER join DW_Vista.dbo.DM_Estrutura Es WITH(NOLOCK) on Es.Id_Estrutura = T.EstruturaId
        INNEr join DW_Vista.dbo.DM_CR cr WITH(NOLOCK) on cr.Id_CR = Es.ID_Cr
        WHERE T.Nome LIKE '%Visita %'
        AND R.Nome <> 'Sistema'
        AND cr.Gerente in(
            'DENISE DOS SANTOS DIAS SILVA',                     
            'CLAYTON MARTINS DAMASCENO'
            )
        AND DAY(T.TerminoReal) = {p.day}
        AND MONTH(T.TerminoReal) = {p.month}
        AND YEAR(T.TerminoReal) = {p.year}""")
    ),
    lambda: p.whats.enviar_msg(
        'GPS Vista - LDA & MGA ', # VISITAS MES
        'Segue Visitas Realizas neste Mês 📆',
        p.whats.criar_imagem_SQL(f"""SELECT R.Nome as Sup, COUNT(R.Nome)  as Realizado
        FROM Tarefa T WITH(NOLOCK)
        INNER join Recurso R WITH(NOLOCK) on R.CodigoHash = T.FinalizadoPorHash
        INNER join dw_vista.dbo.DM_Estrutura Es WITH(NOLOCK) on Es.Id_Estrutura = T.EstruturaId
        INNER join dw_vista.dbo.DM_CR c WITH(NOLOCK) on c.Id_cr = Es.Id_cr
        WHERE cr.Gerente IN (
            'DENISE DOS SANTOS DIAS SILVA',                     
            'CLAYTON MARTINS DAMASCENO'
            ) 
        AND T.Nome LIKE '%Visita %' 
        AND month(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}
        GROUP BY R.Nome
        ORDER BY COUNT(R.Nome) DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'GPS Vista - LDA & MGA', # VISITAS ABERTAS
        'Segue Visitas Operacionais *ABERTAS/INICIADAS NESTE MÊS!* 🚧',
        p.whats.criar_imagem_SQL(f"""SELECT Cliente, COUNT(Cliente) as 'Total'
        FROM Tarefa T with(nolock)
        INNER join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
        INNER join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
        WHERE cr.Gerente IN (
            'DENISE DOS SANTOS DIAS SILVA',                     
            'CLAYTON MARTINS DAMASCENO'
            ) 
        AND T.Nome = 'Visita Oper. Liderança'
        AND MONTH(Disponibilizacao) = {p.month}
        AND YEAR(Disponibilizacao) = {p.year}
        AND T.Status >= 10
        AND T.Status <= 25
        GROUP BY Cliente
        ORDER BY [Total] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'GPS Vista - FCP', # VISITAS DIA
        f'Segue Visitas Realizadas Até o Momento - {p.now} 🌇🏦',
        p.whats.criar_imagem_SQL(f"""SELECT R.Nome as 'Sup', Es.Nivel_03 as 'CR ', TerminoReal as 'Data de Finalização' 
        FROM Tarefa T WITH(NOLOCK)
        INNER join Recurso R WITH(NOLOCK) on R.CodigoHash = T.FinalizadoPorHash
        INNER join DW_Vista.dbo.DM_Estrutura Es WITH(NOLOCK) on Es.Id_Estrutura = T.EstruturaId
        INNER join DW_Vista.dbo.DM_CR cr WITH(NOLOCK) on cr.Id_CR = Es.ID_Cr
        WHERE T.Nome LIKE '%Visita %'
        AND Cr.Gerente = 'GLEISSON EVANGELISTA DE OLIVEIRA'
        AND DAY(T.TerminoReal) = {p.day}
        AND MONTH(T.TerminoReal) = {p.month}
        AND YEAR(T.TerminoReal) = {p.year}""")
    ),
    lambda: p.whats.enviar_msg(
        'GPS Vista - FCP', # VISITAS MES
        f'Segue Visitas Realizas deste mês! 📆',
        p.whats.criar_imagem_SQL(f"""SELECT R.Nome as Sup, COUNT(R.Nome)  as Realizado
        FROM Tarefa T WITH(NOLOCK)
        INNER join Recurso R WITH(NOLOCK) on R.CodigoHash = T.FinalizadoPorHash
        INNER join dw_vista.dbo.DM_Estrutura Es WITH(NOLOCK) on Es.Id_Estrutura = T.EstruturaId
        INNER join dw_vista.dbo.DM_CR c WITH(NOLOCK) on c.Id_cr = Es.Id_cr
        WHERE c.Gerente = 'GLEISSON EVANGELISTA DE OLIVEIRA'
        AND T.Nome LIKE '%Visita %' 
        AND R.Nome <> 'Sistema'
        AND month(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}
        GROUP BY R.Nome
        ORDER BY COUNT(R.Nome) DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'GPS Vista - FCP', # VISITAS ABERTAS
        f'Segue Visitas Operacionais *ABERTAS/INICIADAS DESTE MÊS!* 🚧',
        p.whats.criar_imagem_SQL(f"""SELECT Cliente, COUNT(Cliente) as 'Total'
        FROM Tarefa T with(nolock)
        INNER join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
        INNER join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
        WHERE cr.Gerente = 'GLEISSON EVANGELISTA DE OLIVEIRA'
        AND T.Nome = 'Visita Oper. Liderança'
        AND MONTH(Disponibilizacao) = {p.month}
        AND YEAR(Disponibilizacao) = {p.year}
        AND T.Status >= 10
        AND T.Status <= 25
        GROUP BY Cliente
        ORDER BY [Total] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'Alinhamentos BK - Londrina e Maringá', # BK PRESS
        'Segue *Tarefas Inicias BK* Realizadas!',
        p.whats.criar_imagem_SQL(f"""SELECT Es.Descricao,
        (CASE WHEN R.Nome = 'Sistema' THEN 'FINALIZADO PELO SISTEMA' ELSE R.Nome END) as 'Colaborador', 
        T.TerminoReal as 'Data de Realização'
        FROM Tarefa T with(nolock)
        INNER join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        INNER join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
        INNER join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
        WHERE cr.GerenteRegional = 'DENISE DOS SANTOS DIAS SILVA'
        AND cr.Gerente <> 'GLEISSON EVANGELISTA DE OLIVEIRA'
        AND T.Nome = 'TAREFA INICIAL BK'
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}""")
    ),
    lambda: p.whats.enviar_msg(
        'Burger King Cascavel/Foz', # BR PRESS
        'Segue *Tarefas Inicias BK* Realizadas!',
        p.whats.criar_imagem_SQL(f"""SELECT Es.Descricao,
        (CASE WHEN R.Nome = 'Sistema' THEN 'FINALIZADO PELO SISTEMA' ELSE R.Nome END) as 'Colaborador', 
        T.TerminoReal as 'Data de Realização'
        FROM Tarefa T with(nolock)
        INNER join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        INNER join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
        INNER join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
        WHERE cr.Gerente = 'GLEISSON EVANGELISTA DE OLIVEIRA'
        AND T.Nome = 'TAREFA INICIAL BK'
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}""")
    ),
    lambda: p.whats.enviar_msg(
        'Gps/ loggi', # LOGGI
        f"Segue rondas realizadas até {p.now}",
        p.whats.criar_imagem_SQL(f"""SELECT T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
        FROM Tarefa T with(nolock)
        INNER join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        INNER join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
        WHERE Es.CRNo = 24158
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}
        AND R.Nome <> 'Sistema'
        GROUP BY T.Nome, T.Descricao, R.Nome
        ORDER BY [Total] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'Longping - GPS', # LONGPING
        f"Segue rondas realizadas até {p.now}",
        p.whats.criar_imagem_SQL(f"""SELECT T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
        FROM Tarefa T with(nolock)
        INNER join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        INNER join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
        WHERE Es.CRNo = 42610
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND R.Nome <> 'Sistema'
        AND YEAR(TerminoReal) = {p.year}
        GROUP BY T.Nome, T.Descricao, R.Nome
        ORDER BY [Total] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'Seg Patrimonial Paraná', # M DIAS SEG
        f"Segue rondas realizadas até {p.now}",
        p.whats.criar_imagem_SQL(f"""SELECT T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
        FROM Tarefa T with(nolock)
        INNER join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        INNER join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
        WHERE Es.CRNo = 15073
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}
        AND R.Nome <> 'Sistema'
        GROUP BY T.Nome, T.Descricao, R.Nome
        ORDER BY [Total] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'Cargill Maringá', # CARGILL MARINGA
        f"Segue rondas realizadas até {p.now}",
        p.whats.criar_imagem_SQL(f"""SELECT T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
        FROM Tarefa T with(nolock)
        INNER join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        INNER join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
        WHERE Es.CRNo = 35900
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}
        AND R.Nome <> 'Sistema'
        GROUP BY T.Nome, T.Descricao, R.Nome
        ORDER BY [Total] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'Postos MagSeg', # MAGAZINE LUIZA
        f"Segue rondas realizadas até {p.now}",
        p.whats.criar_imagem_SQL(f"""SELECT DISTINCT T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
        FROM Tarefa T with(nolock)
        join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        join Execucao E on E.TarefaId = T.Id
        join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
        WHERE Es.CRNo = 11753
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}
        AND R.Nome <> 'Sistema'
        AND E.Conteudo = 'SIM'
        GROUP BY T.Nome, T.Descricao, R.Nome
        ORDER BY [Total] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'Postos MagSeg', # MAGAZINE LUIZA NÃO REALIZADO
        f"Segue relatório de *NÃO Realizadas* até {p.now}",
        p.whats.criar_imagem_SQL(f"""SELECT DISTINCT (T.TerminoReal) as 'Data', R.Nome as 'Vigilante', Es.Descricao as 'Local', E.Conteudo as 'Motivo'
        FROM Tarefa T with(nolock)
        join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        join Execucao E on E.TarefaId = T.Id
        join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
        WHERE Es.CRNo = 11753
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}
        AND R.Nome <> 'Sistema'
        AND E.PerguntaDescricao = 'INFORMAR O MOTIVO NO CAMPO ABAIXO.'""")
    ),
    lambda: p.whats.enviar_msg(
        'Agraria - GPS Vista', # Agraria
        f"Segue tarefas realizadas por local até {p.now}",
        p.whats.criar_imagem_SQL(f"""SELECT Es.Nivel_04 as 'Local',  
        COUNT(T.Nome) as 'Realizado'
        from Tarefa T
        INNER JOIN dw_vista.dbo.DM_Estrutura Es 
        on T.EstruturaId = Es.Id_estrutura
        WHERE Es.CRNo = 40859
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}
        GROUP by Es.Nivel_04
        ORDER BY [Realizado] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'GRUPO GPS / BAYER ROLANDIA',
        f'Entradas de Prestadores de Serviço ou Visitantes até {p.now}',
        f"""SELECT 
            Ex.Conteudo, 
            T.TerminoReal as 'Horario de Entrada'
        FROM Tarefa T with(nolock)
        inner join Execucao Ex with(nolock) 
            on Ex.TarefaId = T.Id
        WHERE T.EstruturaNivel2 LIKE '%42636 %'
        AND Ex.PerguntaDescricao = 'NOME COMPLETO'
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}"""
    ),
    lambda: p.whats.enviar_msg(
        'GRUPO GPS / BAYER ROLANDIA',
        f'Entradas de Prestadores de Serviço ou Visitantes até {p.now}',
        f"""SELECT
            Es.Descricao, 
            T.TerminoReal as 'Horario de Entrada'
        FROM Tarefa T with(nolock)
        INNER JOIN Execucao EX
            on Ex.TarefaId = T.Id
        INNER JOIN Estrutura Es 
            on Es.Id = T.EstruturaId
        WHERE T.EstruturaNivel2 LIKE '%42636 %'
        AND Ex.Conteudo = 'ENTRADA'
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}"""
    )
    )

# Fim de Semana
fds = [
    lambda: p.whats.enviar_msg(
        'GPS Vista - PR - Regional Denise',
        f'Aqui esta as tarefas escalonadas do app GPS Vista, nivel Denise na {p.now}',
        p.whats.criar_imagem_SQL('''
        SELECT cr.Gerente, Es.Nivel_03 as 'CR', count(cr.Gerente) as 'Escalonadas'
        FROM Tarefa T with(nolock)
        INNER join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
        INNER join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
        WHERE cr.GerenteRegional = 'DENISE DOS SANTOS DIAS SILVA'
        AND T.Escalonado > 0
        AND T.Status <> 85
        GROUP BY cr.Gerente, Es.Nivel_03
        ORDER BY cr.Gerente, [Escalonadas] DESC ''')
    ),
    lambda: p.whats.enviar_msg(
        'Alinhamentos BK - Londrina e Maringá',
        'Segue *Tarefas Inicias BK* Realizadas!',
        p.whats.criar_imagem_SQL(f"""SELECT Es.Descricao,
        (CASE WHEN R.Nome = 'Sistema' THEN 'FINALIZADO PELO SISTEMA' ELSE R.Nome END) as 'Colaborador', 
        T.TerminoReal as 'Data de Realização'
        FROM Tarefa T with(nolock)
        INNER join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        INNER join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
        INNER join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
        WHERE cr.Gerente IN (
            'DENISE DOS SANTOS DIAS SILVA','CLAYTON MARTINS DAMASCENO'
        )
        AND T.Nome = 'TAREFA INICIAL BK'
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}""")
    ),
    lambda: p.whats.enviar_msg(
        'Burger King Cascavel/Foz',
        'Segue *Tarefas Inicias BK* Realizadas!',
        p.whats.criar_imagem_SQL(f"""select Es.Descricao,
        (CASE WHEN R.Nome = 'Sistema' THEN 'FINALIZADO PELO SISTEMA' ELSE R.Nome END) as 'Colaborador', 
        T.TerminoReal as 'Data de Realização'
        FROM Tarefa T with(nolock)
        INNER join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        INNER join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
        INNER join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
        WHERE cr.Gerente = 'GLEISSON EVANGELISTA DE OLIVEIRA'
        AND T.Nome = 'TAREFA INICIAL BK'
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}""")
    ),
    lambda: p.whats.enviar_msg(
        'Gps/ loggi', # LOGGI
        f"Segue rondas realizadas até {p.now}",
        p.whats.criar_imagem_SQL(f"""SELECT T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
        FROM Tarefa T with(nolock)
        INNER join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        INNER join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
        WHERE Es.CRNo = 24158
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}
        AND R.Nome <> 'Sistema'
        GROUP BY T.Nome, T.Descricao, R.Nome
        ORDER BY [Total] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'Longping - GPS', # LONGPING
        f"Segue rondas realizadas até {p.now}",
        p.whats.criar_imagem_SQL(f"""SELECT T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
        FROM Tarefa T with(nolock)
        INNER join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        INNER join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
        WHERE Es.CRNo = 42610
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND R.Nome <> 'Sistema'
        AND YEAR(TerminoReal) = {p.year}
        GROUP BY T.Nome, T.Descricao, R.Nome
        ORDER BY [Total] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'Seg Patrimonial Paraná', # M DIAS SEG
        f"Segue rondas realizadas até {p.now}",
        p.whats.criar_imagem_SQL(f"""SELect T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
        FROM Tarefa T with(nolock)
        INNER join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        INNER join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
        WHERE Es.CRNo = 15073
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}
        AND R.Nome <> 'Sistema'
        GROUP BY T.Nome, T.Descricao, R.Nome
        ORDER BY [Total] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'Cargill Maringá', # CARGILL MARINGA
        f"Segue rondas realizadas até {p.now}",
        p.whats.criar_imagem_SQL(f"""select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
        FROM Tarefa T with(nolock)
        INNER join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        INNER join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
        WHERE Es.CRNo = 35900
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}
        AND R.Nome <> 'Sistema'
        GROUP BY T.Nome, T.Descricao, R.Nome
        ORDER BY [Total] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'Postos MagSeg', # MAGAZINE LUIZA
        f"Segue rondas realizadas até {p.now}",
        p.whats.criar_imagem_SQL(f"""SELECT DISTINCT T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
        FROM Tarefa T with(nolock)
        join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        join Execucao E on E.TarefaId = T.Id
        join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
        WHERE Es.CRNo = 11753
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}
        AND R.Nome <> 'Sistema'
        AND E.Conteudo = 'SIM'
        GROUP BY T.Nome, T.Descricao, R.Nome
        ORDER BY [Total] DESC""")
    ),
    lambda: p.whats.enviar_msg(
        'Postos MagSeg', # MAGAZINE LUIZA NÃO REALIZADO
        f"Segue relatório de *NÃO Realizadas* até {p.now}",
        p.whats.criar_imagem_SQL(f"""SELECT DISTINCT (T.TerminoReal) as 'Data', R.Nome as 'Vigilante', Es.Descricao as 'Local', E.Conteudo as 'Motivo'
        FROM Tarefa T with(nolock)
        join Recurso R on R.CodigoHash = T.FinalizadoPorHash
        join Execucao E on E.TarefaId = T.Id
        join dw_vista.dbo.DM_Estrutura as Es on T.EstruturaId = Es.Id_Estrutura
        WHERE Es.CRNo = 11753
        AND DAY(TerminoReal) = {p.day}
        AND MONTH(TerminoReal) = {p.month}
        AND YEAR(TerminoReal) = {p.year}
        AND R.Nome <> 'Sistema'
        AND E.PerguntaDescricao = 'INFORMAR O MOTIVO NO CAMPO ABAIXO.'""")
    ),
    
]

# Mensagem com __Horario_Exato__ e com Recorrencia
r = {
    '08:30:00': lambda: p.whats.enviar_msg(
        'Meu amor ❤❤❤', 
        '''Bom diaaaaa meu amor ❤
Não se esqueça de pegar a aliança e tomar café ☕💍
Seu busão passa 08:40 então esteja pronta 🚋 

Tih Amuhhh ❤❤'''
    )
}

master.append(dds)
master.append(fds)
master.append(r)
p.main_loop(master)