/**
 * CataMaze terminal command
 * Usage: catamaze <subcommand> [args]
 */
import { Observation } from '../apiClient';
import type { Command, CommandContext, CommandResult } from '@patch/modules/terminal/types';
import {
  handleNew,
  handleAction,
  handleTick,
  handleClear,
  handleObserve,
  handleResume,
} from './handlers';

interface GameState {
  gameId: string | null;
  observation: Observation | null;
  queueSize: number;
}

function showHelp(): string[] {
  return [
    '=== CataMaze Commands ===',
    '',
    'catamaze new              - Start a new game',
    'catamaze action <key>     - Queue an action',
    'catamaze tick             - Execute one tick',
    'catamaze clear            - Clear action queue (ESC)',
    'catamaze observe          - View current state',
    'catamaze resume <id>      - Resume a game',
    '',
    'Movement keys: w/a/s/d or arrow keys',
    'Shooting keys: i/j/k/l (up/left/down/right)',
    'Wait: space or .',
    '',
    'Example: catamaze action w',
  ];
}

export function createCataMazeCommand(gameStateRef: { current: GameState }): Command {
  return {
    name: 'catamaze',
    aliases: ['cm', 'cata'],
    description: 'CataMaze game commands',
    usage: 'catamaze <new|action|tick|clear|observe|resume> [args]',
    handler: async (ctx: CommandContext): Promise<CommandResult> => {
      const subcommand = ctx.args[0]?.toLowerCase();

      if (!subcommand || subcommand === 'help') {
        return { output: showHelp() };
      }

      switch (subcommand) {
        case 'new':
          return handleNew(gameStateRef);
        case 'action':
        case 'a':
          return handleAction(gameStateRef, ctx.args[1]);
        case 'tick':
        case 't':
          return handleTick(gameStateRef);
        case 'clear':
        case 'esc':
          return handleClear(gameStateRef);
        case 'observe':
        case 'obs':
        case 'o':
          return handleObserve(gameStateRef);
        case 'resume':
        case 'r':
          return handleResume(gameStateRef, ctx.args[1]);
        default:
          return {
            output: [`Unknown subcommand: ${subcommand}`, 'Type "catamaze help" for usage.'],
            error: true,
          };
      }
    },
  };
}
