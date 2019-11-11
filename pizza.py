#! /usr/bin/python3

import sqlite3
import sys

DB = 'test.db'


def check_correct_value(choise_of_option, diapason_of_choice):
	while True:
		if not choise_of_option.isdigit() or not int(choise_of_option) in range(1, diapason_of_choice + 1):
			print('Пожалйсте, введи правильное значение.')
			return True
		else:
			return False


class Dbconector():
	"""Dbconector - class provides methods for connection to database"""
	def __init__(self, db = DB):
		self.db = db
		self.conn, self.cursor = self.connection()

	def connection(self):
		conn = sqlite3.connect(self.db)
		return conn, conn.cursor()

	def get_all_objects(self, table):
		try:
			self.cursor.execute('SELECT * FROM {};'.format(table))
		except sqlite3.OperationalError:
			print('А нету такой таблицы!')
			sys.exit()
		return self.cursor.fetchall()

	def get_table_structure(self, table):
		self.cursor.execute('PRAGMA table_info({});'.format(table))
		return self.cursor.fetchall()

	def set_new_object(self, table, object):
		try:
			self.cursor.execute('INSERT OR IGNORE INTO {} VALUES ({});'.format(table, object))
		except sqlite3.OperationalError:
			print('Введено явно что-то ошибочное ((')
			sys.exit()
		self.conn.commit()
		return self.cursor.fetchall()

	def get_object_id(self, table, id):
		try:
			self.cursor.execute('SELECT * FROM {} WHERE id = {};'.format(table, id))
		except sqlite3.OperationalError:
			print('Введено явно что-то ошибочное ((')
			sys.exit()
		return self.cursor.fetchall()

	def get_sorted_list(self, table, order):
		try:
			self.cursor.execute('SELECT * FROM {} ORDER BY {};'.format(table, order))
		except sqlite3.OperationalError:
			print('Введено явно что-то ошибочное ((')
			sys.exit()
		return self.cursor.fetchall()

	def show_available_tables(self):
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
		return self.cursor.fetchall()

	def close_connection(self):
		self.conn.close()

def main():
	database = input("Введите имя базы данных: ")
	connector = Dbconector(database)

	print('Список таблиц в этой базе данных: ')
	print(connector.show_available_tables())

	table = input('Введите имя таблицы для вывода её содержимого: ')
	print(connector.get_all_objects(table))

	table = input('Введите имя таблицы для добавления нового объекта: ')
	print('Структура выбранной таблицы: \n' + str(connector.get_table_structure(table)))
	new_object = input('Введите новый объект в соответсвии с приведённым выше: ')
	connector.set_new_object(table, new_object)
	print(connector.get_all_objects(table))

	table = input('Введите имя таблицы для получения объекта по его ID: ')
	id_object = input('Введите ID объекта: ')
	print(connector.get_object_id(table, id_object))

	table = input('Введите имя таблицы для последующей сортировки: ')
	argument = input('Введите имя поля по которому будет осущетсвлена сортировка: ')
	print(connector.get_sorted_list(table, argument))

	connector.close_connection()

if __name__ == '__main__':
	main()