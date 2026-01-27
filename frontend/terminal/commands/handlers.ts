/**
 * CataMaze command handlers
 */
import { apiClient, Observation } from '../apiClient';
import type { CommandResult } from '@patch/modules/terminal/types';
import {
  renderGameState,
  renderEventLog,
  renderGameOver,
  renderHelp,
} from '../renderer';

interface GameState {
  gameId: string | null;
  observation: Observation | null;
  queueSize: number;
}

export const keyToAction: Record<string, string> = {
  w: 'MOVE_UP',
  a: 'MOVE_LEFT',
  s: 'MOVE_DOWN',
  d: 'MOVE_RIGHT',
  up: 'MOVE_UP',
  left: 'MOVE_LEFT',
  down: 'MOVE_DOWN',
  right: 'MOVE_RIGHT',
  i: 'SHOOT_UP',
  j: 'SHOOT_LEFT',
  k: 'SHOOT_DOWN',
  l: 'SHOOT_RIGHT',
  space: 'WAIT',
  '.': 'WAIT',
};

export async function handleNew(gameStateRef: { current: GameState }): Promise<CommandResult> {
  try {
    const response = await apiClient.createGame();
    gameStateRef.current = {
      gameId: response.game_id,
      observation: response.observation,
      queueSize: response.queue_size,
    };
    return {
      output: [
        '=== NEW GAME STARTED ===',
        `Game ID: ${response.game_id}`,
        '',
        ...renderGameState(response.observation),
        '',
        'Use "catamaze action <key>" to move/shoot, "catamaze tick" to execute.',
      ],
    };
  } catch (error: any) {
    return { output: [`Error: ${error.message}`], error: true };
  }
}

export async function handleAction(
  gameStateRef: { current: GameState },
  key: string | undefined
): Promise<CommandResult> {
  if (!gameStateRef.current.gameId) {
    return { output: ['No active game. Use "catamaze new" to start.'], error: true };
  }
  if (!key) {
    return { output: ['Usage: catamaze action <key>', 'Keys: w/a/s/d, i/j/k/l, space'], error: true };
  }
  const action = keyToAction[key.toLowerCase()];
  if (!action) {
    return { output: [`Unknown key: ${key}`, 'Valid keys: w/a/s/d, i/j/k/l, space'], error: true };
  }
  try {
    const response = await apiClient.submitAction(gameStateRef.current.gameId, action);
    gameStateRef.current.queueSize = response.queue_size;
    return {
      output: [
        `Action queued: ${action}`,
        `Queue size: ${response.queue_size}`,
        'Use "catamaze tick" to execute.',
      ],
    };
  } catch (error: any) {
    return { output: [`Error: ${error.message}`], error: true };
  }
}

export async function handleTick(gameStateRef: { current: GameState }): Promise<CommandResult> {
  if (!gameStateRef.current.gameId) {
    return { output: ['No active game. Use "catamaze new" to start.'], error: true };
  }
  try {
    const response = await apiClient.executeTick(gameStateRef.current.gameId);
    gameStateRef.current.observation = response.observation;
    gameStateRef.current.queueSize = response.queue_size;
    const obs = response.observation;
    const output = [...renderGameState(obs, response.tick)];
    if (response.events.length > 0) {
      output.push('', ...renderEventLog(response.events));
    }
    if (obs.game_over) {
      output.push(...renderGameOver(obs.won, obs.alive));
    }
    return { output };
  } catch (error: any) {
    return { output: [`Error: ${error.message}`], error: true };
  }
}

export async function handleClear(gameStateRef: { current: GameState }): Promise<CommandResult> {
  if (!gameStateRef.current.gameId) {
    return { output: ['No active game.'], error: true };
  }
  try {
    const response = await apiClient.clearQueue(gameStateRef.current.gameId);
    gameStateRef.current.queueSize = 0;
    return {
      output: [response.message, 'Queue cleared. You can start queueing new actions.'],
    };
  } catch (error: any) {
    return { output: [`Error: ${error.message}`], error: true };
  }
}

export async function handleObserve(gameStateRef: { current: GameState }): Promise<CommandResult> {
  if (!gameStateRef.current.gameId) {
    return { output: ['No active game.'], error: true };
  }
  try {
    const response = await apiClient.observeGame(gameStateRef.current.gameId);
    const obs = response.observation;
    return {
      output: [
        '=== CURRENT STATE ===',
        '',
        ...renderGameState(obs),
      ],
    };
  } catch (error: any) {
    return { output: [`Error: ${error.message}`], error: true };
  }
}

export async function handleResume(
  gameStateRef: { current: GameState },
  gameId: string | undefined
): Promise<CommandResult> {
  if (!gameId) {
    return { output: ['Usage: catamaze resume <game_id>'], error: true };
  }
  try {
    const response = await apiClient.resumeGame(gameId);
    gameStateRef.current = {
      gameId: response.game_id,
      observation: response.observation,
      queueSize: response.queue_size,
    };
    const obs = response.observation;
    return {
      output: [
        '=== GAME RESUMED ===',
        `Game ID: ${response.game_id}`,
        `Queue size: ${response.queue_size}`,
        '',
        ...renderGameState(obs),
      ],
    };
  } catch (error: any) {
    return { output: [`Error: ${error.message}`], error: true };
  }
}
