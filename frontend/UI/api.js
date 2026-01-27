/**
 * CataMaze API Client
 */

// API Configuration
export const API_BASE_URL = 'https://catamaze.catachess.com';

// API Call Helper
export async function apiCall(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' },
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
}

// API Methods
export async function createGame() {
    return apiCall('/game/new', 'POST');
}

export async function submitAction(gameId, action) {
    return apiCall('/game/action', 'POST', { game_id: gameId, action });
}

export async function executeTick(gameId) {
    return apiCall('/game/tick', 'POST', { game_id: gameId });
}

export async function clearQueue(gameId) {
    return apiCall('/game/clear_queue', 'POST', { game_id: gameId });
}

export async function observeGame(gameId) {
    return apiCall(`/game/observe?game_id=${gameId}`);
}

export async function resumeGame(gameId) {
    return apiCall('/game/resume', 'POST', { game_id: gameId });
}
