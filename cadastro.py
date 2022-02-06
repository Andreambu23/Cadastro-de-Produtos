from PyQt5 import uic, QtWidgets #importando a lib do QT Designer

#conectando com o banco de dados
import mysql.connector  
con = mysql.connector.connect(
    host='localhost', database='cadastro_estoque', user='root', password='anova234')

#função de inserir no banco de dados
def insert():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    linha4 = formulario.lineEdit_4.text()

    categoria = ""

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

    #Printando no terminal os itens inseridos, para simples conferência.
    print("Codigo ", linha1)
    print("Descrição ", linha2)
    print("Preço ", linha3)
    print("Quantidade ", linha4)

    #Comando de inserção de dados
    cursor = con.cursor()
    inserir = "INSERT INTO produtos (codigo, descricao, preco, categoria, quantidade) VALUES (%s,%s,%s,%s,%s)"
    dados = (str(linha1), str(linha2), str(linha3), categoria, str(linha4))
    cursor.execute(inserir, dados)
    con.commit()

    #Limpando os campos após cada cadastro
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")
    formulario.lineEdit_4.setText("")

#função consultar no banco de dados
def consult():
    consulta.show()


app = QtWidgets.QApplication([])
formulario = uic.loadUi(
    "/home/andre/Área de Trabalho/Cadastro-de-Produtos-main/formulario.ui")
consulta = uic.loadUi(
    "/home/andre/Área de Trabalho/Cadastro-de-Produtos-main/consultar.ui")
formulario.pushButton.clicked.connect(insert)
formulario.pushButton_2.clicked.connect(consult)

formulario.show()
app.exec()
