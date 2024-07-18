from authWA import Parcial

p = Parcial('guilherme.breve','8458@Guilherme198','10.56.6.56','Vista_Replication_PRD')

dds = (
    lambda: p.whats.enviar_msg(
        'GPS Vista - PR - Regional Denise', # Escalonadas
        f'Aqui estão as *ATIVIDADES ESCALONADAS* do app GPS Vista, na gestão Denise. \n\n DATA: {p.date} - {p.time}',
        p.whats.criar_imagem_SQL_GGPS("""SELECT cr.Gerente, Es.Nivel_03 as 'CR', count(cr.Gerente) as 'Escalonadas'
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
        'GPS Vista - LDA & MGA', # Escalonadas
        f'Aqui estão as *VISITAS REALIZADS* do app GPS Vista. \n\n DATA: {p.date} - {p.time}',
        p.whats.criar_imagem_SQL_GGPS(f"""SELECT DISTINCT 
        R.NOME AS SUPERVISOR, COUNT(T.Nome) as TOTAL
        FROM TAREFA T
        INNER JOIN RECURSO R
            ON R.CODIGOHASH = T.FINALIZADOPORHASH
        INNER JOIN DW_VISTA.dbo.DM_ESTRUTURA ES
            ON ES.ID_ESTRUTURA = T.ESTRUTURAID
        INNER JOIN DW_VISTA.dbo.DM_CR CR
            ON CR.ID_CR = ES.ID_CR
        WHERE CR.Gerente IN (
            'DENISE DOS SANTOS DIAS SILVA',
            'DANIEL ALVES DE OLIVEIRA',
            'CLAYTON MARTINS DAMASCENO'
        )
        AND T.ChecklistId in (
            '7c7d1611-01f5-4f6a-9652-4e24bb1ce07a',
            '21368b38-a8f5-4793-8317-aca40a9489a5',
            '71bb4fa9-6f30-45df-9461-4b01534fbc12',
            'd44ee96b-262e-4d6e-b4a6-861cf0663c3e',
            '460e6d74-a6fe-4128-bc84-3d0455d30f45'
        )
        AND MONTH(TERMINOREAL) = {p.month}
        AND YEAR(TERMINOREAL) = {p.year}
        GROUP BY R.NOME
        ORDER BY TOTAL DESC
        """)
    ),
    lambda: p.whats.enviar_msg(
        'GPS Vista - FCP', # Escalonadas
        f'Aqui estão as *VISITAS REALIZADS* do app GPS Vista. \n\n DATA: {p.date} - {p.time}',
        p.whats.criar_imagem_SQL_GGPS(f"""
        SELECT DISTINCT
        R.NOME AS SUPERVISOR,
        COUNT(T.Nome) as TOTAL
        FROM TAREFA T
        INNER JOIN RECURSO R
            ON R.CODIGOHASH = T.FINALIZADOPORHASH
        INNER JOIN DW_VISTA.dbo.DM_ESTRUTURA ES
            ON ES.ID_ESTRUTURA = T.ESTRUTURAID
        INNER JOIN DW_VISTA.dbo.DM_CR CR
            ON CR.ID_CR = ES.ID_CR
        WHERE CR.Gerente IN (
            'GLEISSON EVANGELISTA DE OLIVEIRA'
        )
        AND T.ChecklistId in (
            '7c7d1611-01f5-4f6a-9652-4e24bb1ce07a',
            '21368b38-a8f5-4793-8317-aca40a9489a5',
            '71bb4fa9-6f30-45df-9461-4b01534fbc12',
            'd44ee96b-262e-4d6e-b4a6-861cf0663c3e',
            '460e6d74-a6fe-4128-bc84-3d0455d30f45'
        )
        AND MONTH(TERMINOREAL) = {p.month}
        AND YEAR(TERMINOREAL) = {p.year}
        GROUP BY R.NOME
        ORDER BY TOTAL DESC
        """)
    ),
    
)

fds = [
    lambda: p.whats.enviar_msg(
        'GPS Vista - PR - Regional Denise', # Escalonadas
        f'Aqui estão as *ATIVIDADES ESCALONADAS* do app GPS Vista, na gestão Denise. \n\n DATA: {p.date} - {p.time}',
        p.whats.criar_imagem_SQL_GGPS("""SELECT cr.Gerente, Es.Nivel_03 as 'CR', count(cr.Gerente) as 'Escalonadas'
        FROM Tarefa T WITH(NOLOCK)
        INNER join dw_vista.dbo.DM_ESTRUTURA Es WITH(NOLOCK) on Es.Id_estrutura = T.EstruturaId
        INNER join dw_vista.dbo.DM_CR cr WITH(NOLOCK) on cr.Id_cr = es.Id_cr
        WHERE cr.GerenteRegional = 'DENISE DOS SANTOS DIAS SILVA'
        AND T.Escalonado > 0
        AND T.Status <> 85
        GROUP BY cr.Gerente, Es.Nivel_03
        ORDER BY cr.Gerente, [Escalonadas] DESC""")
    ),
]

main = []
main.append(dds)
main.append(fds)
p.main_loop(main)