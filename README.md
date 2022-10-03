# DEMO-TykeePy
Public version of TykeePy.

This is a work in progress repository.

Implemented:
- [x] Bases of Market models
- [x] Connection to MetaTrader5 and PostgreSQL

Coming soon:
- [ ] Basic machine learning models
  - [x] Logistic regression
  - [ ] Neural networks
  - [ ] Decision trees
- [ ] Models visualization and analysis
- [ ] Optuna hyperparameter optimization
- [ ] Reinforcement learning model [<sub><sup>(Ugly legacy code)</sup></sub>](https://github.com/refi-refi/ForexBotRL)

Possible future implementations:
- [ ] Backtesting
- [ ] Live trading


## Installation
Either use pip to install the package:
```bash
pip install .
```
or install in editable mode:
```bash
pip install -e .
```

or install using setup.py:
```bash
python setup.py install
```

### Database

To successfully use this repisitory, you need to have a PostgreSQL database running. You can either use a local database or a remote one.

To create a local database, refer to the [Demo-TykeeAPI](https://github.com/refi-refi/DEMO-TykeeAPI/tree/main/postgres).

Once you have a database running, update it with MetaTrader5 data using scripts in [update_candles.py](https://github.com/refi-refi/DEMO-TykeePy/blob/main/tykee/data/scripts/update_candles.py).


### Environment variables

To successfully run the package, you need to create a `.env` file in the root directory of the project.
There is a `.env.example` file in the root directory of the project, which you can use as a template.


## Disclaimer
**The information in this repository is for general information only.**

It should not be taken as constituting professional advice from the repository owner - Artūrs Smiltnieks.

Artūrs Smiltnieks is not a financial adviser. You should consider seeking independent legal, financial,
taxation or other advice to check how the repository's information relates to your unique circumstances.

Artūrs Smiltnieks is not liable for any loss caused, whether due to negligence or otherwise arising from
the use of, or reliance on, the information provided directly or indirectly, by use of this repository.