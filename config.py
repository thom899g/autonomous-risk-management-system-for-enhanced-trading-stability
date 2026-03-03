"""
Configuration module for Autonomous Risk Management System (ARMS)
Centralized configuration with environment variables and defaults
"""
import os
from dataclasses import dataclass
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration"""
    service_account_path: str = os.getenv("FIREBASE_SERVICE_ACCOUNT", "./firebase-key.json")
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "autonomous-risk-system")
    database_url: str = os.getenv("FIREBASE_DATABASE_URL", "")

@dataclass
class TradingConfig:
    """Trading platform configuration"""
    exchange_id: str = os.getenv("EXCHANGE_ID", "binance")
    api_key: str = os.getenv("EXCHANGE_API_KEY", "")
    api_secret: str = os.getenv("EXCHANGE_API_SECRET", "")
    test_mode: bool = os.getenv("TEST_MODE", "True").lower() == "true"

@dataclass
class RiskConfig:
    """Risk management configuration"""
    max_drawdown_limit: float = float(os.getenv("MAX_DRAWDOWN_LIMIT", "0.2"))
    position_size_limit: float = float(os.getenv("POSITION_SIZE_LIMIT", "0.1"))
    volatility_threshold: float = float(os.getenv("VOLATILITY_THRESHOLD", "0.05"))
    risk_free_rate: float = float(os.getenv("RISK_FREE_RATE", "0.02"))

@dataclass
class DataConfig:
    """Data collection configuration"""
    data_sources: List[str] = os.getenv("DATA_SOURCES", "binance,alphavantage,fred").split(",")
    update_interval: int = int(os.getenv("UPDATE_INTERVAL", "60"))
    historical_days: int = int(os.getenv("HISTORICAL_DAYS", "365"))

@dataclass
class ModelConfig:
    """Neural network configuration"""
    model_path: str = os.getenv("MODEL_PATH", "./models/risk_predictor.h5")
    sequence_length: int = int(os.getenv("SEQUENCE_LENGTH", "60"))
    train_interval: int = int(os.getenv("TRAIN_INTERVAL", "86400"))
    hidden_layers: List[int] = [64, 32, 16]

class Config:
    """Main configuration singleton"""
    def __init__(self):
        self.firebase = FirebaseConfig()
        self.trading = TradingConfig()
        self.risk = RiskConfig()
        self.data = DataConfig()
        self.model = ModelConfig()
        
        # Validate critical configurations
        self._validate_config()
    
    def _validate_config(self):
        """Validate critical configuration values"""
        if not os.path.exists(self.firebase.service_account_path):
            raise FileNotFoundError(
                f"Firebase service account file not found: {self.firebase.service_account_path}"
            )
        
        if not self.trading.api_key and not self.trading.test_mode:
            raise ValueError("API key required when not in test mode")
        
        if self.risk.max_drawdown_limit <= 0 or self.risk.max_drawdown_limit > 1:
            raise ValueError("max_drawdown_limit must be between 0 and 1")

config = Config()