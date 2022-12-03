import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='rafael123'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")

cursor.execute("CREATE DATABASE `jogoteca`;")

cursor.execute("USE `jogoteca`;")

# criando tabelas
TABLES = {}
TABLES['Jogos'] = ('''
      CREATE TABLE `jogos` (
      `id` int NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `categoria` varchar(40) NOT NULL,
      `console` varchar(20) NOT NULL,
      `descricao` varchar(500) NOT NULL,
      PRIMARY KEY (`id`)
      ) DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['User'] = ('''
      CREATE TABLE `User` (
      `id` int NOT NULL AUTO_INCREMENT,
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `email` varchar(150) NOT NULL,
      `idade` varchar(2) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`id`)
      ) DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Comentario'] = (''' 
      CREATE TABLE `Comentario` (
      `id` int NOT NULL AUTO_INCREMENT,
      `comentario` varchar(250) NULL,
      `jogo_id` int,
      PRIMARY KEY (`id`)
      ) DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')



for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo jogos
jogos_sql = 'INSERT INTO jogos (nome, categoria, console, descricao) VALUES (%s, %s, %s, %s)'
jogos = [
      ('Tetris', 'Puzzle', 'Atari', 'empilhar tetraminós que descem a tela.'),
      ('God of War', 'Hack n Slash', 'PS2', 'matador de deuses'),
      ('Valorant', 'FPS', 'PC', ' FPS tático.'),
      ('League Of Legends', 'MOBA', 'PC', 'teste'),
]
cursor.executemany(jogos_sql, jogos)

cursor.execute('select * from jogoteca.jogos')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

cursor.execute('ALTER TABLE comentario ADD FOREIGN KEY (jogo_id) REFERENCES jogos(id);')

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()