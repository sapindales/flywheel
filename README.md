# flywheel

flywheel is a personal investment recommendation tool, until we make it a sophisticated trading bot. :)

## Components

```text
flywheel
├── __init__.py
├── __main__.py
├── app.py # where the main app runs
├── backtesting
│   ├── __init__.py
│   └── backtesting.py
├── flags.py
├── market # where we get market data
│   ├── __init__.py
│   ├── factor.py
│   ├── market.py
│   ├── stock_data.json
│   └── stock_list
├── service
│   └── google.py
├── signals # where we derive signals from market data
│   ├── README.txt
│   └── TODO
└── strategy # where we decide investment strategy
    ├── __init__.py
    ├── account.py
    └── strategy.py
```

## Build & Run

pipenv install

pipenv shell

python -m flywheel

(Send email): python flywheel --email

## TESTS

python -m flywheel.tests.test_{test_name}
