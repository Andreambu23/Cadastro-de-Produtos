import mysql.connector
from asyncore import read
from PyQt5 import uic
from PyQt5 import QtWidgets
from numpy import save
from reportlab.pdfgen import canvas

c = 0

# Conectando com o banco de dados

con = mysql.connector.connect(
    host='localhost', database='cadastro_estoque', user='andre2', password='anova123')

# Exportar em arquivo


def export():
    cursor = con.cursor()
    query = ("SELECT * FROM produtos")
    cursor.execute(query)
    readed_data = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 20)
    pdf.drawString(200, 800, "Produtos Cadastrados:")
    pdf.setFont("Times-Bold", 12)

    # Posições dos tópicos na exibição do arquivo em PDF "X, Y"
    # X é a distância entre um titulo em outro na mesma linha
    pdf.drawString(10, 750, "CÓD")
    pdf.drawString(50, 750, "PRODUTO")
    pdf.drawString(280, 750, "PREÇO")
    pdf.drawString(330, 750, "CATEGORIA")
    pdf.drawString(480, 750, "QTD")

    # Linha 37 espaçamento entre linhas.
    for i in range(0, len(readed_data)):
        y = y + 15
        pdf.drawString(10, 750 - y, str(readed_data[i][0]))
        pdf.drawString(50, 750 - y, str(readed_data[i][1]))
        pdf.drawString(280, 750 - y, str(readed_data[i][2]))
        pdf.drawString(330, 750 - y, str(readed_data[i][3]))
        pdf.drawString(480, 750 - y, str(readed_data[i][4]))
        #pdf.drawString(420, 750 - y, str(readed_data[i][5]))

    pdf.save()
    print("Planilha gerada com sucesso.")


# Função de inserir as informações digitadas nos campos no banco de dados SQL

def insert():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    linha4 = formulario.lineEdit_4.text()

    categoria = ("")

    if formulario.checkBox.isChecked():
        print("Item adicionado à categoria Informática.")
        categoria = ("Informática")
    elif formulario.checkBox_2.isChecked():
        print("Item adicionado à categoria Alimentos.")
        categoria = ("Alimentos")
    elif formulario.checkBox_3.isChecked():
        print("Item adicionado à categoria Eletrodomésticos.")
        categoria = ("Eletrodomésticos")
    elif formulario.checkBox_4.isChecked():
        print("Item adicionado à categoria Cama, Mesa e Banho.")
        categoria = ("Cama, Mesa e Banho")
    elif formulario.checkBox_5.isChecked():
        print("Item adicionado à categoria Brinquedos.")
        categoria = ("Brinquedos")
    elif formulario.checkBox_6.isChecked():
        print("Item adicionado à categoria Produtos de Limpeza.")
        categoria = ("Produtos de Limpeza")
    elif formulario.checkBox_7.isChecked():
        print("Item adicionado à categoria Higiene Pessoal.")
        categoria = ("Higiene Pessoal")

    # Printando no terminal os itens inseridos, para simples conferência.
    print("Codigo ", linha1)
    print("Descrição ", linha2)
    print("Preço ", linha3)
    print("Categoria", linha4)

    # Comando SQL de inserção de dados

    cursor = con.cursor()
    query = (
        "INSERT INTO produtos (codigo, descricao, preco, categoria, quantidade) VALUES (%s,%s,%s,%s,%s)")
    dados = (str(linha1), str(linha2), str(linha3), categoria, str(linha4))
    cursor.execute(query, dados)
    con.commit()

    # Limpando os campos de texo após cada cadastro

    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")
    formulario.lineEdit_4.setText("")

# Função consultar no banco de dados


def consult():

    consultar.show()

    cursor = con.cursor()
    query = ("SELECT codigo, descricao, preco, categoria, quantidade FROM produtos;")
    cursor.execute(query)
    readed_data = cursor.fetchall()

    consultar.tableWidget.setRowCount(len(readed_data))
    consultar.tableWidget.setColumnCount(5)

    for i in range(0, len(readed_data)):
        for j in range(0, 5):
            consultar.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(readed_data[i][j])))


# Alterar qualquer dado inserido no DB

def edit():
    global c
    line = consultar.tableWidget.currentRow()
    cursor = con.cursor()
    selectquery = ("Select codigo FROM produtos")
    cursor.execute(selectquery)
    readed_data = cursor.fetchall()
    codigo = readed_data[line][0]
    cursor = con.cursor()
    selectquery2 = (
        "SELECT * FROM produtos WHERE codigo = " + str(codigo) + (";"))
    cursor.execute(selectquery2)
    produto = cursor.fetchall()
    editwindow.show()

    c = codigo

    editwindow.lineEdit.setText(str(produto[0][0]))
    editwindow.lineEdit_2.setText(str(produto[0][1]))
    editwindow.lineEdit_3.setText(str(produto[0][2]))
    editwindow.lineEdit_4.setText(str(produto[0][3]))
    editwindow.lineEdit_5.setText(str(produto[0][4]))

# Salvando os dados editados


def save():
    # Identifica do número do código do Produto
    global c

    # Valor digitado na caixa de texto para edição
    descricao = editwindow.lineEdit_2.text()
    preco = editwindow.lineEdit_3.text()
    categoria = editwindow.lineEdit_4.text()
    quantidade = editwindow.lineEdit_5.text()

    # Atualizando o banco de dados

    cursor = con.cursor()
    editquery = ("UPDATE produtos SET descricao = '{}', preco = '{}', categoria = '{}', quantidade = '{}' WHERE codigo = {}".format(
        descricao, preco, categoria, quantidade, c))
    cursor.execute(editquery)
    con.commit()
    print("Dados alterados com sucesso!")
    editwindow.close()
    consultar.close()
    consult()

# Apagar dado inserido no DB


def delete():

    line = consultar.tableWidget.currentRow()
    consultar.tableWidget.removeRow(line)
    cursor = con.cursor()
    selectquery = ("Select codigo FROM produtos")
    cursor.execute(selectquery)
    readed_data = cursor.fetchall()
    codigo = readed_data[line][0]
    print(codigo)
    cursor.close()
    cursor = con.cursor()
    deletequery = (
        "DELETE FROM cadastro_estoque.produtos WHERE codigo = " + str(codigo) + (";"))
    cursor.execute(deletequery)
    con.commit()

    print("Item excluido da lista.")


# Selecionar produdo cadastrado e exibir na tela, "Ex.: Consulta de preço"

app = QtWidgets.QApplication([])
formulario = uic.loadUi(
    "/home/andre/Área de Trabalho/Estudos/Cadastro-de-Produtos/formulario.ui")
consultar = uic.loadUi(
    "/home/andre/Área de Trabalho/Estudos/Cadastro-de-Produtos/consultar.ui")
editwindow = uic.loadUi(
    "/home/andre/Área de Trabalho/Estudos/Cadastro-de-Produtos/editwindow.ui")
formulario.pushButton.clicked.connect(insert)
formulario.pushButton_2.clicked.connect(consult)
consultar.pushButton.clicked.connect(export)
consultar.pushButton_2.clicked.connect(delete)
consultar.pushButton_3.clicked.connect(edit)
editwindow.pushButton.clicked.connect(save)

formulario.show()
app.exec()


""" Finalmente, com o pouco tempo que eu tenho consegui finalizar essa parte, à partir daqui é que começa a parte de praticar, ainda assim, como estou iniciando tive muita dificuldade em conseguir que todas as funções funcionassem, pesquisei por conta própria, tirei dúvidas em grupos do Telegram, o GitHub me ajudou demais, várias das dúvidas e vários problemas que eu tive foram possíveis encontrar a solução lá.
    A ideia agora, é criar uma tela de Login e com esse login se conectar ao banco de dados, delegando menos atribuições e deixando as funções de editar e excluir dados apenas para o administrador, além do mais, será acrescentada uma tela que será basicamente a tela de um caixa de comércio, que irá buscar o produto pelo código lido, inserir em um display e fazer a somatória dos valores de cada produto."""