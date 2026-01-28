/**
 * CataMaze UI Main Entry Point
 */

import * as api from './api.js?v=20260127-2';
import * as ui from './ui.js?v=20260127-2';

// Game State
let gameState = {
    gameId: null,
    observation: null,
    queueSize: 0,
    autoRunning: false,
    autoRunInterval: null,
};

// Key to Action Mapping
const keyToAction = {
    'w': 'MOVE_UP',
    'a': 'MOVE_LEFT',
    's': 'MOVE_DOWN',
    'd': 'MOVE_RIGHT',
    'i': 'SHOOT_UP',
    'j': 'SHOOT_LEFT',
    'k': 'SHOOT_DOWN',
    'l': 'SHOOT_RIGHT',
    'space': 'WAIT',
};

// Game Functions
async function handleNewGame() {
    try {
        // Stop previous game if running
        stopAutoRun();

        ui.showStatus('Creating new game...', false);
        const response = await api.createGame();

        gameState.gameId = response.game_id;
        gameState.observation = response.observation;
        gameState.queueSize = response.queue_size;

        ui.elements.gameIdLabel.textContent = `Game: ${response.game_id.substring(0, 8)}...`;
        ui.updateHUD(response.observation, response.queue_size);
        ui.updateVision(response.observation.vision);
        ui.clearEventLog();
        ui.addEventToLog('New game created!');
        ui.addEventToLog('Game is running automatically. Click buttons to take actions.');

        ui.showStatus('Game running. Use WASD to move, IJKL to shoot.', false);

        // Start auto-running (automatic WAIT every 2 seconds)
        startAutoRun();
    } catch (error) {
        ui.showStatus(`Error: ${error.message}`, true);
    }
}

async function handleObserve() {
    if (!gameState.gameId) {
        ui.showStatus('No active game. Create a new game first.', true);
        return;
    }

    try {
        ui.showStatus('Observing game state...', false);
        const response = await api.observeGame(gameState.gameId);

        gameState.observation = response.observation;

        ui.updateHUD(response.observation, gameState.queueSize);
        ui.updateVision(response.observation.vision);

        ui.showStatus('Observation updated.', false);
    } catch (error) {
        ui.showStatus(`Error: ${error.message}`, true);
    }
}

async function handleQueueAction(key, isAutoWait = false) {
    if (!gameState.gameId) {
        return;
    }

    const action = keyToAction[key];
    if (!action) {
        return;
    }

    try {
        // Submit action
        const submitResponse = await api.submitAction(gameState.gameId, action);
        gameState.queueSize = submitResponse.queue_size;
        ui.elements.queueValue.textContent = submitResponse.queue_size;

        if (!isAutoWait) {
            ui.showStatus(`Executing ${action}...`, false);
        }

        // Automatically execute tick
        const tickResponse = await api.executeTick(gameState.gameId);
        gameState.observation = tickResponse.observation;
        gameState.queueSize = tickResponse.queue_size;

        ui.updateHUD(tickResponse.observation, tickResponse.queue_size);
        ui.updateVision(tickResponse.observation.vision);

        if (tickResponse.events && tickResponse.events.length > 0) {
            tickResponse.events.forEach(event => ui.addEventToLog(event));
        }

        if (!isAutoWait) {
            ui.showStatus(`${action} executed. Tick ${tickResponse.tick}`, false);
        }

        if (tickResponse.observation.game_over) {
            stopAutoRun();
            ui.showGameOverModal(tickResponse.observation.won, tickResponse.observation.alive);
        }
    } catch (error) {
        ui.showStatus(`Error: ${error.message}`, true);
        stopAutoRun();
    }
}

async function handleTick() {
    if (!gameState.gameId) {
        ui.showStatus('No active game. Create a new game first.', true);
        return;
    }

    try {
        ui.showStatus('Executing tick...', false);
        const response = await api.executeTick(gameState.gameId);

        gameState.observation = response.observation;
        gameState.queueSize = response.queue_size;

        ui.updateHUD(response.observation, response.queue_size);
        ui.updateVision(response.observation.vision);

        if (response.events && response.events.length > 0) {
            response.events.forEach(event => ui.addEventToLog(event));
        }

        ui.showStatus(`Tick ${response.tick} executed. Queue: ${response.queue_size}`, false);

        if (response.observation.game_over) {
            ui.showGameOverModal(response.observation.won, response.observation.alive);
        }
    } catch (error) {
        ui.showStatus(`Error: ${error.message}`, true);
    }
}

function startAutoRun() {
    if (!gameState.gameId) {
        return;
    }

    gameState.autoRunning = true;

    // Execute WAIT every 2 seconds automatically
    gameState.autoRunInterval = setInterval(async () => {
        if (gameState.gameId && gameState.observation && !gameState.observation.game_over) {
            try {
                await handleQueueAction('space', true); // true = silent auto-wait
            } catch (error) {
                console.error('Auto-run error:', error);
                stopAutoRun();
            }
        } else {
            stopAutoRun();
        }
    }, 2000);
}

function stopAutoRun() {
    gameState.autoRunning = false;
    if (gameState.autoRunInterval) {
        clearInterval(gameState.autoRunInterval);
        gameState.autoRunInterval = null;
    }
}

async function handleClearQueue() {
    if (!gameState.gameId) {
        ui.showStatus('No active game. Create a new game first.', true);
        return;
    }

    try {
        ui.showStatus('Clearing queue...', false);
        await api.clearQueue(gameState.gameId);

        gameState.queueSize = 0;
        ui.elements.queueValue.textContent = 0;

        ui.showStatus('Queue cleared.', false);
    } catch (error) {
        ui.showStatus(`Error: ${error.message}`, true);
    }
}

// Event Listeners
ui.elements.btnNewGame.addEventListener('click', handleNewGame);
ui.elements.btnObserve.addEventListener('click', handleObserve);
ui.elements.btnQueueView.addEventListener('click', () => {
    ui.showStatus(`Queue size: ${gameState.queueSize}`, false);
});
ui.elements.btnClearQueue.addEventListener('click', handleClearQueue);
ui.elements.btnTick.addEventListener('click', handleTick);

// Movement buttons
document.querySelectorAll('.btn-move').forEach(btn => {
    btn.addEventListener('click', () => {
        const key = btn.dataset.key;
        handleQueueAction(key);
    });
});

// Shooting buttons
document.querySelectorAll('.btn-shoot').forEach(btn => {
    btn.addEventListener('click', () => {
        const key = btn.dataset.key;
        handleQueueAction(key);
    });
});

// Modal buttons
ui.elements.modalBtnNew.addEventListener('click', () => {
    ui.hideModal();
    handleNewGame();
});
ui.elements.modalBtnClose.addEventListener('click', ui.hideModal);

// Keyboard controls
document.addEventListener('keydown', (e) => {
    const key = e.key.toLowerCase();
    const validKeys = ['w', 'a', 's', 'd', 'i', 'j', 'k', 'l', ' '];

    if (validKeys.includes(key)) {
        e.preventDefault();
        handleQueueAction(key === ' ' ? 'space' : key);
    } else if (key === 'enter') {
        e.preventDefault();
        handleTick();
    } else if (key === 'escape') {
        e.preventDefault();
        handleClearQueue();
    }
});

// Initialize
ui.initVisionGrid();
ui.showStatus('Ready. Click "New Game" to start!', false);
console.log('CataMaze UI initialized');
