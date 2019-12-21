
### Event types
```
(0, 'NoEvent')
(1, 'ActiveEvent')
(2, 'KeyDown')
(3, 'KeyUp')
(4, 'MouseMotion')
(5, 'MouseButtonDown')
(6, 'MouseButtonUp')
(7, 'JoyAxisMotion')
(8, 'JoyBallMotion')
(9, 'JoyHatMotion')
(10, 'JoyButtonDown')
(11, 'JoyButtonUp')
(12, 'Quit')
(13, 'SysWMEvent')
(16, 'VideoResize')
(17, 'VideoExpose')

Connect event only on sdl2
('Unknown', <Event(1541-Unknown {})>)
('Unknown', <Event(1541-Unknown {})>)

Disconnect event only on sdl2
('Unknown', <Event(1542-Unknown {})>)
('Unknown', <Event(1542-Unknown {})>)
```

### Key events

```
LEFT
('KeyDown', <Event(2-KeyDown {'unicode': '', 'key': 276, 'mod': 4096, 'scancode': 113, 'window': None})>)
('KeyUp', <Event(3-KeyUp {'key': 276, 'mod': 4096, 'scancode': 113, 'window': None})>)

UP
('KeyUp', <Event(3-KeyUp {'key': 273, 'mod': 4096, 'scancode': 111, 'window': None})>)
('KeyDown', <Event(2-KeyDown {'unicode': '', 'key': 273, 'mod': 4096, 'scancode': 111, 'window': None})>)

RIGHT
('KeyUp', <Event(3-KeyUp {'key': 275, 'mod': 4096, 'scancode': 114, 'window': None})>)
('KeyDown', <Event(2-KeyDown {'unicode': '', 'key': 275, 'mod': 4096, 'scancode': 114, 'window': None})>)

DOWN
('KeyUp', <Event(3-KeyUp {'key': 274, 'mod': 4096, 'scancode': 116, 'window': None})>)
('KeyDown', <Event(2-KeyDown {'unicode': '', 'key': 274, 'mod': 4096, 'scancode': 116, 'window': None})>)

A - ok
('KeyUp', <Event(3-KeyUp {'key': 97, 'mod': 4096, 'scancode': 38, 'window': None})>)
('KeyDown', <Event(2-KeyDown {'unicode': 'a', 'key': 97, 'mod': 4096, 'scancode': 38, 'window': None})>)

S - cancel
('KeyUp', <Event(3-KeyUp {'key': 115, 'mod': 4096, 'scancode': 39, 'window': None})>)
('KeyDown', <Event(2-KeyDown {'unicode': 's', 'key': 115, 'mod': 4096, 'scancode': 39, 'window': None})>)

z - start
('KeyUp', <Event(3-KeyUp {'key': 122, 'mod': 4096, 'scancode': 52, 'window': None})>)
('KeyDown', <Event(2-KeyDown {'unicode': 'z', 'key': 122, 'mod': 4096, 'scancode': 52, 'window': None})>)

x - select
('KeyUp', <Event(3-KeyUp {'key': 120, 'mod': 4096, 'scancode': 53, 'window': None})>)
('KeyDown', <Event(2-KeyDown {'unicode': 'x', 'key': 120, 'mod': 4096, 'scancode': 53, 'window': None})>)
```

### Joystick events

```
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyButtonDown', 10, <Event(10-JoyButtonDown {'button': 4, 'joy': 0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyButtonDown', 10, <Event(10-JoyButtonDown {'button': 5, 'joy': 0})>)
('JoyButtonUp', 11, <Event(11-JoyButtonUp {'button': 4, 'joy': 0})>)
('JoyButtonUp', 11, <Event(11-JoyButtonUp {'button': 5, 'joy': 0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 0, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 0, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 0, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 0, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 0, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 0, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 1, 'value': 0.0})>)
('JoyAxisMotion', 7, <Event(7-JoyAxisMotion {'joy': 0, 'axis': 0, 'value': -0.05157628101443525})>)
```
