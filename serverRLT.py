from rlt import Relatorio
from time import strftime as st, sleep
from os import system

r = Relatorio('guilherme.breve', '84584608@Gui')
email = 'leandro.costa@gpssa.com.br'
mat = True
diaDeEnvio = 26

# Looping
while True:
    dia = int(st('%d'))
    if dia == diaDeEnvio and mat:
        r.gerarConsulta('25153', emailC= email)
        r.gerarConsulta('25148', emailC= email)
        mat = False
    if dia == diaDeEnvio + 1 and not mat: mat = True
    else:
        system('cls')
        print('Aguardando para enviar email...')
        sleep(1)

