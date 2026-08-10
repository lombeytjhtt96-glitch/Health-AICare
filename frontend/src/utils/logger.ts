/**
 * frontend/src/utils/logger.ts
 * 
 * Professional, unified logger for the frontend matching the backend format.
 * Format: HH:MM:SS | LEVEL | COMPONENT | EMOJI MESSAGE
 */

type LogLevel = 'DEBUG' | 'INFO' | 'WARN' | 'ERROR';

const COLORS = {
  DEBUG: 'color: #7f8c8d; font-weight: normal;',
  INFO: 'color: #2ecc71; font-weight: bold;',
  WARN: 'color: #f39c12; font-weight: bold;',
  ERROR: 'color: #e74c3c; font-weight: bold;',
  RESET: 'color: inherit; font-weight: normal;',
  TIMESTAMP: 'color: #95a5a6; font-family: monospace;',
  COMPONENT: 'color: #3498db; font-weight: bold;',
};

const EMOJI_MAP: Record<string, string> = {
  // LLM/AI
  'gemini request': '🔄',
  'gemini api': '☁️',
  'system prompt': '🤖',
  'llm generated': '🧠',
  'quota': '⏳',
  'rate limit': '⏳',
  
  // Auth/API
  'auth': '🛡️',
  'token': '🔑',
  'unauthorized': '🚫',
  'api success': '✅',
  'api error': '❌',
  
  // App
  'mount': '🚀',
  'render': '🎨',
  'event': '⚡',
};

class Logger {
  private component: string;

  constructor(component: string) {
    this.component = component.padEnd(12).substring(0, 12);
  }

  private getTime(): string {
    return new Date().toLocaleTimeString('en-GB', { hour12: false });
  }

  private getEmoji(message: string): string {
    const lowerMsg = message.toLowerCase();
    for (const [key, emoji] of Object.entries(EMOJI_MAP)) {
      if (lowerMsg.includes(key)) return emoji + ' ';
    }
    return '';
  }

  private format(level: LogLevel, message: string, ...args: any[]): void {
    const timestamp = this.getTime();
    const emoji = this.getEmoji(message);
    const paddedLevel = level.padEnd(8);
    
    const formatStr = `%c${timestamp} %c| %c${paddedLevel} %c| %c${this.component} %c| ${emoji}${message}`;
    
    const styles = [
      COLORS.TIMESTAMP,
      '', // separator
      COLORS[level],
      '', // separator
      COLORS.COMPONENT,
      '', // message text
    ];

    switch (level) {
      case 'DEBUG':
        console.debug(formatStr, ...styles, ...args);
        break;
      case 'INFO':
        console.info(formatStr, ...styles, ...args);
        break;
      case 'WARN':
        console.warn(formatStr, ...styles, ...args);
        break;
      case 'ERROR':
        // Avoid triggering the Next.js error overlay in development for predictable API/flow errors
        if (process.env.NODE_ENV === 'development') {
          console.warn(`[DEVELOPMENT ERROR SUPPRESSED] ${formatStr}`, ...styles, ...args);
        } else {
          console.error(formatStr, ...styles, ...args);
        }
        break;
    }
  }

  public debug(msg: string, ...args: any[]): void { this.format('DEBUG', msg, ...args); }
  public info(msg: string, ...args: any[]): void { this.format('INFO', msg, ...args); }
  public warn(msg: string, ...args: any[]): void { this.format('WARN', msg, ...args); }
  public error(msg: string, ...args: any[]): void { this.format('ERROR', msg, ...args); }
}

export const getLogger = (component: string) => new Logger(component);

export default getLogger;
