/**
 * CataMaze UI Main Entry Point
 */

import * as api from './api.js';
import * as ui from './ui.js';

// Game State
let gameState = {
    gameId: null,
    observation: null,
    queueSize: 0,
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

// Placeholder functions (to be implemented in later stages)
async function handleNewGame() {
    ui.showStatus('Creating new game...', false);
    // To be implemented in Stage 4B
}

async function handleObserve() {
    ui.showStatus('Observing game state...', false);
    // To be implemented in Stage 4B
}

async function handleQueueAction(key) {
    ui.showStatus(`Queueing action: ${key}...`, false);
    // To be implemented in Stage 4C
}

async function handleTick() {
    ui.showStatus('Executing tick...', false);
    // To be implemented in Stage 4C
}

async function handleClearQueue() {
    ui.showStatus('Clearing queue...', false);
    // To be implemented in Stage 4C
}

// Event Listeners
ui.elements.btnNewGame.addEventListener('click', handleNewGame);
ui.elements.btnObserve.addEventListener('click', handleObserve);
ui.elements.btnQueueView.addEventListener('click', () => {
    ui.showStatus(`Queue size: ${gameState.queueSize}`, false);
});
ui.elements.btnClearQueue.addEventListener('click', handleClearQueue);
ui.elements.btnWait.addEventListener('click', () => handleQueueAction('space'));
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
