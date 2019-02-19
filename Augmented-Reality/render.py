import pyglet
import ratcave as rc

# Create the window
window = pyglet.window.Window()

def update(dt):
	pass
pyglet.clock.schedule(update)

# 3D Object file name
obj_filename = "cube.obj"
obj_reader = rc.WavefrontReader(obj_filename)

# Create the mesh
monkey = obj_reader.get_mesh("cube")
monkey.position.xyz = 0, 1, -2

# Create Scene

scene = rc.Scene(meshes=[monkey])

@window.event
def on_draw():
	with rc.default_shader:
		scene.draw()
		
pyglet.app.run()