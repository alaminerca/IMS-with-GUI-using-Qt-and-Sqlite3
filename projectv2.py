import sqlite3
import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItem
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QApplication, QDialog, QListWidget, QMessageBox
from PyQt5.QtWidgets import QTableView, QHeaderView
from PyQt5.uic import loadUi


class Employee:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class Product:
    def __init__(self, id, name, quantity):
        self.id = id
        self.name = name
        self.quantity = quantity


class Login(QDialog):
    def __init__(self, db):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.db = db
        self.signIn.clicked.connect(self.loginFunction)
        self.registration.clicked.connect(self.gotoSignUp)

    def loginFunction(self):
        email = self.email.text()
        password = self.password.text()
        try:
            users = self.db.get_users()
            for user in users:
                if email == user[0] and password == user[1]:
                    print('Logged in as:', email)
                    self.gotoManagement()
                    return
            QMessageBox.warning(self, "Warning", "Invalid email or password")
        except Exception as e:
            QMessageBox.critical(self, "Error", "An error occurred: {}".format(e))

    def gotoManagement(self):
        manage = Management(self.db)
        widget.addWidget(manage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoSignUp(self):
        signUp = SignUp(self.db)
        widget.addWidget(signUp)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class SignUp(QDialog):
    def __init__(self, db):
        super(SignUp, self).__init__()
        loadUi("signup.ui", self)
        self.db = db
        self.signUp.clicked.connect(self.registerFunction)



    def registerFunction(self):
        email = self.email.text()
        password = self.password.text()
        confirm_password = self.confirmPassword.text()
        empty = ""
        null = None
        try:
            if password != confirm_password:
                QMessageBox.warning(self, "Warning", "Passwords do not match")
                return
            if (email == empty or email == null) or (password == empty or password == null):
                QMessageBox.warning(self, "Warning", "Invalid inputs")
                return
            self.db.add_user(Employee(email, password))
            QMessageBox.information(self, "Success", "Registered successfully")
            login_dialog = Login(self.db)
            widget.addWidget(login_dialog)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as e:
            QMessageBox.critical(self, "Error", "An error occurred: {}".format(e))




class Management(QDialog):
    def __init__(self, db):
        super(Management, self).__init__()
        loadUi("management.ui", self)
        self.db = db
        self.viewAll.clicked.connect(self.displayProductFunction)
        self.updateProduct.clicked.connect(self.updateProductFunction)
        self.addProduct.clicked.connect(self.addProductFunction)
        self.deleteProduct.clicked.connect(self.deleteProductFunction)
        self.logout.clicked.connect(self.loginFunction)

    def displayProductFunction(self):
        try:
            display_dialog = DisplayProduct(self.db)
            display_dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", "An error occurred: {}".format(e))

    def updateProductFunction(self):
        try:
            update_dialog = UpdateProduct(self.db)
            update_dialog.exec_()
            self.displayProductFunction()
        except Exception as e:
            QMessageBox.critical(self, "Error", "An error occurred: {}".format(e))

    def addProductFunction(self):
        try:
            add_dialog = InsertProduct(self.db)
            add_dialog.exec_()
            self.displayProductFunction()
        except Exception as e:
            QMessageBox.critical(self, "Error", "An error occurred: {}".format(e))

    def deleteProductFunction(self):
        try:
            delete_dialog = DeleteProduct(self.db)
            delete_dialog.exec_()
            self.displayProductFunction()
        except Exception as e:
            QMessageBox.critical(self, "Error", "An error occurred: {}".format(e))

    def loginFunction(self):
        self.close()


class DisplayProduct(QDialog):
    def __init__(self, db):
        super(DisplayProduct, self).__init__()
        loadUi("viewAll.ui", self)
        self.db = db
        self.createConnection()
        self.select_data()
        self.gotomanagement.clicked.connect(self.backtoManagement)

    def createConnection(self):
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        self.con.setDatabaseName("projectDB.db")
        if not self.con.open():
            QMessageBox.critical(self, "Error", "Unable to connect to database")

    def select_data(self):
        try:
            self.model = QSqlTableModel(self, self.con)
            self.model.setTable("products")
            self.model.select()
            self.tableView.setModel(self.model)
            self.tableView.resizeColumnsToContents()
        except Exception as ex:
            QMessageBox.critical(self, "Error", str(ex))

    def backtoManagement(self):
        self.close()



class UpdateProduct(QDialog):
    def __init__(self, db):
        super(UpdateProduct, self).__init__()
        loadUi("update.ui", self)
        self.db = db
        self.gotomanagement.clicked.connect(self.backtoManagement)
        self.commitUpdate.clicked.connect(self.updateProduct)

    def updateProduct(self):
        try:
            product_id = int(self.productIDToUpdate.text())
            name = self.productNameToUpdate.text()
            quantity = int(self.productQuantityToUpdate.text())
            self.db.update_product(Product(product_id, name, quantity))
            QMessageBox.information(self, "Success", "Product updated successfully")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", "An error occurred: {}".format(e))

    def backtoManagement(self):
        self.close()


class InsertProduct(QDialog):
    def __init__(self, db):
        super(InsertProduct, self).__init__()
        loadUi("insert.ui", self)
        self.db = db
        self.gotomanagement.clicked.connect(self.backtoManagement)
        self.commitAdd.clicked.connect(self.addProduct)

    def addProduct(self):
        try:
            product_id = int(self.productIdToAdd.text())
            name = self.productName.text()
            quantity = int(self.productQuantity.text())
            self.db.add_product(Product(product_id, name, quantity))
            QMessageBox.information(self, "Success", "Product added successfully")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", "An error occurred: {}".format(e))

    def backtoManagement(self):
        self.close()


class DeleteProduct(QDialog):
    def __init__(self, db):
        super(DeleteProduct, self).__init__()
        loadUi("delete.ui", self)
        self.db = db
        self.gotomanagement.clicked.connect(self.backtoManagement)
        self.commitDelete.clicked.connect(self.deleteProduct)

    def deleteProduct(self):
        try:
            product_id = int(self.idOfProductToDelete.text())
            self.db.delete_product(product_id)
            QMessageBox.information(self, "Success", "Product deleted successfully")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", "An error occurred: {}".format(e))

    def backtoManagement(self):
        self.close()


class Database:
    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self.create_tables()
        except Exception as e:
            QMessageBox.critical(None, "Error", "An error occurred: {}".format(e))

    def create_tables(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                                   (email TEXT, password TEXT)''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS products
                                   (id INT, name TEXT, quantity INTEGER)''')
            self.conn.commit()
            print("Tables created successfully")
        except Exception as e:
            QMessageBox.critical(None, "Error", "An error occurred: {}".format(e))

    def add_user(self, employee):
        try:
            self.cursor.execute("INSERT INTO employees VALUES (?, ?)", (employee.email, employee.password))
            self.conn.commit()
        except Exception as e:
            QMessageBox.critical(None, "Error", "An error occurred: {}".format(e))

    def add_product(self, product):
        try:
            self.cursor.execute("INSERT INTO products VALUES (?, ?, ?)", (product.id, product.name, product.quantity))
            self.conn.commit()
        except Exception as e:
            QMessageBox.critical(None, "Error", "An error occurred: {}".format(e))

    def update_product(self, product):
        try:
            self.cursor.execute("UPDATE products SET name = ?, quantity = ? WHERE id = ?",
                                (product.name, product.quantity, product.id))
            self.conn.commit()
        except Exception as e:
            QMessageBox.critical(None, "Error", "An error occurred: {}".format(e))

    def delete_product(self, product_id):
        try:
            self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            self.conn.commit()
        except Exception as e:
            QMessageBox.critical(None, "Error", "An error occurred: {}".format(e))

    def get_users(self):
        try:
            self.cursor.execute("SELECT * FROM employees")
            return self.cursor.fetchall()
        except Exception as e:
            QMessageBox.critical(None, "Error", "An error occurred: {}".format(e))

    def get_products(self):
        try:
            self.cursor.execute("SELECT * FROM products")
            return self.cursor.fetchall()
        except Exception as e:
            QMessageBox.critical(None, "Error", "An error occurred: {}".format(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = Database("projectDB.db")
    login_dialog = Login(db)
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(login_dialog)
    widget.setCurrentWidget(login_dialog)
    widget.setFixedWidth(620)
    widget.setFixedHeight(740)
    widget.show()
    sys.exit(app.exec_())
