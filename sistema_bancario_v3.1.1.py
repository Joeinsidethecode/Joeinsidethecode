from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, cpf, nome, endereco):
        self.cpf = cpf
        self.nome = nome
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.cadastrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, endereco, data_nascimento):
        super().__init__(cpf, nome, endereco)
        self.data_nascimento = data_nascimento

class Conta(ABC):
    def __init__(self, numero_conta, cliente):
        self.numero_conta = numero_conta
        self.cliente = cliente
        self.saldo = 0
        self.historico = Historico()

    @abstractmethod
    def sacar(self, valor):
        pass

    @abstractmethod
    def depositar(self, valor):
        pass

    @property
    def extrato(self):
        return self.historico.transacoes

class ContaCorrente(Conta):
    def __init__(self, numero_conta, cliente, limite=500, limite_saques=3):
        super().__init__(numero_conta, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        if valor <= 0:
            print('Valor inválido. Informe corretamente o valor.\n')
            return False

        saldo_total = self.saldo + self.limite
        if valor > saldo_total:
            print('Seu saldo é insuficiente. A operação não foi realizada.\n')
            return False

        if len(self.historico.transacoes) >= self.limite_saques:
            print(f'Seu limite de {self.limite_saques} saques diários foi excedido. A operação não foi realizada.\n')
            return False

        self.saldo -= valor
        self.historico.adicionar_transacao('Saque', valor)
        print('Saque realizado com sucesso.\n')
        return True

    def depositar(self, valor):
        if valor <= 0:
            print('Valor inválido. Informe corretamente o valor.\n')
            return False

        self.saldo += valor
        self.historico.adicionar_transacao('Depósito', valor)
        print('Depósito realizado com sucesso.\n')
        return True

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, tipo, valor):
        self.transacoes.append({
            'tipo': tipo,
            'valor': valor,
            'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        })

def menu():
    menu_text = '''
*** MENU PRINCIPAL ***
[1] Cadastro de novo cliente
[2] Cadastro de nova conta-corrente
[3] Exibir lista de clientes
[4] Exibir contas
[5] Fazer depósito
[6] Efetuar saque
[7] Ver extrato
[8] Encerrar
'''
    return input(textwrap.dedent(menu_text))

def filtrar_cliente(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def criar_cliente(clientes):
    cpf = input('CPF (somente números): ')
    if filtrar_cliente(cpf, clientes):
        print('Erro: CPF já cadastrado para outro usuário.')
        return

    nome = input('Nome completo: ')
    endereco = input('Endereço: ')
    data_nascimento = input('Data de nascimento (dd/mm/aaaa): ')
    cliente = PessoaFisica(cpf, nome, endereco, data_nascimento)
    clientes.append(cliente)
    print('\nCliente cadastrado com sucesso!')

def criar_conta(clientes, contas):
    cpf = input('CPF do cliente (somente números): ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print('Cliente não encontrado no banco de dados.')
        return

    numero_conta = len(contas) + 1
    conta = ContaCorrente(numero_conta, cliente)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print('Conta-corrente cadastrada com sucesso!')

def listar_contas(contas):
    for conta in contas:
        print('='*100)
        print(f'Número da Conta: {conta.numero_conta}')
        print(f'Cliente: {conta.cliente.nome}')
        print(f'Saldo: R${conta.saldo:.2f}')
        print('='*100)

def depositar(clientes):
    cpf = input('CPF do cliente (somente números): ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print('Cliente não encontrado no banco de dados.')
        return

    valor = float(input('Valor do depósito: R$ '))
    conta = cliente.contas[0]  # Assumindo que o cliente possui apenas uma conta
    conta.depositar(valor)

def sacar(clientes):
    cpf = input('CPF do cliente (somente números): ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print('Cliente não encontrado no banco de dados.')
        return

    valor = float(input('Valor do saque: R$ '))
    conta = cliente.contas[0]  # Assumindo que o cliente possui apenas uma conta
    conta.sacar(valor)

def exibir_extrato(clientes):
    cpf = input('CPF do cliente (somente números): ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print('Cliente não encontrado no banco de dados.')
        return

    conta = cliente.contas[0]  # Assumindo que o cliente possui apenas uma conta
    print('='*60)
    print('\n\t**** INFORMAÇÕES DA CONTA ****')
    transacoes = conta.extrato
    if not transacoes:
        print('Não foram realizadas transações no período')
    else:
        for transacao in transacoes:
            print(f"{transacao['tipo']}:\tR${transacao['valor']:.2f}")
    print(f'\nSaldo: R${conta.saldo:.2f}')
    print('='*60)

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        if opcao == '1':
            criar_cliente(clientes)
        elif opcao == '2':
            criar_conta(clientes, contas)
        elif opcao == '3':
            for cliente in clientes:
                print(f'CPF: {cliente.cpf}, Nome: {cliente.nome}, Endereço: {cliente.endereco}')
        elif opcao == '4':
            listar_contas(contas)
        elif opcao == '5':
            depositar(clientes)
        elif opcao == '6':
            sacar(clientes)
        elif opcao == '7':
            exibir_extrato(clientes)
        elif opcao == '8':
            print('Encerrando o programa...')
            break
        else:
            print('Opção inválida. Escolha a operação desejada.\n')

if __name__ == "__main__":
    main()
