from pyodbc import connect
from time import sleep, strftime as st
import pyautogui as pg 
from pyperclip import copy
from pandas import read_sql, DataFrame
from dataframe_image import export
from os import system, mkdir


class Parcial():
    def __init__(self):
        pg.FAILSAFE = False
        pg.PAUSE = 1.5
        try: mkdir('dist')
        except: False
        self.strConn = "DRIVER={SQL Server}; DATABASE=Vista_Replication_PRD; SERVER=10.56.6.56; UID=guilherme.breve; PWD=84584608Guilherme"
        self.conn = connect(self.strConn)

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
        sleep(1)
        self.atalho('alt','k')
        sleep(2)
        self.cola(nome)
        sleep(2)
        pg.press('enter')
        self.cola(mensagem)
        pg.press('enter')
        pg.press('esc')
        self.atalho('alt','tab')
    
    def envio(self, nome, legenda):
        self.atalho('ctrl','f')
        sleep(1)
        self.cola(nome)
        sleep(2)
        self.atalho('ctrl','1')
        system(f'explorer {self.caminho}')
        sleep(7)
        self.atalho('ctrl','c')
        self.atalho('ctrl','w')
        self.atalho('ctrl','v')
        sleep(2)
        self.cola(legenda)
        sleep(2)
        pg.press('Enter')
        pg.press('esc')
        self.atalho('ctrl','f')
        self.atalho('ctrl','a')
        pg.press('backspace')

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