import random
import string

import requests
import bcrypt
import numpy as np

def criar():
    # criando um codigo
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=6))


def send_verification(email):
    codigo_aleatorio = criar()
    url = 'https://aplicativo-chatto-default-rtdb.firebaseio.com/Usuarios.json'

    # criptografando o codigo
    hashed_password = codigo_aleatorio.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=hashed_password, salt=salt).decode('utf-8')

    # Adicionando o codigo ao banco de dados
    data = {'verification_code': hashed_password}
    print(hashed_password)

    # Primeiro, obtenha os dados de todos os usuários
    resposta = requests.get(url)
    usuarios = resposta.json()

    # Transforme o dicionário em um array de numpy estruturado
    dados = np.array([(chave, info.get('email')) for chave, info in usuarios.items()],
                     dtype=[('chave', 'U50'), ('email', 'U100')])

    # Encontre a chave do usuário com o email correspondente
    filtro = dados[dados['email'] == email]

    if filtro.size > 0:
        chave_usuario = filtro[0]['chave']
        print(chave_usuario)
        url_patch = f'{url}/Usuarios/{chave_usuario}.json'



send_verification(email='sukunamec@gmail.com')
