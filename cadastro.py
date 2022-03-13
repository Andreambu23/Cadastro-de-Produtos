from asyncore import read
import readline
from sqlite3 import Cursor
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtQuickWidgets
from reportlab.pdfgen import canvas

# conectando com o banco de dados

import mysql.connector
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


# função de inserir no banco de dados.

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

# função consultar no banco de dados


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


#def edit(): - Alterar qualquer dado inserido no DB

# Apagar dado inserido no DB


def delete():

    line = consultar.tableWidget.currentRow()
    consultar.tableWidget.removeRow(line)
    cursor = con.cursor()
    query1 = ("Select codigo FROM produtos")
    cursor.execute(query1)
    readed_data = cursor.fetchall()
    cod_value = readed_data[line][0]
    print(cod_value)
    query2 = (
        "DELETE FROM `cadastro_estoque`.`produtos` WHERE (`codigo` = `%s`);") 
    cursor.execute(query2)

    print("Item excluido da lista.")


# def select(): - Selecionar produdo cadastrado e exibir na tela, "Ex.: Consulta de preço"

app = QtWidgets.QApplication([])
formulario = uic.loadUi(
    "/home/andre/Área de Trabalho/Estudos/Cadastro-de-Produtos/formulario.ui")
consultar = uic.loadUi(
    "/home/andre/Área de Trabalho/Estudos/Cadastro-de-Produtos/consultar.ui")
formulario.pushButton.clicked.connect(insert)
formulario.pushButton_2.clicked.connect(consult)
consultar.pushButton.clicked.connect(export)
consultar.pushButton_2.clicked.connect(delete)

formulario.show()
app.exec()
