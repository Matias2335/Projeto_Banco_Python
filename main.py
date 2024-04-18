#Codigo feito por:
#Guilherme Matias Rodrigues De Souza RA: 22.122.071-8
import re
import time
from datetime import datetime
from pytz import timezone

Extrato_final = []


def Menu():
  while True:
    print(30 * "=")
    print("** Menu **")
    print("1 - Novo Cliente")
    print("2 - Apagar Cliente")
    print("3 - Listar Clientes")
    print("4 - Débito")
    print("5 - Depósito")
    print("6 - Extrato")
    print("7 - Tranferência entre contas")
    print("8 - Investimento")
    print("9 - Sair")
    print(30 * "=")

    opcao = int(input("Digite sua escolha: "))
    if opcao == 1:
      NovoCliente()
    elif opcao == 2:
      Apagar()
    elif opcao == 3:
      Listar()
    elif opcao == 4:
      Debito()
    elif opcao == 5:
      Deposito()
    elif opcao == 6:
      Extrato()
    elif opcao == 7:
      Tranferir()
    elif opcao == 8:
      Investimento()
    elif opcao == 9:
      print("Volte Sempre")
      exit()
    else:
      print("Parece que houve um erro")
      print("Deseja voltar para o menu ??")
      voltar = int(input("Se desejar voltar digite [1]: "))
      if voltar == 1:
        return Menu()
      else:
        exit()

#função criada para verificar cpf e senha
def Verificar():
  cpf = int(input("Digite o CPF: "))
  encontrado = False
  arq = open("Banco.txt", "r")
  linhas = arq.readlines()
  arq.close()
  for i in range(len(linhas)):
    if "CPF: {}".format(cpf) in linhas[i]:
      encontrado = True

  if not encontrado:
    print("CPF não encontrado no sistema!")
    return Menu()

  senha = input("Digite sua Senha: ")
  encontrado = False
  arq = open("Banco.txt", "r")
  linhas = arq.readlines()
  arq.close()
  for i in range(len(linhas)):
    if "Senha: {}".format(senha) in linhas[i]:
      encontrado = True

  if not encontrado:
    print("Senha não encontrado no sistema!")
    return Menu()


#O sistema de Cadastro e adicionado no arquivo
def NovoCliente():
  arq = open("Banco.txt", "a")
  Nome = input("Digite seu nome: ")
  CPF = int(input("Digite seu CPF: "))
  TipoConta = input("Digite o tipo da sua conta (comum ou plus): ")
  Valor_Inicial = int(input("Digite o valor inicial da sua conta: "))
  Senha = input("Digite sua Senha: ")
  arq.write(
    f"Nome: {Nome}\nCPF: {CPF}\nConta: {TipoConta}\nValor: {Valor_Inicial}\nSenha: {Senha}"
  )


#funcao criada para vericar se o CPF digitado é igual a do cadastro , caso for o arquivo será removido caso contrario o arquivo continuará intacto
def Apagar():
  import os
  Verificar()
  os.remove("Banco.txt")


def Listar():
  arq = open("Banco.txt", "r")
  for i in range(4):
    linha = arq.readline()
    if linha:
      print(linha)
    else:
      break


#Função Debito onde é verificado seu CPF e Senha depois verifica qual tipo de conta para poder debitar da sua conta
def Debito():
  Verificar()

  arq = open("Banco.txt", "r")
  linhas = arq.readlines()
  arq.close()

  tipo_conta = None
  for linha in linhas:
    if "Conta: plus" in linha:
      tipo_conta = "plus"
      limite_negativo = -5000
    elif "Conta: comum" in linha:
      tipo_conta = "comum"
      limite_negativo = -1000

  if tipo_conta is None:
    print("Conta não encontrada no arquivo.")
  else:
    valor = float(input("Digite o valor que deseja debitar: "))
    for i, linha in enumerate(linhas):
      if "Valor:" in linha:
        saldo_atual = float(linha.split(": ")[1].strip())
        break

    if tipo_conta == "plus":
      taxa_debito = 0.03
    else:
      taxa_debito = 0.05
    saldo_novo = saldo_atual - (valor - taxa_debito)
    
    arq = open("Banco.txt","a")
    data_e_hora_atuais = datetime.now()
    fuso_horario = timezone('America/Sao_Paulo')
    data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
    datahora = data_e_hora_sao_paulo.strftime("%d/%m/%Y %H:%M")
    Extrato_final.append((f"\nExtrato: {datahora} - {valor} Tarifa: {taxa_debito:.2f} Saldo: {saldo_novo}\n"))
    teste = "".join(Extrato_final)
    arq.write(teste)
    arq.close()

    if saldo_novo < limite_negativo:
      print(
        "Débito não permitido. Saldo negativo ultrapassa o limite permitido.")
    elif valor <= saldo_atual:
      linhas[i] = f"Valor: {saldo_novo:.2f}\n"
      arq = open("Banco.txt", "w")
      arq.writelines(linhas)
      arq.close()
      print("Débito realizado com sucesso!")
    else:
      print("Saldo insuficiente para realizar o débito.")

  
  


#Função Deposito onde é verificado o cpf do cliente para depois consegueir fazer um deposito em sua conta
def Deposito():
  cpf = int(input("Digite o CPF: "))
  valor = float(input("Digite o valor do depósito: "))

  encontrado = False
  arq = open("Banco.txt", "r")
  linhas = arq.readlines()
  arq.close()

  for i in range(len(linhas)):
    if "CPF: {}".format(cpf) in linhas[i]:
      encontrado = True
      saldo_atual = float(linhas[i + 2].split(": ")[1].strip())
      saldo_novo = saldo_atual + valor
      linhas[i + 2] = f"Valor: {saldo_novo:.2f}\n"
      
      arq = open("Banco.txt", "w")
      arq.writelines(linhas)
      arq.close()
      print("Depósito realizado com sucesso!")
      break

  if not encontrado:
    print("CPF não encontrado no sistema!")
  arq =  open("Banco.txt","a")
  data_e_hora_atuais = datetime.now()
  fuso_horario = timezone('America/Sao_Paulo')
  data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
  datahora = data_e_hora_sao_paulo.strftime("%d/%m/%Y %H:%M")
  Extrato_final.append((f"Extrato: {datahora} + {valor:.3f} Tarifa: 0.00 Saldo: {saldo_novo}\n"))
  teste = "".join(Extrato_final)
  arq.write(teste)
  arq.close()

#Função Transferir onde é pedido 2 cpf o seu e de outra conta para conseguir fazer uma trasnferencia entre contas
def Tranferir():
  cpf_origem = int(input("Digite o CPF da conta de origem: "))
  cpf_destino = int(input("Digite o CPF da conta de destino: "))
  valor = float(input("Digite o valor a ser transferido: "))

  arq = open("Banco.txt", "r")
  linhas = arq.readlines()
  arq.close()

  origem_encontrado = False
  destino_encontrado = False

  for i in range(len(linhas)):
    if "CPF: {}".format(cpf_origem) in linhas[i]:
      origem_encontrado = True
      saldo_origem_atual = float(linhas[i + 2].split(": ")[1].strip())
      if valor > saldo_origem_atual:
        print("Saldo insuficiente para realizar a transferência.")
        return
      saldo_origem_novo = saldo_origem_atual - valor
      linhas[i + 2] = f"Valor: {saldo_origem_novo:.2f}\n"

    elif "CPF: {}".format(cpf_destino) in linhas[i]:
      destino_encontrado = True
      saldo_destino_atual = float(linhas[i + 2].split(": ")[1].strip())
      saldo_destino_novo = saldo_destino_atual + valor
      linhas[i + 2] = f"Valor: {saldo_destino_novo:.2f}\n"

  if not origem_encontrado:
    print("Conta de origem não encontrada.")
    return

  if not destino_encontrado:
    print("Conta de destino não encontrada.")
    return

  arq = open("Banco.txt", "w")
  arq.writelines(linhas)
  arq.close()
  print("Transferência realizada com sucesso!")

#Função Extrato mostra a suas transações 
def Extrato():
  Verificar()
  linhas_extrato = []

  arq = open('Banco.txt', 'r') 
  arq= arq.readlines()
  print(f"{arq[0]}{arq[1]}{arq[2]}")
  for linha in arq:
    if "Extrato: " in linha.strip():
      linhas_extrato.append(linha)

  for linha in linhas_extrato:
    print(linha)


#Sistema de investimento com 4 tipos de acões para comprar e demonstrar quanto seu dinheiro renderia com elas
def Investimento():
  Verificar()
  while True:

    print("1 - LCI IPCA FINAL 3 ANOS")
    print("2 - CDB LIQUIDEZ DIARIA")
    print("3 - CDB VOITER")
    print("4 - ENERGISA")
    print("0 - Sair")
    escolha = int(input("Digite qual opções deseja investir: "))
    arq = open("Banco.txt","a")
    if escolha == 1:
      print("Descrição sobre LCI IPCA FINAL 3 ANOS")
      print(
        "Grau de risco: Baixo\nRentabilidade: A partir de 4.41%% +IPCA\nValor Minimo: R$50,00\nVencimento 23/10/2025"
      )
      valor_investir = int(input("Valor a investir: "))
      if valor_investir >= 50:
        calc = (0.0714 + 0.0441) * valor_investir
        total = calc + valor_investir
        arq.write(f"\nIsso seria quantos reais renderia durante 1 ano: {calc}\nEsse seria o resultado do seu investimento: {total}")
        print(f"Valor que renderia: {total}\n")
      else:
        print("Valor minimo não atingido\n")
        time.sleep(2)
        return Investimento()

    elif escolha == 2:
      print("Descrição sobre CDB LIQUIDEZ DIARIA")
      print(
        "Grau de risco: Muito baixo\nRentabilidade: A partir de 98.0%% do CDI\nValor Minimo:R$100,00\nVencimento 08/10/2024"
      )
      valor_investir = int(input("Valor a investir: "))
      if valor_investir >= 100:
        calc = (0.1167) * valor_investir
        total = calc + valor_investir
        arq.write(f"\nIsso seria quantos reais renderia durante 1 ano: {calc}\nEsse seria o resultado do seu investimento: {total}")
        print(f"Valor que renderia: {total}")
      else:
        print("Valor minimo não atingido\n")
        time.sleep(2)
        return Investimento()

    elif escolha == 3:
      print("Descrição sobre CDB VOITER")
      print(
        "Grau de risco: Médio\nRentabilidade: 14,25%% a.a\nValor Minimo:R$1001,45\nVencimento 18/11/2024"
      )
      valor_investir = int(input("Valor a investir: "))
      if valor_investir >= 1001.45:
        calc = (0.1425) * valor_investir
        total = calc + valor_investir
        arq.write(f"\nIsso seria quantos reais renderia durante 1 ano: {calc}\nEsse seria o resultado do seu investimento: {total}")
        print(f"Valor que renderia: {total}")
      else:
        print("Valor minimo não atingido\n")
        time.sleep(2)
        return Investimento()

    elif escolha == 4:
      print("Descrição sobre ENERGISA")
      print(
        "Grau de risco: Alto\nRentabilidade: IPCA + 6.00%% a.a\nValor Minimo: R$1008,45\nVencimento 15/04/2029"
      )
      valor_investir = int(input("Valor a investir: "))
      if valor_investir >= 1008.45:
        calc = (0.0714 + 0.06) * valor_investir
        total = calc + valor_investir
        arq.write(f"\nIsso seria quantos reais renderia durante 1 ano: {calc}\nEsse seria o resultado do seu investimento: {total}")
        print(f"Valor que renderia: {total}")
      else:
        print("Valor minimo não atingido\n")
        time.sleep(2)
        return Investimento()

    elif escolha == 0:
      return Menu()

  arq.close()
      


Menu()
