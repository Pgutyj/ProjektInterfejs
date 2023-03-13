from flask import Flask
from flask import render_template, session
from flask import request, redirect, url_for
import uuid
import importlib

import graph_creation
import graph_creation as graph
from game import Game
from player import Player

app = Flask(__name__)
app.secret_key = 'v%Ftf2Sf3yl7'
games = {}



def check_simple():
    if session.get('key') and 'games' in globals():
        return True
    return False

def move(G, n1, n2):
    if not check_simple():
        return redirect('/', code=302)

    node = (n1, n2)
    if games[session['key']].current != node:
        G.add_edge(games[session['key']].current, node)
        games[session['key']].current = node
        pos = {(x, y): (y, -x) for x, y in G.nodes()}
        graph_creation.D_SH_S(G, pos)



def change_player(n1,n2):
    if not check_simple():
        return redirect('/', code=302)
    for i in range(1, 12):
        for j in range(1,10):
            if ((n1,n2),(i,j)) in graph.G.edges():
                return
            elif ((i,j),(n1,n2)) in graph.G.edges():
                return
    if games[session['key']].active_player == 0:
        games[session['key']].active_player = 1
    elif games[session['key']].active_player == 1:
        games[session['key']].active_player = 0

@app.route('/', methods=['GET', 'POST'])
def start():
    if 'key' not in session:
        session['key'] = uuid.uuid4()
    graph.refresh_graph(graph.G)

    return render_template('start.htm')

@app.route('/end', methods=['GET', 'POST'])
def end():
    if not check_simple():
        return redirect('/', code=302)
    graph.refresh_graph(graph.G)
    importlib.reload("static/empty.png")
    return render_template('end.htm')

def check_win(al, nod1,nod2):
    if not check_simple():
        return redirect('/', code=302)
    if len(al) == 1:
        if games[session['key']].active_player == 0:
            games[session['key']].players[1].score = 1
            games[session['key']].end = True
            return 1
        elif games[session['key']].active_player == 1:
            games[session['key']].players[0].score = 1
            games[session['key']].end = True
            return 1
    if (nod1,nod2) in [(0,5),(0,4),(0,6)]:
        games[session['key']].players[1].score = 1
        games[session['key']].end = True
        return 1
    if (nod1,nod2) in [(12,5),(12,4),(12,6)]:
        games[session['key']].players[0].score = 1
        games[session['key']].end = True
        return 1
    else:
        return 0

def allowed(G, n1, n2):
        l = []
        for i in range(n1 - 1, n1 + 2):
            for j in range(n2 - 1, n2 + 2):
                if ((n1, n2), (i, j)) not in G.edges():
                    if ((i, j),(n1, n2)) not in G.edges():
                        if (i,j) not in graph.outside:
                            if (i,j) != (n1,n2):
                                l.append((i, j))
        return l

@app.route('/graph/<int:nod1><int:nod2>', methods=['GET', 'POST'])
def show_graph(nod1,nod2):
    if not check_simple():
        return redirect('/', code=302)
    al = allowed(graph.G, nod1, nod2)
    if games[session['key']].end == False:
        if check_win(al,nod1,nod2) == 1:
            if games[session['key']].players[1].score == 1:
                winner = games[session['key']].players[1]
            else:
                winner = games[session['key']].players[0]
            graph.refresh_graph(graph.G)
            return render_template('end.htm', winner=winner)
    change_player(nod1,nod2)
    move(graph.G, nod1, nod2)
    al = allowed(graph.G, nod1, nod2)
    games[session['key']].stage +=1
    return render_template('graph.htm', game = games[session['key']], pilka=games[session['key']].current, al= al, stage = games[session['key']].stage)

@app.route('/mode', methods=['GET', 'POST'])
def hot_seat():
    if not check_simple():
        return redirect('/', code=302)
    graph.refresh_graph(graph.G)

    return render_template('game_mode.htm')


@app.route('/user', methods=['GET', 'POST'])
def user_form():  # put application's code here
    if not check_simple():
        return redirect('/', code=302)

    if request.method == 'POST':
        graph.refresh_graph(graph.G)
        players = [x for x in request.form.getlist('names') if x]
        return new_game(players)

    return render_template('user_form.htm')

def new_game(names):
    if not check_simple():
        return redirect('/', code=302)

    graph.refresh_graph(graph.G)
    games[session['key']] = Game(names)
    return redirect(url_for('show_graph', nod1=6, nod2=5), code=302)






if __name__ == '__main__':
    app.run(host="wierzba.wzks.uj.edu.pl", port=5111, debug=True)
