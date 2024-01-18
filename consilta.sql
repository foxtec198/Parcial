select R.Nome as 'Sup', Es.Nivel_03 as 'CR ', TerminoReal as 'Data de Finalização' 
from Tarefa T with(nolock)
inner join Recurso R with(nolock) on R.CodigoHash = T.FinalizadoPorHash
inner join DW_Vista.dbo.DM_Estrutura Es with(nolock) on Es.Id_Estrutura = T.EstruturaId
inner join DW_Vista.dbo.DM_CR cr with(nolock) on cr.Id_CR = Es.ID_Cr
where Cr.Gerente = 'DENISE DOS SANTOS DIAS SILVA'
and DAY(T.TerminoReal) = 18 
and MONTH(T.TerminoReal) = 01
and YEAR(T.TerminoReal) = 2024