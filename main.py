from authWA import Parcial

p = Parcial('guilherme.breve','84584608-Gui','10.56.6.56','Vista_Replication_PRD')

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