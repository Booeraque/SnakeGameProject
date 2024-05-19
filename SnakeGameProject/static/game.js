let  gameIntervalId = null;
function startGame() {
    // Hide the endgame screen if there is one
    document.getElementById('endgameWindow').style.display = 'none';
    const size = document.getElementById('size').value;
    const nickname = document.getElementById('nickname').value;
    fetch('/start_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ size: size, nickname: nickname }),
    })
    .then(() => {
        updateGameView();
        document.getElementById('startingWindow').style.display = 'none';
        document.getElementById('gameWindow').style.display = 'block';
    });
}

function updateGameView() {
    fetch('/get_state')
        .then(response => response.json())
        .then(gameState => {
            // Check if the game is over
            if (gameState.game_over) {
                console.log('Game over!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                // Stop updating the game view
                if (gameIntervalId !== null) {
                    clearInterval(gameIntervalId);
                    gameIntervalId = null;
                }

                // Hide the game board and show the endgame screen
                document.getElementById('gameWindow').style.display = 'none';
                document.getElementById('endgameWindow').style.display = 'block';

                // Update the endgame text
                document.getElementById('endgame-text').innerText = gameState.endgame_text;

                // Add event listeners to the buttons
                document.getElementById('new-game-button').addEventListener('click', startGame);
            } else {
                // Clear the game board
                const gameBoard = document.getElementById('game-board');
                gameBoard.innerHTML = '';

                // Update the nickname and score
                document.getElementById('nicknameDisplay').innerText = "Nickname: " + document.getElementById('nickname').value;
                document.getElementById('scoreDisplay').innerText = "Score: " + gameState.score;

                // Draw the new game state
                for (let row of gameState.board) {
                    const rowDiv = document.createElement('div');
                    rowDiv.className = 'row';
                    for (let cell of row) {
                        const cellDiv = document.createElement('div');
                        if (cell === ' ') {
                            cellDiv.className = 'empty';
                        } else if (cell === 'H') {
                            cellDiv.className = 'head ' + gameState.snake_direction.toLowerCase();
                        } else if (cell === 'B') {
                            cellDiv.className = 'snake';
                        } else if (cell === 'F') {
                            cellDiv.className = 'food';
                        } else if (cell === 'O') {
                            cellDiv.className = 'obstacle';
                        }
                        rowDiv.appendChild(cellDiv);
                    }
                    gameBoard.appendChild(rowDiv);
                }

                // Update the game interval to match the speed
                if (gameIntervalId !== null) {
                    clearInterval(gameIntervalId);
                }
                gameIntervalId = setInterval(updateGameView, 1000 / gameState.speed);
            }
        })
        .catch(error => {
            console.log(error);
            // Stop updating the game view if there's an error
            if (gameIntervalId !== null) {
                clearInterval(gameIntervalId);
                gameIntervalId = null;
            }
        });
}

document.addEventListener('keydown', function(event) {
    let direction;
    switch (event.code) {
        case 'ArrowUp':
            direction = 'UP';
            break;
        case 'ArrowDown':
            direction = 'DOWN';
            break;
        case 'ArrowLeft':
            direction = 'LEFT';
            break;
        case 'ArrowRight':
            direction = 'RIGHT';
            break;
        default:
            return;  // Quit when this doesn't handle the key event.
    }
    // Send the new direction to the server
    fetch('/update_direction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ direction: direction }),
    })
    .then(response => response.json())
});