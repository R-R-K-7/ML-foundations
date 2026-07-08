# ConnectFour
Instructions to run the python script

Run ```python ConnectFour.py arg1 arg``` where ```arg1``` and ```arg2``` are one of AI, random, or human.

* For ai v/s human run ```python ConnectFour.py ai human```

* For ai v/s ai run ```python ConnectFour.py ai ai```

* For ai v/s random player run ```python ConnectFour.py ai random```

Similarly different combinations of players can be made to run.

ConnectFour.py takes one optional argument --time which is an integer. It is the value used to limit
the amount of time in seconds to wait for the AI player to make a move. The default value is 5
seconds.

For example, to limit the time per move to 3 seconds, run
```python ConnectFour.py ai ai --time 3``` or ```python ConnectFour.py --time 3 ai ai```
