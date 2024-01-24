select R.Nome as 'Sup', Es.Nivel_03 as 'CR ', TerminoReal as 'Data de Finalização' 
from Tarefa T
inner join Recurso R on R.CodigoHash = T.FinalizadoPorHash
inner join DW_Vista.dbo.DM_Estrutura Es on Es.Id_Estrutura = T.EstruturaId
inner join DW_Vista.dbo.DM_CR cr on cr.Id_CR = Es.ID_Cr
where T.Nome LIKE '%Visita%'
and Cr.Gerente = 'DENISE DOS SANTOS DIAS SILVA'
and DAY(T.TerminoReal) = 22
and MONTH(T.TerminoReal) = 01
and YEAR(T.TerminoReal) = 2024