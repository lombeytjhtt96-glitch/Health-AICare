"""
Structured logging configuration for production monitoring.

This module provides JSON-formatted logging for easy parsing by ELK stack.
"""
import io
import logging
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, Optional
import traceback


class UnicodeStreamHandler(logging.StreamHandler):
    """
    A StreamHandler that properly handles Unicode characters on Windows.
    
    Windows console (cp1252) can't display emojis, so this handler either:
    1. Uses UTF-8 encoding when the stream supports it
    2. Strips problematic characters when UTF-8 isn't available
    """
    
    def __init__(self, stream=None):
        # On Windows, wrap stdout with UTF-8 encoding if possible
        if stream is None:
            stream = sys.stdout
        
        # Try to reconfigure stdout for UTF-8 on Windows
        if sys.platform == "win32" and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, OSError):
                pass
        
        super().__init__(stream)
    
    def emit(self, record):
        """Emit a record, handling Unicode errors gracefully."""
        if sys is None or getattr(sys, "meta_path", None) is None:
            return
        try:
            msg = self.format(record)
            stream = self.stream
            if stream is None:
                return
            
            # Try to write with error handling
            try:
                stream.write(msg + self.terminator)
                self.flush()
            except (UnicodeEncodeError, OSError):
                # Fallback: replace unencodable characters
                safe_msg = msg.encode("ascii", errors="replace").decode("ascii")
                stream.write(safe_msg + self.terminator)
                self.flush()
                
        except RecursionError:
            raise
        except Exception:
            pass


class JSONFormatter(logging.Formatter):
    """
    Format logs as JSON for easy parsing by log aggregators (ELK, Loki, etc).
    
    Outputs structured JSON with timestamp, level, message, and context fields.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON string."""
        exc_info = record.exc_info
        if exc_info is True:
            exc_info = sys.exc_info()

        log_data: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "thread": record.thread,
            "thread_name": record.threadName,
        }
        
        # Add exception info if present
        if exc_info:
            log_data["exception"] = {
                "type": exc_info[0].__name__ if exc_info[0] else None,
                "message": str(exc_info[1]) if exc_info[1] else None,
                "traceback": self.formatException(exc_info)
            }
        
        # Add stack trace for errors (without full exception)
        if record.levelno >= logging.ERROR and not exc_info:
            log_data["stack_info"] = self.formatStack(record.stack_info) if record.stack_info else None
        
        # Add custom context fields (optional, but keep for compatibility)
        for attr in ['user_id', 'user_role', 'session_id', 'prompt_id', 'agent']:
            if hasattr(record, attr):
                log_data[attr] = getattr(record, attr)
                
        return json.dumps(log_data, default=str)


class ProfessionalFormatter(logging.Formatter):
    """
    Highly readable, professional formatter for console output.
    Format: HH:MM:SS | LEVEL    | COMPONENT    | EMOJI MESSAGE
    """
    
    # ANSI Color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[41m',  # White on Red
        'RESET': '\033[0m'
    }
    
    # Semantic emoji mapping for message prefixes
    EMOJI_MAP = {
        # LLM/AI
        "gemini request": "🔄",
        "gemini api": "☁️",
        "system prompt": "🤖",
        "llm generated": "🧠",
        "gemini plan": "📋",
        "llm call": "📞",
        "quota": "⏳",
        "throttle": "⏳",
        "rate limit": "⏳",
        "safety review passed": "✅",
        "safety review blocked": "⚠️",
        "intervention blocked": "⚠️",
        "successful": "✅",
        "success": "✅",
        
        # Database/Model
        "database": "🗄️",
        "db ": "🗄️",
        "sqlalchemy": "🔗",
        "afc": "📡",
        
        # Auth
        "token": "🔑",
        "jwt": "🔒",
        "decode": "🔓",
        "auth": "🛡️",
        
        # Flow/Graph
        "graph": "🕸️",
        "tca": "🧘",
        "sta": "🛡️",
        "sda": "🏥",
        "ia ": "📊",
        "cma": "🧠",
        "node": "📍",
        "trigger": "⚡",
        
        # Errors
        "failed to parse": "❌",
        "error": "❌",
        "failed": "❌",
        "exception": "🚨",
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors, padding, and emojis."""
        exc_info = record.exc_info
        if exc_info is True:
            exc_info = sys.exc_info()

        try:
            timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S')
        except Exception:
            timestamp = "00:00:00"
        level = record.levelname
        color = self.COLORS.get(level, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Padded level
        padded_level = f"{level:<8}"
        
        # Padded logger name (component)
        logger_name = record.name.split('.')[-1]
        padded_component = f"{logger_name:<12}"
        
        message = record.getMessage()
        
        # Auto-apply emojis if not already present
        emoji_prefix = ""
        msg_lower = message.lower()
        
        for keyword, emoji in self.EMOJI_MAP.items():
            if keyword in msg_lower:
                emoji_prefix = emoji + " "
                break
        
        if any(message.startswith(e) for e in self.EMOJI_MAP.values()):
            emoji_prefix = ""

        formatted_msg = f"{timestamp} | {color}{padded_level}{reset} | {padded_component} | {emoji_prefix}{message}"
        
        if exc_info:
            if not record.exc_text:
                if exc_info[0] is not None:
                    record.exc_text = self.formatException(exc_info)
                else:
                    record.exc_text = "".join(traceback.format_stack()[:-1])
            if record.exc_text:
                if formatted_msg[-1:] != "\n":
                    formatted_msg = formatted_msg + "\n"
                formatted_msg = formatted_msg + record.exc_text
                
        return formatted_msg


def configure_logging(
    log_level: str = "INFO",
    format_type: str = "professional",
    log_to_file: bool = False,
    log_file_path: str = "logs/app.log"
) -> None:
    """
    Configure structured logging for production.
    """
    if format_type == "json":
        formatter = JSONFormatter()
    elif format_type == "professional":
        formatter = ProfessionalFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler = UnicodeStreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    handlers = [console_handler]
    
    if log_to_file:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    for handler in handlers:
        root_logger.addHandler(handler)
    
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    root_logger.info(
        f"Logging configured: level={log_level}, format={format_type}, log_to_file={log_to_file}"
    )


class ContextLogger:
    """
    Logger wrapper that adds context to log messages.
    """
    def __init__(self, name: str, **context):
        self.logger = logging.getLogger(name)
        self.context = context
    
    def _add_context(self, record: logging.LogRecord) -> None:
        for key, value in self.context.items():
            setattr(record, key, value)
    
    def _log(self, level: int, msg: str, **extra):
        exc_info = extra.pop("exc_info", None)
        if exc_info is True:
            exc_info = sys.exc_info()

        record = self.logger.makeRecord(
            self.logger.name, level, "(unknown file)", 0, msg, (), exc_info
        )
        self._add_context(record)
        for key, value in extra.items():
            setattr(record, key, value)
        self.logger.handle(record)
    
    def debug(self, msg: str, **extra): self._log(logging.DEBUG, msg, **extra)
    def info(self, msg: str, **extra): self._log(logging.INFO, msg, **extra)
    def warning(self, msg: str, **extra): self._log(logging.WARNING, msg, **extra)
    def error(self, msg: str, **extra): self._log(logging.ERROR, msg, **extra)
    def critical(self, msg: str, **extra): self._log(logging.CRITICAL, msg, **extra)
    
    def with_context(self, **additional_context) -> "ContextLogger":
        merged_context = {**self.context, **additional_context}
        return ContextLogger(self.logger.name, **merged_context)


def get_logger(name: str, **context) -> ContextLogger:
    return ContextLogger(name, **context)
