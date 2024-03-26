import smtplib
from email.mime.multipart import MIMEMultipart as mlt
from email.mime.text import MIMEText as mt
from email.mime.base import MIMEBase as mb
from email import encoders
from time import strftime as st
from pyodbc import connect
from openpyxl import load_workbook as lw
from os import remove

class Relatorio():
    def __init__(self, user, pwd, server:str = '10.56.6.56'):
        self.user = user
        self.pwd = pwd
        self.server = server
        
    def gerarConsulta(self, contrato, servico = '', emailC = 'guilherme.breve@gpssa.com.br'):
        self.planilha = lw('dist/relatorio.xlsx') 
        self.ws = self.planilha.active
        self.cr = contrato
        self.servico = servico
        self.month = int(st('%m'))
        self.year = int(st('%Y'))
        self.consulta = f"""SELECT
        T.Id, 
        T.Numero, 
        T.Nome, 
        R.Nome as 'Colaborador', 
        T.TerminoReal as 'Horario', 
        P.Descricao as 'Pergunta', 
        E.Conteudo as 'Resposta', 
        Es.Descricao
        from Tarefa T with(nolock)
        join Recurso R with(nolock) on R.CodigoHash = T.CriadoPorHash
        join Pergunta P with(nolock) on P.ChecklistId = T.ChecklistId
        join Execucao E with(nolock) on E.TarefaId = T.Id
        join Estrutura Es with(nolock) on Es.Id = T.EstruturaId
        where T.EstruturaNivel2 LIKE '%{self.cr}%'
        and ServicoDescricao LIKE '%%'
        and R.Nome NOT IN ('Sistema')
        and MONTH(T.TerminoReal) = {self.month}
        and YEAR(T.TerminoReal) = {self.year}
        """

        # PARAMETROS DO BD
        self.str_conn = f"DRIVER=SQL Server; SERVER={self.server}; UID={self.user}; PWD={self.pwd}"
        self.conn = connect(self.str_conn)
        self.c = self.conn.cursor()
        
        self.emailC = emailC
        self.nomeCR()
        self.dados = self.c.execute(self.consulta).fetchall()
        self.GerarRelatório()

    def nomeCR(self):
        self.cons = self.c.execute(f"""select Descricao
        from Estrutura
        where Descricao LIKE '%{self.cr}%'
        and Nivel = 3""").fetchall()[0][0]
    
    def GerarRelatório(self):
        linha = 3
        for i in self.dados:
            nome = i[0]
            self.ws[f'A{linha}'] = nome
            nome = i[1]
            self.ws[f'B{linha}'] = nome
            nome = i[2]
            self.ws[f'C{linha}'] = nome
            nome = i[3]
            self.ws[f'D{linha}'] = nome
            nome = i[4]
            self.ws[f'E{linha}'] = nome
            nome = i[5]
            self.ws[f'F{linha}'] = nome
            nome = i[6]
            self.ws[f'G{linha}'] = nome
            nome = i[7]
            self.ws[f'H{linha}'] = nome
            linha += 1
        self.nomeArquivo = 'relatorios.xlsx' 
        self.planilha.save(self.nomeArquivo)
        self.planilha.close()
        self.EnviarEmail(self.emailC)
        
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

        msg.attach(mt(f'Segue em anexo relatórios do contrato {self.cons} referente ao mês {self.month}/{self.year}', 'plain'))
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