-- select distinct cr.Gerente, es.Nivel_03 as CR, COUNT(T.Escalonado) as 'Escalonadas'
-- from Tarefa T
-- inner join dw_vista.dbo.DM_ESTRUTURA es on es.Id_Estrutura = T.EstruturaId
-- inner join dw_vista.dbo.DM_CR cr on cr.Id_CR = Es.Id_CR
-- where cr.Gerente = 'DENISE DOS SANTOS DIAS SILVA'
-- and T.Escalonado >= 2
-- and DAY(T.Prazo) = 26
-- and MONTH(T.Prazo) = 01
-- and YEAR(T.Prazo) = 2024 
-- GROUP BY cr.Gerente, es.Nivel_03
-- ORDER BY [Escalonadas] DESC


-- select T.Nome, T.Origem from Tarefa T
-- where T.Numero = 36806489

-- 30R,32F,48C

select 
T.Nome, R.Nome as 'Colaborador',
(CASE WHEN T.Status = 10 THEN 'ABERTA' ELSE
(CASE WHEN T.Status = 85 THEN 'FINALIZADA' ELSE
(CASE WHEN T.Status = 25 THEN 'INICIADA' END) END) END) as 'status',
(CASE WHEN T.Origem = 30 THEN 'ROTINA' ELSE
(CASE WHEN T.Origem = 32 THEN 'FLUXO' ELSE
(CASE WHEN T.Origem = 48 THEN 'CHAMADO' END) END) END) as 'Origem', Es.Descricao
from Tarefa T with(nolock)
inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
inner join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on es.Id_Estrutura = T.EstruturaId
inner join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_CR = Es.Id_CR
where cr.Gerente = 'denise dos santos dias silva'
and es.PECNo = 098629 
and T.Nome = 'Visita Oper. Liderança'
and MONTH(Disponibilizacao) = 01
and YEAR(Disponibilizacao) = 2024
ORDER BY [Status]
