from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def new_board():
    return ['' for _ in range(9)]

def check_winner(board):
    combos = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
        (0, 4, 8), (2, 4, 6)              # diags
    ]
    for a, b, c in combos:
        if board[a] != '' and board[a] == board[b] == board[c]:
            return board[a]
    if '' not in board:
        return 'Draw'
    return None

# Minimax AI
def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == 'O': return 1
    if winner == 'X': return -1
    if winner == 'Draw': return 0

    scores = []
    for i in range(9):
        if board[i] == '':
            board[i] = 'O' if is_maximizing else 'X'
            score = minimax(board, not is_maximizing)
            scores.append(score)
            board[i] = ''

    return max(scores) if is_maximizing else min(scores)

def best_move(board):
    best_score = -float('inf')
    move = -1
    for i in range(9):
        if board[i] == '':
            board[i] = 'O'
            score = minimax(board, False)
            board[i] = ''
            if score > best_score:
                best_score = score
                move = i
    if move != -1:
        board[move] = 'O'
    return board

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    board = data['board']
    index = data['index']

    if board[index] == '':
        board[index] = 'X'
        winner = check_winner(board)
        if not winner:
            board = best_move(board)
            winner = check_winner(board)
    else:
        return jsonify({'error': 'Invalid move'}), 400

    return jsonify({'board': board, 'winner': winner})

if __name__ == '__main__':
    app.run(debug=True)
