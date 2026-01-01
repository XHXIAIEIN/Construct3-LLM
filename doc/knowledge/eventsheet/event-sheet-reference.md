# Construct 3 Event Sheet JSON Reference

## Event Sheet Root

```json
{
  "name": "EventSheetName",
  "events": [],
  "sid": 100000000000000
}
```

## Event Types

### variable

```json
{
  "eventType": "variable",
  "name": "Score",
  "type": "number",
  "initialValue": "0",
  "comment": "",
  "isStatic": false,
  "isConstant": false,
  "sid": 100000000000001
}
```

type: `"number"` | `"string"` | `"boolean"`

### comment

```json
{
  "eventType": "comment",
  "text": "Comment text here"
}
```

### group

```json
{
  "eventType": "group",
  "disabled": false,
  "title": "Group Title",
  "description": "",
  "isActiveOnStart": true,
  "children": [],
  "sid": 100000000000002
}
```

### block

```json
{
  "eventType": "block",
  "conditions": [],
  "actions": [],
  "sid": 100000000000003
}
```

Optional fields:
- `"children": []` - nested sub-events
- `"isOrBlock": true` - OR conditions instead of AND

### function-block

```json
{
  "eventType": "function-block",
  "functionName": "MyFunction",
  "functionDescription": "",
  "functionCategory": "",
  "functionReturnType": "none",
  "functionIsAsync": false,
  "functionParameters": [],
  "conditions": [],
  "actions": [],
  "sid": 100000000000004,
  "children": []
}
```

functionReturnType: `"none"` | `"number"` | `"string"` | `"any"`

Function parameter:
```json
{
  "name": "Param1",
  "type": "number",
  "initialValue": "0",
  "comment": "",
  "sid": 100000000000005
}
```

---

## Conditions

### System Conditions

```json
{"id": "on-start-of-layout", "objectClass": "System", "sid": 1}
```

```json
{"id": "every-tick", "objectClass": "System", "sid": 2}
```

```json
{"id": "every-x-seconds", "objectClass": "System", "sid": 3,
 "parameters": {"interval-seconds": "2"}}
```

```json
{"id": "compare-two-values", "objectClass": "System", "sid": 4,
 "parameters": {"first-value": "Score", "comparison": 4, "second-value": "100"}}
```

```json
{"id": "repeat", "objectClass": "System", "sid": 5,
 "parameters": {"count": "10"}}
```

```json
{"id": "for-each", "objectClass": "System", "sid": 6,
 "parameters": {"object": "Enemy"}}
```

```json
{"id": "else", "objectClass": "System", "sid": 7}
```

```json
{"id": "trigger-once-while-true", "objectClass": "System", "sid": 8}
```

### Comparison Operators

| Value | Operator |
|-------|----------|
| 0 | = |
| 1 | != |
| 2 | < |
| 3 | <= |
| 4 | > |
| 5 | >= |

### Object Conditions

```json
{"id": "on-collision-with-another-object", "objectClass": "Bullet", "sid": 10,
 "parameters": {"object": "Enemy"}}
```

```json
{"id": "compare-instance-variable", "objectClass": "Enemy", "sid": 11,
 "parameters": {"instance-variable": "health", "comparison": 3, "value": "0"}}
```

```json
{"id": "is-overlapping-another-object", "objectClass": "Player", "sid": 12,
 "parameters": {"object": "Coin"}}
```

### Input Conditions

```json
{"id": "key-is-down", "objectClass": "Keyboard", "sid": 20,
 "parameters": {"key": 32}}
```

Key codes: Space=32, Left=37, Up=38, Right=39, Down=40, A-Z=65-90

### Behavior Conditions

```json
{"id": "on-timer", "objectClass": "Player", "sid": 30,
 "behaviorType": "Timer",
 "parameters": {"tag": "\"Cooldown\""}}
```

### Inverted Condition

```json
{"id": "key-is-down", "objectClass": "Keyboard", "sid": 40,
 "parameters": {"key": 32},
 "isInverted": true}
```

---

## Actions

### System Actions

```json
{"id": "create-object", "objectClass": "System", "sid": 100,
 "parameters": {"object-to-create": "Bullet", "layer": "\"Game\"", "x": "100", "y": "200"}}
```

```json
{"id": "set-eventvar-value", "objectClass": "System", "sid": 101,
 "parameters": {"variable": "Score", "value": "Score + 10"}}
```

```json
{"id": "wait", "objectClass": "System", "sid": 102,
 "parameters": {"seconds": "1"}}
```

```json
{"id": "go-to-layout", "objectClass": "System", "sid": 103,
 "parameters": {"layout": "\"GameOver\""}}
```

```json
{"id": "restart-layout", "objectClass": "System", "sid": 104}
```

### Object Actions

```json
{"id": "destroy", "objectClass": "Enemy", "sid": 200}
```

```json
{"id": "set-position", "objectClass": "Player", "sid": 201,
 "parameters": {"x": "100", "y": "200"}}
```

```json
{"id": "set-angle", "objectClass": "Bullet", "sid": 202,
 "parameters": {"angle": "Player.Angle"}}
```

```json
{"id": "spawn-another-object", "objectClass": "Player", "sid": 203,
 "parameters": {"object": "Bullet", "layer": "\"Game\"", "image-point": "0"}}
```

```json
{"id": "set-instvar-value", "objectClass": "Enemy", "sid": 204,
 "parameters": {"instance-variable": "health", "value": "100"}}
```

```json
{"id": "set-opacity", "objectClass": "Ghost", "sid": 205,
 "parameters": {"opacity": "50"}}
```

```json
{"id": "set-animation", "objectClass": "Player", "sid": 206,
 "parameters": {"animation": "\"Running\"", "from": "beginning"}}
```

### Behavior Actions

```json
{"id": "set-speed", "objectClass": "Bullet", "sid": 300,
 "behaviorType": "Bullet",
 "parameters": {"speed": "500"}}
```

```json
{"id": "start-timer", "objectClass": "Player", "sid": 301,
 "behaviorType": "Timer",
 "parameters": {"duration": "0.5", "type": "once", "tag": "\"Cooldown\""}}
```

### Function Call

```json
{"callFunction": "SpawnEnemy", "sid": 400}
```

With parameters:
```json
{"callFunction": "SpawnAt", "sid": 401, "parameters": ["100", "200"]}
```

### Inline Comment

```json
{"type": "comment", "text": "Inline comment between actions"}
```

---

## Rules

1. **SID**: Unique 15-digit number for each element
2. **String values**: Use escaped quotes `"\"Game\""`
3. **Numeric values**: Always strings `"100"` not `100`
4. **Object names**: Must match project objectTypes exactly
5. **Behavior names**: Must match behaviorType in objectType definition
