# Construct 3 Scripting API

## Entry Point

```javascript
runOnStartup(async runtime => {
    runtime.addEventListener("beforeprojectstart", () => init(runtime));
});
```

## IRuntime

```javascript
// Objects
runtime.objects.Player.getFirstInstance()
runtime.objects.Enemy.getAllInstances()
runtime.objects.Bullet.createInstance("LayerName", x, y)

// Global variables
runtime.globalVars.Score

// Layout
runtime.layout.name
runtime.goToLayout("LayoutName")

// Timing
runtime.dt          // delta time
runtime.gameTime    // time since start
runtime.timeScale   // speed multiplier

// Instance by UID
runtime.getInstanceByUid(uid)

// Call event sheet function
runtime.callFunction("FunctionName", param1, param2)
```

## IInstance

```javascript
inst.uid
inst.destroy()
inst.instVars.health    // instance variable
inst.behaviors.Bullet   // behavior access
```

## IWorldInstance

```javascript
// Position
inst.x, inst.y
inst.setPosition(x, y)

// Size
inst.width, inst.height
inst.setSize(w, h)

// Rotation
inst.angle          // radians
inst.angleDegrees   // degrees

// Appearance
inst.isVisible
inst.opacity        // 0-100

// Layer
inst.layer
inst.moveToTop()
inst.moveToBottom()

// Collision
inst.testOverlap(otherInst)
inst.containsPoint(x, y)

// Hierarchy
inst.getParent()
inst.addChild(child, opts)
```

## Events

```javascript
runtime.addEventListener("tick", () => {})
runtime.addEventListener("keydown", e => {})
runtime.addEventListener("pointerdown", e => {})
inst.addEventListener("destroy", e => {})
```

## Behavior Access

```javascript
inst.behaviors.Platform.maxSpeed = 300
inst.behaviors.Bullet.speed = 500
inst.behaviors.Bullet.angleOfMotion = 45
```
