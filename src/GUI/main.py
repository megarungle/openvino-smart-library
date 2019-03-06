import sys, os
import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
import LoginWin  #design
import SignupWin #design
import AdminWin  #design
import AdminWin  #design
import ReaderWin
sys.path.insert(0, '../modules')
import face_recognizer
import book_recognizer



class LoginWindow(QtWidgets.QMainWindow, LoginWin.Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # initial design
        self.setFixedSize(self.size())
        self.pushButton.clicked.connect(self.SignUp)
        self.pushButton_2.clicked.connect(self.SignIn)  # execute func on button click
        self.admWin = AdminWindow()
        self.readerWin = ReaderWindow()
        self.signupWin = SignupWindow()
        
    def SignIn(self):
#        rec = face_recognizer.PVLRecognizer() #передавать через параметры
#        rec.Create("..\\modules\\pvl\\build\\Release\\PVL_wrapper.dll") # передавать через параметры
#        cap = cv2.VideoCapture(0)
#        UID = -10000
#        name = "UNKNOWN"
#        while(True): 
#            _, f = cap.read()
#            (ID, (x, y, w, h)) = rec.Recognize(f)
#            if (ID != UID):
#              name = str(ID)
#            cv2.rectangle(f, (x, y), (x + w, y + h), (0, 255, 0), 1)
#            cv2.putText(f, name , (x,y-2), cv2.FONT_HERSHEY_SIMPLEX, 1, (219, 132, 58), 2)
#            cv2.imshow("web", f)
#            ch = cv2.waitKey(1)
#            if ID != -10000:
#                break
#        ch = cv2.waitKey(1000)
#        cap.release()
#        cv2.destroyAllWindows()
#        print(ID)
        self.close()
        self.readerWin.show()
       # self.admWin.show()
        
    def SignUp(self):
        self.close()
        self.signupWin.show()

class SignupWindow(QtWidgets.QMainWindow, SignupWin.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # initial design
        self.setFixedSize(self.size())   
        self.pushButton.clicked.connect(self.SignUp)
        self.pushButton.setEnabled(False)
        
        self.lineEdit.textChanged.connect(self.EnableBtn)
        self.lineEdit_2.textChanged.connect(self.EnableBtn)
        self.lineEdit_3.textChanged.connect(self.EnableBtn)
        self.lineEdit_4.textChanged.connect(self.EnableBtn)
        
         
    def SignUp(self):
        self.fName = self.lineEdit.text()
        self.lName = self.lineEdit_2.text()
        self.mName = self.lineEdit_3.text()
        self.phone = self.lineEdit_4.text()
        
        #insert user in DB
        
        #---------------------
        rec = face_recognizer.PVLRecognizer() #передавать через параметры
        rec.Create("..\\modules\\pvl\\build\\Release\\PVL_wrapper.dll") # передавать через параметры
        cap = cv2.VideoCapture(0)
        UID = -10000
        name = "UNKNOWN"
        while(True): 
            _, f = cap.read()
            (ID, (x, y, w, h)) = rec.Recognize(f)
            if (ID != UID):
              name = str(ID) #Можно выводить имя пользователя
              cv2.putText(f, "You are already a member" , (x-w,y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 208, 86), 2)
              cv2.putText(f, "Press Q to exit" , (x-w,y+h+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 208, 86), 2)
            cv2.rectangle(f, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(f, name , (x+w//2 - 10  ,y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (219, 132, 58), 2)
            cv2.imshow("web", f)
            ch = cv2.waitKey(1)
            if (ch & 0xFF == ord('r') or ch & 0xFF == ord('R')) and ID != UID:
                tmp = rec.Register(f, 1) #Необходимо генерировать новый ID
            if ch & 0xFF == ord('q') or ch & 0xFF == ord('Q'):
               break
        cap.release()
        cv2.destroyAllWindows()
        print(ID)
        self.close()
        self.loginWin = LoginWindow()
        self.loginWin.show()
       
    
    def EnableBtn(self):
        if(len(self.lineEdit.text()) > 0 and  len(self.lineEdit_2.text()) > 0 and
            len(self.lineEdit_3.text()) > 0 and  len(self.lineEdit_4.text()) > 0 ):
             self.pushButton.setEnabled(True)
        else:
             self.pushButton.setEnabled(False)
        
class AdminWindow(QtWidgets.QMainWindow, AdminWin.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) #initial design
        self.setFixedSize(self.size())
        self.pushButton_1.clicked.connect(self.GetBook)
        self.pushButton_2.clicked.connect(self.AddBook) 
        self.pushButton_3.clicked.connect(self.GetInfoReaders) 
        self.pushButton_4.clicked.connect(self.GetInfoBooks) 
        self.pushButton_5.clicked.connect(self.GetInfoBB) # get information about borrowed books
    
    def GetBook(self):
        rec = book_recognizer.Recognizer()
        rec.Create("SURF")
#        #---Функция БД, присваивающая templ список с изображениями обложек-----------
        templ = [ os.path.join("../infrastructure/Database/Books/Covers/", b) 
                for b in os.listdir("../infrastructure/Database/Books/Covers/")
                 if os.path.isfile(os.path.join("../infrastructure/Database/Books/Covers/", b)) ]
        #-----------------------------------------------------------------------------
        #---Получить видеопоток с камеры----------------------------------------------
        cap = cv2.VideoCapture(0)
        #-----------------------------------------------------------------------------
        i = 0
        l = len(templ)
        res_arr = []
        for i in range(l):
            res_arr.append(0)
        while(True): 
            _, frame = cap.read()
            cv2.imshow("web", frame)
            ch = cv2.waitKey(1)   
            recognize_result = rec.Recognize(frame, templ, 0.87)
            print(res_arr, "\n")
            for i in range(l):
                res_arr[i] = res_arr[i] + recognize_result[i]
            if max(res_arr) > 8000:
                break
        print(res_arr, "\n")
        cap.release()
        cv2.destroyAllWindows()
        idres = res_arr.index(max(res_arr))
        print("Book id = ", idres)

        
    def AddBook(self):
        print("AddBook")
    
    def GetInfoReaders(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(6)
         #disable editing
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Set the table headers
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Last name", "First name", 
                                                     "Middle name", "Phone", "Role"])
        #insert row
        self.tableWidget.verticalHeader().hide()
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem("1"))
        self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem("Вихрев"))
        self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem("Иван"))
        self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem("Борисович"))
        self.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem("+00000000000"))
        self.tableWidget.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem("Administrator"))
        #fit available space
        header = self.tableWidget.horizontalHeader()    
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        #self.tableWidget.resizeColumnsToContents()
        print("GetInfoReaders")
        
    def GetInfoBooks(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(6)
         #disable editing
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Set the table headers
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Author", "Title", 
                                                     "Publisher", "Publication date", "Cover"])
        #insert row
        self.tableWidget.verticalHeader().hide()
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem("1"))
        self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem("---"))
        #fit available space
        header = self.tableWidget.horizontalHeader()    
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        print("GetInfoBooks")
    
    def GetInfoBB(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(9)
        #disable editing
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Set the table headers
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Last name", "First name", 
                                                     "Middle name", "Phone", "Author", "Title", "Borrow date",
                                                     "Return date"])
        #insert row
        self.tableWidget.verticalHeader().hide()
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem("1"))
        self.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 6, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 7, QtWidgets.QTableWidgetItem("---"))
        self.tableWidget.setItem(rowPosition, 8, QtWidgets.QTableWidgetItem("---"))
        #fit available space
        header = self.tableWidget.horizontalHeader()    
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)
        print("GetInfoBBooks")
       
class ReaderWindow(QtWidgets.QMainWindow, ReaderWin.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) #initial design
        self.setFixedSize(self.size())
        self.pushButton.clicked.connect(self.GetBook)
        #tabel 1 with borrowed books
        self.tableWidget.setColumnCount(6)
        #disable editing
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #Рассмотреть возможность вывода обложки книги в таблицу
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Author", "Title", 
                                                    "Publisher", "Publication date", "Borrow date"])
        self.tableWidget.resizeColumnsToContents()
        #tabel 2 with previously taken books
        self.tableWidget_2.setColumnCount(7)
        #disable editing
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setHorizontalHeaderLabels(["ID", "Author", "Title", 
                                                    "Publisher", "Publication date", "Borrow date", "Return date"])
        self.tableWidget_2.resizeColumnsToContents()    
    def GetBook(self):
        print("hello")

def main():
    app = QtWidgets.QApplication(sys.argv)  # new QApplication
    window = LoginWindow()  
    window.show() 
    app.exec_()  

if __name__ == '__main__':  
    main() 