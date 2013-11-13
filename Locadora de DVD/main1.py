#!usr/bin/python
#_*_coding:utf-8_*_
# MAIN.PY --- Funcoes e Classes mais pertinentes em relacao ao programa
#    modulos para execucao em segundo plano
#

#___METAS_________-
#   - Implementar a conta do valor de acordo com Dia da Semana e Categoria
#   - Terminar metodo de "devolucao"

import wx
import shelve
from cliente import cliente
from produto import produto
from datetime import date
from carrinho import carrinho

class loja:
    listaDeFilmes=[]
    lista=[]
    listaDeClientes=[]
    # -------------------------------------- FUNCOES PRIVADAS --------------------------------------
    #Ira procurar o cliente por CPF no banco de dados de Clientes
    def __procurarClienteCPF(self,cpfCliente = None):
        clientes = shelve.open("clientes")
        if cpfCliente==None:
            clientes.close()
            wx.MessageBox('Erro no Codigo', 'Erro', wx.OK|wx.ICON_ERROR)
        if len(clientes) == 0:   #Retorna erro se o banco de dados estiver vazio
            wx.MessageBox("Banco de dados vazio!!","Erro",wx.OK|wx.ICON_ERROR)
        
        for keys in clientes:
            clienteEncontrado = clientes[keys]
            if clienteEncontrado.cpf == cpfCliente:
                clientes.close()
                self.listaDeClientes.append(clienteEncontrado)
                return self.listaDeClientes
            elif clientes[keys].cpf[:len(cpfCliente)] == cpfCliente:
                self.listaDeClientes.append(clienteEncontrado)
        clientes.close()
        elif len(self.listaDeClientes)==0:
            wx.MessageBox('Nenhum Cliente Encontrado','Erro')
        return self.listaDeClientes

    #Procurar Cliente pelo NOME no banco de dados de Clientes
    def __procurarClienteNome(self,nomeCliente=None):
        clientes = shelve.open("clientes")
        if len(clientes) == 0:
            wx.MessageBox("Banco de Dados vazio!","Info",wx.OK|wx.ICON_INFORMATION)
        if nomeCliente!='':
            for keys in clientes:
                if keys == nomeCliente:
                    clienteEncontrado = clientes[nomeCliente]
                    clientes.close()
                    self.listaDeClientes.append(clienteEncontrado)
                    return self.listaDeClientes
                elif keys[:len(nomeCliente)].upper == nomeCliente.upper():
                    self.listaDeClientes.append(clientes[keys])
            clientes.close()
            return self.listaDeClientes
            wx.MessageBox('Varias Congruencias')
            

    #Função Privada para cadastrar lotes de filmes
    def __cadastrarFilmes(self,nomeFilme=None,codigo=None,qtd=None,Midia=None):
        filmes = shelve.open("filmes", writeback=True)
        if filmes.has_key(nomeFilme)==True and filmes[nomeFilme].codigo==codigo:
            filmes.close()
            wx.MessageBox("Filme já cadastrado no Banco de Dados",'Info',wx.OK|wx.ICON_INFORMATION)
            return False
        else:
            dataHj = date.today()
            f=produto(nomeFilme,codigo,qtd,dataHj,Midia)
            filmes[nomeFilme]=f
            filmes.close()      
            return True

    #Função Privada para cadastrar Clientes
    def __cadastrarClientes(self, nome = None, CPF = None):
        clientes = shelve.open("clientes", writeback = True)
        if nome == None or CPF == None:
            clientes.close()
            return False
        if clientes.has_key(nome) == True and clientes[nome].cpf == CPF:
            wx.MessageBos('Cliente ja cadastrado','Info',wx.OK|wx.ICON_INFORMATION)
            return False
        else:
            c = cliente(nome, CPF)
            clientes[nome] = c
            clientes.close()
            return "Cliente cadastrado com exito", True
    
    # Funcao que vai retornar uma lista de 10 congruencias 
    def __procurarFilme(self,titulo, codigo, categoria, midia):
        filmes=shelve.open("filmes")
        listaDeFilmes=[]
        if len(filmes)==0:
            wx.MessageBox('Banco de Dados Vazio!','Info',wx.OK|wx.ICON_INFORMATION)
        if (titulo == codigo) and (categoria==titulo) and (midia == titulo) and titulo=='': 
            for filme in filmes:
                self.listaDeFilmes.append(filmes[filme])
            filmes.close()
            return self.listaDeFilmes
        
        if titulo=='' or (titulo!='' and codigo!=''):
            for x in filmes:
                if filmes[x].codigo == codigo:
                    filmeEncontrado=filmes[x]
                    self.listaDeFilmes.append(filmeEncontrado)
            filmes.close()
            return self.listaDeFilmes  

        if titulo!='':
            if filmes.has_key(titulo):
                filmeEncontrado = filmes[nomeFilme]
                self.listaDeFilmes.append(filmeEncontrado)
                filmes.close()
                return self.listaDeFilmes
            else:
                for filme in filmes:
                    if filme[:len(titulo)].upper()==titulo.upper():
                        self.listaDeFilmes.append(filmes[filme])
                if len(listaDeFilmes)==0:                
                    filmes.close()
            
        if midia!='':
            for filme in filmes:
                if len(self.listaDeFilmes) == 10:
                    break
                if filmes[filme].midia == midia:
                    self.listaDeFilmes.append(filmes[filme])
            filmes.close()
            return self.listaDeFilmes

        if categoria!='':
            for filme in filmes:
                if len(self.listaDeFilmes)==10:
                    break
                if filmes[filme].categoria == categoria:
                    self.listaDeFilmes.append(filmes[filme])
            filmes.close()
            return self.listaDeFilmes
        

        else:
            filmes.close()
            return self.listaDeFilmes

    # -------------------------------- FUNÇOES EFETIVAS ---------------------------------------------------
    def procurarCliente(self,nomeCliente=None,cpf=None):
        if nomeCliente==None and cpf==None:
            return "Preencha um dos campos", False

        if nomeCliente=='' or (nomeCliente!='' and cpf!=''):
            try:
                self.__procurarClienteCPF(cpf)
            except:
                wx.MessageBox("Cliente não encontrado","Info",wx.OK|wx.ICON_INFORMATION)
        if cpf=='':
            try:
                self.__procurarClienteNome(nomeCliente)
            except:
                wx.MessageBox("Cliente não encontrado","Info",wx.OK|wx.ICON_INFORMATION)
                
    
    def cadastroCliente(self, nome = None, cpf = None):
        try:
            self.__cadastrarClientes(nome, cpf)
        except:
            return "Erro ao tentar cadastrar o Cliente", False

    def cadastroFilme(self, nome, codigo, quantidade, midia):
        try:
            self.__cadastrarFilmes(nome,codigo,quantidade,midia)
        except:
            return False

    def procurarFilme(self,titulo,codigo, categoria,midia): 
        if len(self.listaDeFilmes)>0:
            for x in self.listaDeFilmes:
                self.listaDeFilmes.remove(x)
        if len(self.lista)>0:
           for x in self.lista:
               self.lista.remove(x)
        try:
            self.lista = self.__procurarFilme(titulo,codigo,categoria,midia)
            return self.lista
        except:
            wx.MessageBox('Erro ao procurar Filme','Error',wx.OK|wx.ICON_INFORMATION)
            return False
            
    def alugar(self,filmes=None):
        if filmes==None:
           if len(carrinho.carrinhoDeCompras)!=0:
               filmes=carrinho.carrinhoDeCompras
               clientes = shelve.open("clientes.txt", writeback=True)
               dataHj = datetime.today()

           else:
                return "Carrinho de Compras Vazio![Erro 1]", False



