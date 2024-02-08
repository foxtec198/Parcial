from time import sleep as sl, strftime as st # Time
import pyautogui as pg # Automate
from pyperclip import copy # Trad Clipboard
from ctpaperclip import PyClipboardPlus # Image to Clipboard
from pandas import read_sql, DataFrame # Tratamento de Dados
from dataframe_image import export # Export png
from os import system, mkdir # Systems
from sqlalchemy import create_engine # SQL Server

# Parametros globais
engine = create_engine('mssql://guilherme.breve:84584608Guilherme@10.56.6.56/Vista_Replication_PRD?driver=SQL Server')
horaInicio = 8
mudarTurno = 18
horaFinal = 7
horaInicioFixed = horaInicio

class Parcial:
    def __init__(self):
        pg.FAILSAFE = False
        pg.PAUSE = 1.5
        self.create_dist()
        print(self.connection())
        self.pc = PyClipboardPlus()

    def create_dist(self):
        try: mkdir('dist')
        except: ...

    def connection(self):
        try:
            self.conn = engine.connect()
            self.init()
            return 'Conectado com sucesso'
        except: return 'Erro na conexão!'

    def init(self):
        self.now = st('%d/%m/%Y - %H:%M')
        self.day = st('%d')
        self.month = st('%m')
        self.year = st('%Y')
        self.horaC = st('%X')
        self.hora = int(st('%H'))
        self.nameOfMonth = st('%h')

    def make(self, nome, legenda, consulta, fimDeSemana=False, arquivo='img.png'):
        self.fds = st('%a')
        if fimDeSemana == True:
            self.caminho = f'dist\{arquivo}'
            self.png(nomeArquivo=arquivo, consulta=consulta)
            self.envio(nome=nome,legenda=legenda)
        else:
            if self.fds != 'Sat' and self.fds != 'Sun':
                self.caminho = f'dist\{arquivo}'
                self.png(nomeArquivo=arquivo, consulta=consulta)
                self.envio(nome=nome,legenda=legenda)

    def msg(self, nome, mensagem):
        # Entrar no chat
        self.atalho('alt','tab')
        sl(1)
        self.atalho('ctrl','f')
        sl(2)
        self.cola(nome)
        sl(2)
        self.atalho('ctrl','1')
        sl(7)
        
        # Enviar mensagem e fechamento de chat
        self.cola(mensagem)
        pg.press('enter')
        pg.press('esc')
        self.atalho('ctrl','f')
        self.atalho('ctrl','a')
        pg.press('backspace')
        self.atalho('alt','tab')

    def envio(self, nome, legenda):
        # Entrar no chat
        self.atalho('alt','tab')
        self.atalho('ctrl','f')
        sl(1)
        self.cola(nome)
        self.atalho('ctrl','1')
        sl(7)

        # Colar Imagem
        self.pc.write_image_to_clipboard(self.caminho)
        self.atalho('ctrl','v')
        sl(5)

        # Colar Legenda
        self.cola(legenda)
        sl(2)

        # Envio e Fechamento do chat
        pg.press('enter')
        pg.press('esc')
        self.atalho('ctrl','f')
        self.atalho('ctrl','a')
        pg.press('backspace')
        self.atalho('alt','tab')


    def png(self, consulta, nomeArquivo):
        self.nomeArquivo = f"dist/{nomeArquivo}"
        cv = read_sql(consulta, self.conn)
        df = DataFrame(cv)
        self.dataFrameBool = df.empty
        export(df, self.nomeArquivo, max_rows=95)

    def atalho(self, *key):
        with pg.hold(key[0]):
            pg.press(key[1])

    def cola(self, msg):
        copy(msg)
        self.atalho('ctrl','v')

    def display(self):
        print(st('%X'))
        sl(1)
        system('cls')

    def getHour(self):
        ent = input('Horario: ')
        if ent != '': return int(ent)
        else: return 8