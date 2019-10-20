import csv # модуль для работы с csv-файлами

from datetime import datetime

# импорт всех интерфейсов:
from IDatabaseInterfaces import IDatabaseBRM, IDatabaseAuthService
from IDatabaseInterfaces import IDatabaseFRM, IDatabaseGUI

from Entities.Book import Book
from Entities.User import User
from Entities.Role import Role
from Entities.Author import Author
from Entities.Model import Model

# ПРИМЕЧАНИЕ: для корректной работы методов оформляйте строки в БД правильно.
# При записи любых данных в файлы БД вручную обязательно в конце сделать
# перевод строки на новую.

class CSVDatabase(IDatabaseBRM, IDatabaseAuthService,
                  IDatabaseFRM, IDatabaseGUI):
    # dbRootDir = 'infrastructure/Database/'
    dbRootDir = 'Database/'
    
    def __init__(self):
        self.fBooks = self.dbRootDir + 'Books/Books.csv'
        self.fAuthors = self.dbRootDir + 'Books/Authors.csv'
        self.fAuthorship = self.dbRootDir + 'Books/Authorship.csv'
        self.fUsers = self.dbRootDir + 'Users/Users.csv'
        self.fUserModel = self.dbRootDir + 'Users/UserModel.csv'
        self.fUserRole = self.dbRootDir + 'Users/UserRole.csv'
        self.fRoles = self.dbRootDir + 'Users/Roles.csv'
        self.fModels = self.dbRootDir + 'Users/Models.csv'
        self.fReaders = self.dbRootDir + 'Readers.csv'
        #
        self.dUser = {'user_id': 'user_id', 'phone': 'phone',
                         'first_name': 'first_name', 'last_name': 'last_name',
                         'middle_name': 'middle_name'}
        self.dBook = {'book_id': 'book_id', 'file_path': 'file_path',
                      'title': 'title', 'year': 'year',
                      'publisher': 'publisher', 'authors': 'authors'}
        self.dAuthor = {'author_id': 'author_id', 'first_name': 'first_name',
                        'last_name': 'last_name', 'middle_name': 'middle_name'}
        self.dAuthorship = {'book_id': 'book_id', 'author_id': 'author_id'}
        self.dRole = {'role_id': 'role_id', 'description': 'description'}
        self.dModel = {'model_id': 'model_id', 'file_path': 'file_path',
                       'name_model': 'name_model'}
        self.dReader = {'user_id': 'user_id', 'book_id': 'book_id',
                        'borrow_date': 'borrow_date', 'return_date': 'return_date'}
    
    # Данную функцию нужно вынести за пределы этого файла. Функция генерирует
    # ID для новых книг и пользователей.
    # def GetNewID(self):
        # newID = str(datetime.now())
        # newID = newID.replace('-', '')
        # newID = newID.replace(' ', '')
        # newID = newID.replace(':', '')
        # newID = newID.replace('.', '')
        # return newID
        
    def ClearCSV(self, file_path):
        fileR = open(file_path, newline = '')
        header = fileR.readline()
        fileR.close()
        fileOverW = open(file_path, 'w', newline = '')
        fileOverW.write(header)
        fileOverW.close()
        
    def ClearAllCSV(self):
        files = [self.fAuthors, self.fAuthorship, self.fBooks, self.fModels,
                 self.fRoles, self.fUserModel, self.fUserRole,
                 self.fUsers, self.fReaders]
        for f in files:
            self.ClearCSV(f)
    
    def GetBookCovers(self):
        fileBooksR = open(self.fBooks, newline = '')
        fileAuthorsR = open(self.fAuthors, newline = '')
        fileAuthorshipR = open(self.fAuthorship, newline = '')
        #
        book = []
        authors = []
        #
        readerBooks = csv.DictReader(fileBooksR, delimiter = ',')
        readerAuthorship = csv.DictReader(fileAuthorshipR, delimiter = ',')
        readerAuthors = csv.DictReader(fileAuthorsR, delimiter = ',')
        # захожу в цикл по строкам файла Books.csv
        for lineBooks in readerBooks:
            # захожу в цикл по строкам файла Authorship.csv
            # с фиксированным значением book_id
            fileAuthorshipR.seek(0) # возвращаю указатель в начало файла
            for lineAuthorship in readerAuthorship:
                # нахожу нужные(ый) author_id
                if (lineAuthorship[self.dAuthorship['book_id']] ==
                    lineBooks[self.dBook['book_id']]):
                    # захожу в цикл по строкам файла Authors.csv
                    # с фиксированным значением author_id
                    fileAuthorsR.seek(0) # возвращаю указатель в начало файла
                    for lineAuthors in readerAuthors:
                        # имея author_id нахожу нужного автора
                        # и добавляю его в authors[]
                        if (lineAuthorship[self.dAuthorship['author_id']] ==
                            lineAuthors[self.dAuthor['author_id']]):
                            authors.append(Author(lineAuthors[self.dAuthor['author_id']],
                                                  lineAuthors[self.dAuthor['first_name']],
                                                  lineAuthors[self.dAuthor['last_name']],
                                                  lineAuthors[self.dAuthor['middle_name']]))
                            break
            book.append(Book(lineBooks[self.dBook['book_id']],
                             lineBooks[self.dBook['file_path']],
                             lineBooks[self.dBook['title']],
                             lineBooks[self.dBook['year']],
                             lineBooks[self.dBook['publisher']],
                             authors.copy()))
            authors.clear()
        #
        fileBooksR.close()
        fileAuthorsR.close()
        fileAuthorshipR.close()
        return book
    
    def AddUser(self, user):
        fieldnamesUser = [self.dUser['user_id'], self.dUser['phone'],
                               self.dUser['first_name'], self.dUser['last_name'],
                               self.dUser['middle_name']]
        fileUsersR = open(self.fUsers, newline = '')
        fileUsersW = open(self.fUsers, 'a', newline = '')
        # 'a' - дозапись в файл, 'w' - перезапись файла
        reader = csv.DictReader(fileUsersR, delimiter = ',')
        # если такой пользователь уже есть в базе, то raise
        for line in reader:
            if ((user.first_name == line[self.dUser['first_name']]) and
                (user.last_name == line[self.dUser['last_name']]) and
                (user.middle_name == line[self.dUser['middle_name']]) and
                (str(user.phone) == line[self.dUser['phone']])):
                fileUsersR.close()
                fileUsersW.close()
                raise Exception('This user is already registered!')
        #
        writer = csv.DictWriter(fileUsersW, fieldnames = fieldnamesUser,
                                delimiter = ',')
        writer.writerow({self.dUser['user_id']: user.user_id,
                         self.dUser['phone']: user.phone,
                         self.dUser['first_name']: user.first_name,
                         self.dUser['last_name']: user.last_name,
                         self.dUser['middle_name']: user.middle_name})
        #
        fileUsersR.close()
        fileUsersW.close()
    
    def GetUser(self, user_id):
        # РАЗОБРАТЬСЯ С ENUMERATE!
        fileUsersR = open(self.fUsers, newline = '')
        fileUserRoleR = open(self.fUserRole, newline = '')
        fileRolesR = open(self.fRoles, newline = '')
        # ищу пользователя по user_id
        reader = csv.DictReader(fileUsersR, delimiter = ',')
        user = User(-1, -1, -1, -1, -1)
        for i, line in enumerate(reader, 1):
            if (i == user_id):
                user = User(line[self.dUser['user_id']],
                            line[self.dUser['phone']],
                            line[self.dUser['first_name']],
                            line[self.dUser['last_name']],
                            line[self.dUser['middle_name']])
                break
        reader = csv.DictReader(fileUserRoleR, delimiter = ',')
        role_id = 0
        # зная user_id, нахожу соответсвующее значение role_id
        for i, line in enumerate(reader, 1):
            if (i == user_id):
                role_id = int(line[self.dRole['role_id']])
                break
        # зная role_id, нахожу полную информацию об этой роли
        reader = csv.DictReader(fileRolesR, delimiter = ',')
        role = Role(-1, -1)
        for i, line in enumerate(reader, 1):
            if (i == role_id):
                role = Role(line[self.dRole['role_id']],
                            line[self.dRole['description']])
                break
        #
        fileUsersR.close()
        fileUserRoleR.close()
        fileRolesR.close()
        return (user, role) # tuple()
    
    def GetTrainedModel(self, name_model):
        fileModelsR = open(self.fModels, newline = '')
        reader = csv.DictReader(fileModelsR, delimiter = ',')
        for line in reader:
            if (name_model == line[self.dModel['name_model']]):
                return line[self.dModel['file_path']]
            
        fileModelsR.close()
        raise Exception('This model does not exist!')
    
    def AddModel(self, model):
        fieldnamesModel = [self.dModel['model_id'], self.dModel['file_path'],
                           self.dModel['name_model']]
        fileModelsW = open(self.fModels, 'a', newline = '')
        writer = csv.DictWriter(fileModelsW, fieldnames = fieldnamesModel,
                                delimiter = ',')
        writer.writerow({self.dModel['model_id']: model.model_id,
                         self.dModel['file_path']: model.file_path,
                         self.dModel['name_model']: model.name_model})
        #
        fileModelsW.close()
        
    def AddBook(self, book):
        fileBooksR = open(self.fBooks, newline = '')
        # если такая книга уже есть, то raise
        readerBooks = csv.DictReader(fileBooksR, delimiter = ',')
        for line in readerBooks:
            # file_path не сравниваю, т.к. могут быть 2 разных фото одной книги
            if ((book.title == line[self.dBook['title']]) and
                (book.year == line[self.dBook['year']]) and
                (book.publisher == line[self.dBook['publisher']])):
                fileBooksR.close()
                raise Exception('This book is already added!')
        fileBooksW = open(self.fBooks, 'a', newline = '')
        fileAuthorshipW = open(self.fAuthorship, 'a', newline = '')
        fileAuthorsR = open(self.fAuthors, newline = '')
        fileAuthorsW = open(self.fAuthors, 'a', newline = '')
        # в таблицу книг дописываю одну новую:
        fieldnamesBooks = [self.dBook['book_id'], self.dBook['file_path'],
                           self.dBook['title'], self.dBook['year'],
                           self.dBook['publisher']]
        writerBooks = csv.DictWriter(fileBooksW, fieldnames = fieldnamesBooks,
                                     delimiter = ',')
        writerBooks.writerow({self.dBook['book_id']: book.book_id,
                              self.dBook['file_path']: book.file_path,
                              self.dBook['title']: book.title,
                              self.dBook['year']: book.year,
                              self.dBook['publisher']: book.publisher})
        # 
        readerAuthors = csv.DictReader(fileAuthorsR, delimiter = ',')
        fieldnamesAuthors = [self.dAuthor['author_id'], self.dAuthor['first_name'],
                             self.dAuthor['last_name'], self.dAuthor['middle_name']]
        writerAuthors = csv.DictWriter(fileAuthorsW,
                                       fieldnames = fieldnamesAuthors,
                                       delimiter = ',')
        fieldnamesAuthorship = [self.dAuthorship['book_id'],
                                self.dAuthorship['author_id']]
        writerAuthorship = csv.DictWriter(fileAuthorshipW,
                                          fieldnames = fieldnamesAuthorship,
                                          delimiter = ',')
        for aut in book.authors:
            new_author_id = 0
            for line in readerAuthors:
                # проверяю, есть ли в файле с Authors.csv, автор, который написал книгу, которую мы добавляем
                if ((aut.first_name == line[self.dAuthor['first_name']]) and
                    (aut.last_name == line[self.dAuthor['last_name']]) and
                    (aut.middle_name == line[self.dAuthor['middle_name']])):
                    # если да, то его id будет ассоциироваться с id книги, которую мы добавляем
                    new_author_id = line[self.dAuthor['author_id']]
            # если нет, то занесём автора в базу
            if (new_author_id == 0):
                writerAuthors.writerow({self.dAuthor['author_id']: aut.author_id,
                                        self.dAuthor['first_name']: aut.first_name,
                                        self.dAuthor['last_name']: aut.last_name,
                                        self.dAuthor['middle_name']: aut.middle_name})
            writerAuthorship.writerow({self.dBook['book_id']: book.book_id,
                                       self.dAuthor['author_id']: aut.author_id})
            fileAuthorsR.seek(0)
            fileAuthorsW.seek(0)
        #
        fileBooksR.close()
        fileBooksW.close()
        fileAuthorsR.close()
        fileAuthorsW.close()
        fileAuthorshipW.close()
    
    def GetAllUsers(self):
        fileUsersR = open(self.fUsers, newline = '')
        reader = csv.DictReader(fileUsersR, delimiter = ',')
        user = []
        for line in reader:
            user.append(User(line[self.dUser['user_id']],
                             line[self.dUser['phone']],
                             line[self.dUser['first_name']],
                             line[self.dUser['last_name']],
                             line[self.dUser['middle_name']]))
        #
        fileUsersR.close()
        return user
    
    def GetAllBooks(self):
        return self.GetBookCovers()
    
    def GetBorrowedBooks(self):
        fileBooksR = open(self.fBooks, newline = '')
        fileUsersR = open(self.fUsers, newline = '')
        fileAuthorsR = open(self.fAuthors, newline = '')
        fileAuthorshipR = open(self.fAuthorship, newline = '')
        fileReadersR = open(self.fReaders, newline = '')
        user = []
        book = []
        date1 = []
        date2 = []
        authors = []
        readerReaders = csv.DictReader(fileReadersR, delimiter = ',')
        readerUsers = csv.DictReader(fileUsersR, delimiter = ',')
        readerBooks = csv.DictReader(fileBooksR, delimiter = ',')
        readerAuthorship = csv.DictReader(fileAuthorshipR, delimiter = ',')
        readerAuthors = csv.DictReader(fileAuthorsR, delimiter = ',')
        # захожу в цикл по строкам файла Readers.csv
        for lineReaders in readerReaders:
            # захожу в цикл по строкам файла Books.csv с фиксированным
            # значением user_id
            fileUsersR.seek(0) # возвращаю указатель в начало файла
            for lineUsers in readerUsers:
                # нахожу нужного пользователя и добавляю его данные в user[]
                if (lineUsers[self.dUser['user_id']] ==
                    lineReaders[self.dReader['user_id']]):
                    user.append(User(lineUsers[self.dUser['user_id']],
                                     lineUsers[self.dUser['phone']],
                                     lineUsers[self.dUser['first_name']],
                                     lineUsers[self.dUser['last_name']],
                                     lineUsers[self.dUser['middle_name']]))
                    break
            # захожу в цикл по строкам файла Authorship.csv с фиксированным
            # значением book_id
            fileAuthorshipR.seek(0) # возвращаю указатель в начало файла
            for lineAuthorship in readerAuthorship:
                # нахожу нужные(ый) author_id
                if (lineAuthorship[self.dAuthorship['book_id']] ==
                    lineReaders[self.dReader['book_id']]):
                    # захожу в цикл по строкам файла Authors.csv с
                    # фиксированным значением author_id
                    fileAuthorsR.seek(0) # возвращаю указатель в начало файла
                    for lineAuthors in readerAuthors:
                        # имея author_id нахожу нужного автора и добавляю его
                        # в authors[]
                        if (lineAuthorship[self.dAuthorship['author_id']] ==
                            lineAuthors[self.dAuthor['author_id']]):
                            authors.append(Author(lineAuthors[self.dAuthor['author_id']],
                                                  lineAuthors[self.dAuthor['first_name']],
                                                  lineAuthors[self.dAuthor['last_name']],
                                                  lineAuthors[self.dAuthor['middle_name']]))
                            break
            # добавляю нужную дату взятия книги в date1[]
            date1.append(lineReaders[self.dReader['borrow_date']])
            # добавляю нужную дату сдачи книги в date2[]
            date2.append(lineReaders[self.dReader['return_date']])
            #
            # захожу в цикл по строкам файла Books.csv с фиксированным
            # значением book_id
            fileBooksR.seek(0) # возвращаю указатель в начало файла
            for lineBooks in readerBooks:
                # нахожу нужную книгу
                if (lineBooks[self.dBook['book_id']] ==
                    lineReaders[self.dReader['book_id']]):
                    # добавляю её в book[]
                    book.append(Book(lineBooks[self.dBook['book_id']],
                                     lineBooks[self.dBook['file_path']],
                                     lineBooks[self.dBook['title']],
                                     lineBooks[self.dBook['year']],
                                     lineBooks[self.dBook['publisher']],
                                     authors.copy()))
                    authors.clear()
                    break
        #
        fileUsersR.close()
        fileBooksR.close()
        fileAuthorsR.close()
        fileAuthorshipR.close()
        fileReadersR.close()
        return (book, date1, date2, user) # tuple()

    def ChangeBookStatus(self, user_id, book_id, status):
        borrowDate = ''
        fileReadersR = open(self.fReaders, 'r', newline = '')
        # статус = 1 - взять книгу
        # статус = 2 - сдать книгу
        # return_date == -1 - книга не сдана
        reader = csv.DictReader(fileReadersR, delimiter = ',')
        for line in reader:
            # нахожу нужную дату по id книги и пользователя
            if (line[self.dReader['book_id']] == str(book_id) and
                line[self.dReader['user_id']] == str(user_id)):
                # если эту книгу этот пользователь уже брал и возвращал
                if (line[self.dReader['return_date']] != '-1'):
                    continue
                # если же он книгу взял, но не вернул
                borrowDate = line[self.dReader['borrow_date']]
        if (status == 1):
            fileReadersW = open(self.fReaders, 'a', newline = '')
            fieldnames = [self.dReader['user_id'], self.dReader['book_id'],
                          self.dReader['borrow_date'],
                          self.dReader['return_date']]
            writer = csv.DictWriter(fileReadersW, fieldnames = fieldnames,
                                    delimiter = ',')
            writer.writerow({self.dReader['user_id']: user_id,
                             self.dReader['book_id']: book_id,
                             self.dReader['borrow_date']: datetime.strftime(datetime.now(), '%d.%m.%Y'),
                             self.dReader['return_date']: '-1'})
            fileReadersW.close()
        if (status == 2):
            fileReadersR.seek(0)
            lines = fileReadersR.readlines()
            fileReadersOverW = open(self.fReaders, 'w', newline = '')
            s = str(user_id) + ',' + str(book_id) + ',' + borrowDate + ','
            for line in lines:
                line = line.strip()
                if line == s + '-1':
                    fileReadersOverW.write(s +
                                           datetime.strftime(datetime.now(), '%d.%m.%Y') +
                                           '\r' + '\n')
                else:
                    fileReadersOverW.write(line + '\r' + '\n')
            fileReadersOverW.close()
        #
        fileReadersR.close()

if __name__ == '__main__':
    """main"""