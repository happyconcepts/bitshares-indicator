---------------------------------------------------------------------
Release 0.8 20180614
---------------------------------------------------------------------
Features
--------
 - Support for Python 3
 - Tests for each of the API sources

 Fixes
 --------
 - Python 2/3 type checking
 - Improved Menu UX

 Future...
 --------
 - Is RuDEX link now valid
 - More tests
 - Issue by issue

---------------------------------------------------------------------
Release 0.7 20180510
---------------------------------------------------------------------
Features
--------
 - User settings are now saved

 Fixes
 --------
 - #9 Type check some json input
 - #12 Menu UX
 - Icon tweak

 Future...
 --------
 - more bases
 - more tests

---------------------------------------------------------------------
Release 0.6 20180424
---------------------------------------------------------------------
Features
--------
- Added unit test for gate.io
- .gitignore .pyc files

Fixes
--------
- #7 Change filename to bitshares_indicator.py (unittest)
- #8 Fix price update

Future...
--------
- data persistence

---------------------------------------------------------------------
Release 0.5 20180407
---------------------------------------------------------------------
Features
--------
- Multiple update intervals - added 30 min, 4 hour
- Single settings window UI

Fixes
--------
- UI tweaks

Future...
--------
- data persistence

---------------------------------------------------------------------
Release 0.4 20180405
---------------------------------------------------------------------
Features
--------
- improved eur base price
- UTF-8

Fixes
--------
- Reload prices
- Focus settings window

Future...
--------
- user select update interval
- data persistence

---------------------------------------------------------------------
Release 0.3 20180404
---------------------------------------------------------------------
Features
--------
- Set base currency: USD, EUR
- Added Makefile

Fixes
--------
- added Unicode Euro symbol
- error-handling

Future...
--------
- user select update interval
- data persistence
- Euro pricing source

---------------------------------------------------------------------
Release 0.2 20180403
---------------------------------------------------------------------
Features
--------
- price history held
- set update interval

Fixes
--------
- signal response [Ctrl-C]
- Gtk parent window
- more error handling

Future...
--------
- set base for pairs

---------------------------------------------------------------------
Release 0.1 20180401
---------------------------------------------------------------------
Features
--------
- obtains BTS price from Gate.io
- obtains BTC price from binance.com
- handles json response errors
