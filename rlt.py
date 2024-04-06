import smtplib
from email.mime.multipart import MIMEMultipart as mlt
from email.mime.text import MIMEText as mt
from email.mime.base import MIMEBase as mb
from email import encoders
from time import strftime as st
from openpyxl import load_workbook as lw
from os import remove
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from pandas import read_sql

class Relatorio():
    def __init__(self, user, pwd, server:str = '10.56.6.56'):
        self.status = self.connect_db(user, pwd, server)

    def connect_db(self, uid, pwd, server):
        try:
            uid = quote_plus(uid)
            pwd = quote_plus(pwd)
            server = quote_plus(server)
            driver = quote_plus('ODBC Driver 18 for SQL Server')
            engine = create_engine(f'mssql+pyodbc://{uid}:{pwd}@{server}/Vista_Replication_PRD?driver={driver}&TrustServerCertificate=yes')
            self.conn = engine.connect()
            return 'Conectado'
        except Exception as error: return f'Conexão Invalida com o DB, Motivo: {str(error)}'

    def gerarConsulta(self, contrato: int, servico = '', emailC = 'guilherme.breve@gpssa.com.br'):
        self.month = int(st('%m'))
        self.year = int(st('%Y'))
        self.consulta = f"""SELECT T.Id, T.Numero, T.Nome, R.Nome as 'Colaborador',
        T.TerminoReal as 'Horario', P.Descricao as 'Pergunta', E.Conteudo as 'Resposta', Es.Descricao
        from Tarefa T with(nolock)
        inner join Recurso R with(nolock) on R.CodigoHash = T.CriadoPorHash
        inner join Pergunta P with(nolock) on P.ChecklistId = T.ChecklistId
        inner join Execucao E with(nolock) on E.TarefaId = T.Id
        inner join Estrutura Es with(nolock) on Es.Id = T.EstruturaId
        inner join dw_vista.dbo.DM_ESTRUTURA Es2 with(nolock)on Es2.Id_Estrutura = T.EstruturaId
        where Es2.CRno = {contrato}
        and R.Nome <> 'Sistema'
        and ServicoDescricao LIKE '%{servico}%'
        and MONTH(T.TerminoReal) = {self.month}
        and YEAR(T.TerminoReal) = {self.year} """
        self.emailC = emailC
        self.CR = self.nomeCR(contrato)
        self.nomeArquivo = f'{self.CR}.xlsx'
        dados = read_sql(self.consulta, self.conn)
        dados.to_excel(self.nomeArquivo,'Relatório')
        self.EnviarEmail(emailC)

    def nomeCR(self, cr):
        cr = read_sql(f"""select top 1 Descricao from Estrutura 
        where Descricao LIKE '%{cr}%' and Nivel = 3""", self.conn)
        for i in cr['Descricao']: return i
        
    def EnviarEmail(self, emailTo):
        # PARAMETROS DE EMAIL
        host = 'smtp.gmail.com'
        port = '587'
        email = 'projetos.londrinagps@gmail.com'
        senha = 'kxxgcptidjsnwdbt'
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(email, senha)
        
        # EMAIL EM SI
        msg = mlt()
        msg['From'] = email
        msg['To'] = emailTo
        msg['Subject'] = 'Relatorios Mensais'

        msg.attach(mt(f'Segue em anexo relatórios do contrato {self.CR} referente ao mês {self.month}/{self.year}', 'plain'))
        #abre o arquivo
        arquivo = open(self.nomeArquivo, 'rb')
        # Le o arquivo 
        att = mb('application','octet-stream')
        att.set_payload(arquivo.read()) 
        encoders.encode_base64(att)
    
        att.add_header('Content-Disposition',f'attachment; filename= {self.nomeArquivo}')
        arquivo.close()
        
        msg.attach(att)
        # SERVER DE ENVIO
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        remove(self.nomeArquivo)
        print(f'Email enviado com sucesso para {self.emailC}')

if __name__ == '__main__':
    r = Relatorio('guilherme.breve','84584608@Gui')
    r.gerarConsulta(42636)