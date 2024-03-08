from flask import Flask, render_template, request, redirect, url_for, session, flash
from tinydb import TinyDB, Query
from dobot import Dobot
from serial.tools import list_ports
from random import randint


app = Flask(__name__)
dobot = Dobot()

dbUsario = TinyDB('coordenadas.json', indent=4)

@app.route('/conexao')
def conexao():
    portas_disponiveis = list_ports.comports()

    portas = [x.device for x in portas_disponiveis]

    return render_template('conectarDobot.html', portas=portas)

@app.route('/conectar', methods=['POST'])
def conectar():
    porta = request.form.get('porta')

    if dobot.conectar(porta):
        return "Conectado ao dobot."
    else:
        return "Falha ao conectar."

@app.route('/novo')
def novo():
    return render_template('novo_cadastro.html')

@app.route('/novo_cadastro', methods=['POST'])
def novo_cadastro():

    nome = request.form.get('nome')
    # Recebo o request que foi pego do meu formulário
    x = float(request.form.get('x'))
    y = float(request.form.get('y'))
    z = float(request.form.get('z'))
    r = float(request.form.get('r'))

    dobot.ir_para(x, y, z, r)
    

    dbUsario.insert({'x': x, 'y': y, 'z': z}, doc_id=randint(0, 1000))
    return render_template('novo_cadastro.html')

@app.route('/pegar_caminho')
def pegar_caminhoar():
    pegar_caminhoar = dbUsario.all()
    return render_template('caminho.html', coordenadas=dbUsario.all())

@app.route('/listas_caminhos')
def listas_caminhos():
    # return render_template('listas_caminhos.html', coordenadas=dbUsario.all(), id= dbUsario.all())
    
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')

    # Busca no banco de dados o usuário e senha
    procura = Query()

    # Verifica se o usuário e senha estão no banco de dados
    resultado = dbUsario.search((procura.usuario == usuario) & (procura.senha == senha))

    # Busca vazia, usuário ou senha inválidos
    if resultado == []:
        return render_template('login.html', erro="Usuário ou senha inválidos")
    else:
        return render_template('home.html', usuarioLogado=usuario)

@app.route('/atualizar/<int:id>')
def atualizar(id):
    usuario = dbUsario.get(doc_id=id)
    return render_template('editar.html', usuario=usuario)

@app.route('/deletar/<int:id>')
def deletar(id):
    dbUsario.remove(doc_ids=[id])
    return redirect(url_for('pegar_caminho'))


