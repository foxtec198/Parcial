from time import sleep as sl, strftime as st
import pyautogui as pg 
from pyperclip import copy
from pandas import read_sql, DataFrame
from dataframe_image import export
from os import system, mkdir
from sqlalchemy import create_engine

engine = create_engine('mssql://guilherme.breve:84584608Guilherme@10.56.6.56/Vista_Replication_PRD?driver=SQL Server')
horaInicio = 8
mudarTurno = 18
horaFinal = 7
horaInicioFixed = horaInicio

class Parcial:
    def __init__(self):
        pg.FAILSAFE = False
        pg.PAUSE = 1.5
        try: mkdir('dist')
        except: False
        self.conn = engine.connect()
        self.init()
    
    def sleep(self, x):
        sl(x)
        
    def init(self):    
        self.now = st('%d/%m/%Y - %H:%M')
        self.day = st('%d')
        self.month = st('%m')
        self.year = st('%Y')
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
                
    def makeFdsOnly(self, nome, arquivo, legenda, consulta):
        self.fds = st('%a')
        if self.fds == 'Sat' or self.fds == 'Sun':
            self.caminho = f'dist\{arquivo}'
            self.png(nomeArquivo=arquivo, consulta=consulta)
            self.envio(nome=nome,legenda=legenda)
                
    def msg(self, nome, mensagem):
        self.atalho('alt','tab')
        sl(1)
        self.atalho('alt','k')
        sl(2)
        self.cola(nome)
        sl(2)
        pg.press('enter')
        self.cola(mensagem)
        pg.press('enter')
        pg.press('esc')
        self.atalho('alt','tab')
    
    def envio(self, nome, legenda):
        self.atalho('ctrl','f')
        sl(1)
        self.cola(nome)
        self.atalho('ctrl','1')
        system(f'explorer {self.caminho}')
        sl(7)
        self.atalho('ctrl','c')
        self.atalho('alt','tab')
        sl(2)
        self.atalho('ctrl','v')
        sl(5)
        self.cola(legenda)
        sl(2)
        pg.press('Enter')
        pg.press('esc')
        self.atalho('ctrl','f')
        self.atalho('ctrl','a')
        pg.press('backspace')
        self.atalho('alt','tab')
        self.atalho('ctrl','w')

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