from flask import Flask, render_template, request, jsonify

from SourceCode.Snake import Snake
from SourceCode.SnakeGame import SnakeGame
from SourceCode.GameLogic import GameLogic

app = Flask(__name__)
game = None
# TODO: Make the game over screen prettier
@app.route('/start_game', methods=['POST'])
def start_game():
    global game
    size = int(request.json.get('size', 10))  # Convert size to integer
    nickname = request.json.get('nickname')  # Get the nickname from the request
    game = SnakeGame(size, nickname)  # Create a new game instance
    game.start_game()  # Start the game
    return jsonify(game.get_state()), 200

@app.route('/get_state', methods=['GET'])
def get_state():
    if game is None or game.game_logic.game_over:
        return jsonify(game.get_state()), 400
    game.game_logic.update_game()  # Update the game state
    return jsonify(game.get_state()), 200

@app.route('/update_direction', methods=['POST'])
def update_direction():
    direction = request.json.get('direction')
    # Check if the new direction is opposite to the current direction
    opposite_directions = [('UP', 'DOWN'), ('DOWN', 'UP'), ('LEFT', 'RIGHT'), ('RIGHT', 'LEFT')]
    if (game.game_logic.snake.direction, direction) not in opposite_directions:
        game.game_logic.snake.direction = direction  # Update the direction of the snake
    return jsonify(game.get_state()), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')