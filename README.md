# Led Games

The code base to play games in your led strips.

With [gaming in your Christmas tree as an example](https://twitter.com/JordyMoos/status/1206568610275241984)

## Installation

Check out the repository
```
git clone git@github.com:JordyMoos/led-games.git
```

### Configure the led controller

The leds are controller by a [Teensy](https://www.pjrc.com/store/teensy32_pins.html) and the code is located here:
```
./src/led-controller/teensy.ino
```

You should change these values to match your led setup.
```
const int ledsPerStrip = 100;
const int strips = 8;
```

And after that you should upload that file to your Teensy.


[See the official teensy documentation how that is done.](https://www.pjrc.com/teensy/td_download.html)


### Run the game engine

Go to the game engine directory
```
cd src/game-engine
```

Install the python dependencies
```
python3 -m pip install -r requirements.txt
```

Run the game engine:
```
python3 ./main.py run snake
```

**Tip**:
Use the virtual renderer if you do not have the leds
```
python3 ./main.py run snake --renderer PYGAME
```

Use the `list` command to view the games
```
python3 ./main.py list
```

Run the command with the `-h` flag to see the options
```
python3 ./main.py run -h
```

**Optionally**:
You can change the default settings in `defaults.py`


## Game Controls

The game engine has these buttons defined

In code | Description
--- | --- 
Buttons.up | Used for movement / navigation
Buttons.right | Used for movement / navigation 
Buttons.down | Used for movement / navigation
Buttons.left | Used for movement / navigation
Buttons.ok | The default "submit" button. Used in TicTacToe to select a field
Buttons.cancel | Not used yet
Buttons.start | Not used yet - it is meant to get into the game menu
Buttons.select | Not used yet

#### Player One Keyboard
 
In code | Key on keyboard
--- | --- 
Buttons.up | `w`
Buttons.right | `d` 
Buttons.down | `s`
Buttons.left | `a`
Buttons.ok | `q`
Buttons.cancel | `e`
Buttons.start | `z`
Buttons.select | `x`

#### Player Two Keyboard
 
In code | Key on keyboard
--- | --- 
Buttons.up | `i`
Buttons.right | `l` 
Buttons.down | `k`
Buttons.left | `j`
Buttons.ok | `u`
Buttons.cancel | `o`
Buttons.start | `m`
Buttons.select | `,` (Comma)

#### DualShock 4

In code | On controller
--- | --- 
Buttons.up | Left stick up
Buttons.right | Left stick right 
Buttons.down | Left stick down
Buttons.left | Left stick left
Buttons.ok | `X`
Buttons.cancel | `O`
Buttons.start | `Options`
Buttons.select | `Share`
