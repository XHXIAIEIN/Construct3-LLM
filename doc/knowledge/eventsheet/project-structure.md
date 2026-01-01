# Construct 3 Project Structure

## Directory Layout

```
project/
├── project.c3proj
├── eventSheets/*.json
├── layouts/*.json
├── objectTypes/*.json
├── images/
├── icons/
└── scripts/
```

## project.c3proj

```json
{
  "projectFormatVersion": 1,
  "name": "ProjectName",
  "runtime": "c3",
  "uniqueId": "abc123",
  "objectTypes": {"items": ["Player", "Enemy"], "subfolders": []},
  "layouts": {"items": ["Game"], "subfolders": []},
  "eventSheets": {"items": ["MainCode"], "subfolders": []},
  "viewportWidth": 320,
  "viewportHeight": 180
}
```

## objectTypes/*.json

```json
{
  "name": "Player",
  "plugin-id": "Sprite",
  "sid": 100000000000001,
  "isGlobal": false,
  "instanceVariables": [
    {"name": "health", "type": "number", "desc": "", "sid": 100000000000002}
  ],
  "behaviorTypes": [
    {"behaviorId": "Platform", "name": "Platform", "sid": 100000000000003}
  ],
  "effectTypes": [],
  "animations": {"items": [], "subfolders": []}
}
```

## layouts/*.json

```json
{
  "name": "Game",
  "layers": [
    {
      "name": "Main",
      "instances": [
        {
          "type": "Player",
          "uid": 0,
          "instanceVariables": {"health": 100},
          "behaviors": {},
          "world": {"x": 100, "y": 100, "width": 32, "height": 32, "angle": 0}
        }
      ]
    }
  ]
}
```

## Common Plugin IDs

- `Sprite` - Animated sprite
- `TiledBg` - Tiled background
- `Text` - Text object
- `Spritefont2` - Sprite font
- `Particles` - Particle emitter
- `Keyboard` - Keyboard input
- `Mouse` - Mouse input
- `Touch` - Touch input
- `Audio` - Audio playback

## Common Behavior IDs

- `Platform` - Platform movement
- `8Direction` - 8-directional movement
- `Bullet` - Bullet movement
- `Solid` - Solid obstacle
- `Timer` - Timer events
- `Tween` - Animation tweening
- `Pathfinding` - AI pathfinding
- `LineOfSight` - Line of sight detection
- `Fade` - Fade in/out
- `Flash` - Flash effect
