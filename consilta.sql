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

-- select 
-- T.Nome, R.Nome as 'Colaborador',
-- (CASE WHEN T.Status = 10 THEN 'ABERTA' ELSE
-- (CASE WHEN T.Status = 85 THEN 'FINALIZADA' ELSE
-- (CASE WHEN T.Status = 25 THEN 'INICIADA' END) END) END) as 'status',
-- (CASE WHEN T.Origem = 30 THEN 'ROTINA' ELSE
-- (CASE WHEN T.Origem = 32 THEN 'FLUXO' ELSE
-- (CASE WHEN T.Origem = 48 THEN 'CHAMADO' END) END) END) as 'Origem', Es.Descricao
-- from Tarefa T with(nolock)
-- inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
-- inner join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on es.Id_Estrutura = T.EstruturaId
-- inner join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_CR = Es.Id_CR
-- where cr.Gerente = 'denise dos santos dias silva'
-- and es.PECNo = 098629 
-- and T.Nome = 'Visita Oper. Liderança'
-- and MONTH(Disponibilizacao) = 01
-- and YEAR(Disponibilizacao) = 2024
-- ORDER BY [Status]

-- select T.Nome, T.Descricao, R.Nome as 'Vigilante', COUNT(R.Nome) as Total
-- from Tarefa T with(nolock)
-- inner join Recurso R with(nolock) on R.CodigoHash = T.FinalizadoPorHash
-- inner join dw_vista.dbo.DM_Estrutura Es with(nolock) on T.EstruturaId = Es.Id_Estrutura
-- where Es.CRNo = 35900
-- and DAY(TerminoReal) = 30
-- and MONTH(TerminoReal) = 01
-- and YEAR(TerminoReal) = 2024
-- and R.Nome <> 'Sistema'
-- GROUP BY T.Nome, T.Descricao, R.Nome
-- ORDER BY [Total] DESC

-- set nocount on
-- select cr.Gerente, Es.Nivel_03 as 'CR', count(cr.Gerente) as 'Escalonadas'
-- from Tarefa T with(nolock)
-- inner join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
-- inner join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
-- where cr.GerenteRegional = 'denise dos santos dias silva'
-- and T.Escalonado > 0
-- and T.Status <> 85
-- GROUP BY cr.Gerente, Es.Nivel_03
-- ORDER BY cr.Gerente, [Escalonadas] DESC

-- select T.Nome, R.Nome, T.TerminoReal as 'Data de Realização'
-- from Tarefa T with(nolock)
-- inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
-- inner join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
-- inner join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
-- where cr.Gerente = 'DENISE DOS SANTOS DIAS SILVA'
-- and T.Nome = 'TAREFA INICIAL BK'
-- and DAY(TerminoReal) = 01
-- and MONTH(TerminoReal) = 02
-- and YEAR(TerminoReal) = 2024

-- select 
-- Cliente,
-- COUNT(Cliente) as 'Total'
-- from Tarefa T with(nolock)
-- inner join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
-- inner join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
-- where cr.Gerente = 'DENISE DOS SANTOS DIAS SILVA'
-- and T.Nome = 'Visita Oper. Liderança'
-- and MONTH(Disponibilizacao) = 02
-- and YEAR(Disponibilizacao) = 2024
-- and T.Status >= 10
-- and T.Status <= 25
-- GROUP BY Cliente
-- ORDER BY [Total] 

-- select  R.Nome, count(T.Nome) as 'Total de Visitas'
-- from Tarefa T with(nolock)
-- inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
-- inner join dw_vista.dbo.DM_ESTRUTURA Es with(nolock) on Es.Id_estrutura = T.EstruturaId
-- inner join dw_vista.dbo.DM_CR cr with(nolock) on cr.Id_cr = es.Id_cr
-- where es.pecno = 116771
-- and Cr.Gerente = 'denise dos santos dias silva' 
-- and T.Nome LIKE '%Visita %'
-- and MONTH(TerminoReal) = 01
-- and YEAR(TerminoReal) = 2024
-- group by R.Nome
-- order by [Total de Visitas] DESC

select R.Nome as Sup, COUNT(R.Nome)  as Realizado
from Tarefa T
inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
inner join dw_vista.dbo.DM_Estrutura Es on Es.Id_Estrutura = T.EstruturaId
inner join dw_vista.dbo.DM_CR c on c.Id_cr = Es.Id_cr
where c.Gerente = 'CLAYTON MARTINS DAMASCENO'
and T.Nome LIKE '%Visita %' 
and MONTH(T.TerminoReal) = 02
and Year(T.TerminoReal) = 2024
GROUP BY R.Nome
ORDER BY COUNT(R.Nome) DESC

select R.Nome as Sup, COUNT(R.Nome)  as Realizado
from Tarefa T with(nolock)
inner join Recurso R with(nolock) on R.CodigoHash = T.FinalizadoPorHash
inner join dw_vista.dbo.DM_Estrutura Es with(nolock) on Es.Id_Estrutura = T.EstruturaId
inner join dw_vista.dbo.DM_CR c with(nolock) on c.Id_cr = Es.Id_cr
where c.Gerente = 'DENISE DOS SANTOS DIAS SILVA'
and T.Nome LIKE '%Visita %'
and R.Nome <> 'Sistema'
and MONTH(T.TerminoReal) = 02
and Year(T.TerminoReal) = 2024
GROUP BY R.Nome
ORDER BY COUNT(R.Nome) DESC

select R.Nome as Sup, COUNT(R.Nome)  as Realizado
from Tarefa T with(nolock)
inner join Recurso R with(nolock) on R.CodigoHash = T.FinalizadoPorHash
inner join dw_vista.dbo.DM_Estrutura Es with(nolock) on Es.Id_Estrutura = T.EstruturaId
inner join dw_vista.dbo.DM_CR c with(nolock) on c.Id_cr = Es.Id_cr
where c.Gerente = 'JOSIEL CESAR RIBAS DE OLIVEIRA'
and T.Nome LIKE '%Visita %'
and R.Nome <> 'Sistema'
and MONTH(T.TerminoReal) = 02
and Year(T.TerminoReal) = 2024
GROUP BY R.Nome
ORDER BY COUNT(R.Nome) DESC