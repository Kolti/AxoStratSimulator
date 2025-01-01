from dataclasses import dataclass
from varname import nameof
import numpy as np
import datetime as dt
    
@dataclass(unsafe_hash=True)
class StrategyResult():
    PeriodIndex: np.array
    DateGrid: np.array
    VOBBuy: np.array
    VOBSell: np.array
    CumFees: np.array
    BuyAmount: np.array
    SellAmount: np.array
    Price: np.array
    HoldingABop: np.array
    HoldingBBop: np.array
    TotalHoldingsInABop: np.array
    
    def __init__(self, count: int):
        self.PeriodIndex = np.zeros(count, dtype=int)
        self.DateGrid = np.empty(count, dtype=dt.datetime)
        self.VOBBuy = np.zeros(count, dtype=float)
        self.VOBSell = np.zeros(count, dtype=float)
        self.CumFees = np.zeros(count, dtype=float)
        self.BuyAmount = np.zeros(count, dtype=float)
        self.SellAmount = np.zeros(count, dtype=float)
        self.Price = np.zeros(count, dtype=float)
        self.HoldingABop = np.zeros(count, dtype=float)
        self.HoldingBBop = np.zeros(count, dtype=float)
        self.TotalHoldingsInABop = np.zeros(count, dtype=float)

            
    def to_dict(self):
        return {
            nameof(self.DateGrid): self.DateGrid,
            nameof(self.VOBBuy): self.DateGrid,
            nameof(self.VOBSell): self.DateGrid,
            nameof(self.CumFees): self.CumFees,
            nameof(self.BuyAmount): self.DateGrid,
            nameof(self.SellAmount): self.DateGrid,
            nameof(self.Price): self.DateGrid,
            nameof(self.HoldingABop): self.DateGrid,
            nameof(self.HoldingBBop): self.DateGrid,
            nameof(self.TotalHoldingsInABop): self.TotalHoldingsInABop
        }
    