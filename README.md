# AxoStratSimulator
Allows backtesting Axo strategies based on TapTools api price data. Strategy can be simulated over historical time intervals for a set of strategy parameters (e.g. spread, MA length, tranche size etc) to see which parameter choice would have performed best on average over the tested time intervals. Sample implementation is contained for AxoMAMMv1 algorithm https://app.axo.trade/composer/44068768-1b40-42b1-9fa8-86f04c591f24

To try it:

Enter TapToolsAPI key in Implementations/TapToolsConnector.py
Makre sure folder path at the top of files ATradingStrategy.py, AxoMAMMv1Strategy.py and Simulatation.py is correct
Run Simulation.py to generate result output as .csv
Other strategies can be implemented as implementations of abstract base class ATradingStrategy analogously.
