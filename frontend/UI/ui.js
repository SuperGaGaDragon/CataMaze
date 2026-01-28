/**
 * CataMaze UI Update Functions
 */

// DOM Elements
export const elements = {
    // HUD
    hpFill: document.getElementById('hp-fill'),
    hpText: document.getElementById('hp-text'),
    ammoFill: document.getElementById('ammo-fill'),
    ammoText: document.getElementById('ammo-text'),
    tickValue: document.getElementById('tick-value'),
    positionValue: document.getElementById('position-value'),
    queueValue: document.getElementById('queue-value'),
    soundValue: document.getElementById('sound-value'),

    // Vision
    visionGrid: document.getElementById('vision-grid'),

    // Event Log
    eventList: document.getElementById('event-list'),

    // Status Bar
    statusMessage: document.getElementById('status-message'),
    statusAlive: document.getElementById('status-alive'),
    statusWon: document.getElementById('status-won'),
    gameIdLabel: document.getElementById('game-id-label'),

    // Buttons
    btnNewGame: document.getElementById('btn-new-game'),
    btnResumeShow: document.getElementById('btn-resume-show'),
    btnPauseSave: document.getElementById('btn-pause-save'),
    btnObserve: document.getElementById('btn-observe'),
    btnQueueView: document.getElementById('btn-queue-view'),
    btnClearQueue: document.getElementById('btn-clear-queue'),
    btnTick: document.getElementById('btn-tick'),

    // Resume section
    resumeSection: document.getElementById('resume-section'),
    inputGameId: document.getElementById('input-game-id'),
    btnResumeConfirm: document.getElementById('btn-resume-confirm'),
    btnResumeCancel: document.getElementById('btn-resume-cancel'),

    // Game Over Modal
    modal: document.getElementById('game-over-modal'),
    modalTitle: document.getElementById('modal-title'),
    modalMessage: document.getElementById('modal-message'),
    modalBtnNew: document.getElementById('modal-btn-new'),
    modalBtnClose: document.getElementById('modal-btn-close'),

    // Pause & Save Modal
    pauseModal: document.getElementById('pause-save-modal'),
    savedGameId: document.getElementById('saved-game-id'),
    btnCopyId: document.getElementById('btn-copy-id'),
    modalBtnContinue: document.getElementById('modal-btn-continue'),
    modalBtnExit: document.getElementById('modal-btn-exit'),
};

// Initialize Vision Grid
export function initVisionGrid() {
    elements.visionGrid.innerHTML = '';
    for (let i = 0; i < 25; i++) {
        const cell = document.createElement('div');
        cell.className = 'vision-cell empty';
        cell.textContent = '·';
        elements.visionGrid.appendChild(cell);
    }
}

// Update HUD
export function updateHUD(observation, queueSize) {
    const hp = observation.hp;
    const maxHp = 5;
    const ammo = observation.ammo;
    const maxAmmo = 3;

    elements.hpFill.style.width = `${(hp / maxHp) * 100}%`;
    elements.hpText.textContent = `${hp}/${maxHp}`;

    elements.ammoFill.style.width = `${(ammo / maxAmmo) * 100}%`;
    elements.ammoText.textContent = `${ammo}/${maxAmmo}`;

    elements.tickValue.textContent = observation.time;
    elements.positionValue.textContent = `(${observation.position.x}, ${observation.position.y})`;
    elements.queueValue.textContent = queueSize;
    elements.soundValue.textContent = observation.last_sound || '[silence]';

    elements.statusAlive.textContent = observation.alive ? 'Alive: ✓' : 'Alive: ✗';
    elements.statusWon.textContent = observation.won ? 'Won: ★' : 'Won: ✗';
}

// Update Vision Grid
export function updateVision(vision) {
    const cells = elements.visionGrid.children;
    let index = 0;

    for (let row of vision) {
        for (let cell of row) {
            const cellElement = cells[index];
            const { className, text } = getCellStyle(cell);
            cellElement.className = `vision-cell ${className}`;
            cellElement.textContent = text;
            index++;
        }
    }
}

// Get Cell Style
function getCellStyle(symbol) {
    const styles = {
        '#': { className: 'wall', text: '█' },
        '.': { className: 'empty', text: '·' },
        '@': { className: 'player', text: '@' },
        'P': { className: 'agent', text: 'P' },
        'S': { className: 'start', text: 'S' },
        'E': { className: 'exit', text: 'E' },
        'A': { className: 'ammo', text: 'A' },
        'o': { className: 'bullet', text: 'o' },
    };
    return styles[symbol] || { className: 'empty', text: symbol };
}

// Add Event to Log
export function addEventToLog(event) {
    const p = document.createElement('p');
    p.textContent = event;
    elements.eventList.appendChild(p);
    elements.eventList.scrollTop = elements.eventList.scrollHeight;
}

// Clear Event Log
export function clearEventLog() {
    elements.eventList.innerHTML = '<p class="event-placeholder">No events yet. Start a new game!</p>';
}

// Show Status Message
export function showStatus(message, isError = false) {
    elements.statusMessage.textContent = message;
    elements.statusMessage.style.color = isError ? '#ff0000' : '#00ff00';
}

// Show Game Over Modal
export function showGameOverModal(won, alive) {
    if (won) {
        elements.modalTitle.textContent = '★ YOU WON! ★';
        elements.modalMessage.textContent = 'Congratulations! You escaped the maze!';
        elements.modalTitle.style.color = '#ffff00';
    } else if (!alive) {
        elements.modalTitle.textContent = '✗ GAME OVER ✗';
        elements.modalMessage.textContent = 'You died in the maze...';
        elements.modalTitle.style.color = '#ff0000';
    }
    elements.modal.classList.add('show');
}

// Hide Modal
export function hideModal() {
    elements.modal.classList.remove('show');
}

// Show Pause & Save Modal
export function showPauseSaveModal(gameId) {
    elements.savedGameId.value = gameId;
    elements.pauseModal.classList.add('show');
}

// Hide Pause & Save Modal
export function hidePauseSaveModal() {
    elements.pauseModal.classList.remove('show');
}

// Show Resume Section
export function showResumeSection() {
    elements.resumeSection.style.display = 'block';
    elements.inputGameId.value = '';
    elements.inputGameId.focus();
}

// Hide Resume Section
export function hideResumeSection() {
    elements.resumeSection.style.display = 'none';
}

// Toggle Game UI State
export function setGameUIState(isPlaying) {
    if (isPlaying) {
        elements.btnNewGame.style.display = 'none';
        elements.btnResumeShow.style.display = 'none';
        elements.btnPauseSave.style.display = 'block';
    } else {
        elements.btnNewGame.style.display = 'block';
        elements.btnResumeShow.style.display = 'block';
        elements.btnPauseSave.style.display = 'none';
    }
}
