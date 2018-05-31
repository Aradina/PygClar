import math
import os
import json

import pyglet
from pyglet.window import key, mouse
import pyglet.gl as gl

# The shapes from the other included file.
import prefabs as pf

import config


# The model class is used to spawn things/render the main batch.
# Location is the location where you want it spawned
# Vector is the mouse vector gotten via get_sight_vector()
# Most of these are called via mouse presses.


class Model(object):
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.world = []
    # Many of these are self explanatory.

    def addCube(self, location, vector):
        pf.cube(location, gl.GL_QUADS, self.batch, vector)
    # Adds rectangles of different shapes based.
    # One goes forward and one to the side.

    def addRectanglex(self, location, vector):
        pf.rectanglex(location, gl.GL_QUADS, self.batch, vector, rotation=1)

    def addRectanglez(self, location, vector):
        pf.rectanglez(location, gl.GL_QUADS, self.batch, vector, rotation=1)
    # This will make the words "SEND NUDES" where ever you are standing.
    # This is a very important feature, of course.

    def addNudes(self, location):
        pf.nudes(location, gl.GL_QUADS, self.batch)
    # Adds a small "Hallway" made up of rectangles and cubes.
    # Mostly pointless
    # unless snapping were to be added for building game related reasons.

    def addHallway(self, location, vector):
        pf.hallway(location, gl.GL_QUADS, self.batch, vector)
    # This gets called by Pyglets on_draw function, which is further down.

    def draw(self):
        self.batch.draw()


class unGUI(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sets the minimum window size. By default the window is 1600x900.
        # and can be toggled between that and 1920x1080 with F1.
        # It can also just be resized as needed, but not below this.
        self.set_minimum_size(800, 600)

        # playerMove is used for player movement.
        self.playerMove = [0, 0]
        self.position = (0, 0, 0)
        self.rotation = (0, 0)

        # spaceLoc and spawnRot are used for testing purposes.
        # Pressing G by default will reset you to this position.
        self.spawnLoc = self.position
        self.spawnRot = self.rotation

        # This sets various variables, again.
        # Sets flying, exclusive mouse, etc to defaults.
        # Most are fairly self explanatory.
        self.dy = 0
        self.gravity = 20
        self.flying = False
        self.exclusive = False
        self.reticle = None

        # This displays the direction that you're facing on a label, or rather,
        # this sets it to blank.
        # The direction (Forward, Right, Down, Backward and Up, Middle and Down)
        # are set elsewhere based on camera movement.
        # The camera direction system is very far from perfect.
        # That needs improvement.
        # See on_mouse_motion for the rest of it.
        self.angley = ''
        self.direction = ''
        # This sets the default selection.
        # Selections are changed later in the on_key_press section.
        # Should have it set to cycle
        # (perhaps with a display of non-selected types) but that's far from important.
        self.selected = 'Cubes'

        # This checks if a config file exists, and if not, creates one.
        # I'll admit that I'm not sure this is a perfect way to do this.
        if (os.path.exists('config') is False or os.path.exists('config\config.txt') is False):
            # If the path /config/ in the main folder.
            # should default to the script folder, or exe if one were to be made
            # Or if the config.txt file doesn't exist.
            # userSettings sets the current (default)
            # values to add to the config file.
            # Then it sends it down to playerConfig
            # which is what actually makes the file.
            # Again, not sure this is the best way to do this.
            userSettings = {
                'width': self.width, 'height': self.height,
                'fullscreen': self.fullscreen, 'vsync': self.vsync}
            playerConfig().configFile(userSettings)
        # This checks for saves.
        # There is little to no reason for character saves yet, but here it is.
        if (os.path.exists('saves') is False or os.path.exists('saves\character.txt') is False):
            playerConfig().charDef()
        elif os.path.exists('saves\character.txt') is True:
            with open('saves\character.txt') as keybind:
                # The keybindings don't work.
                # Not really sure how to use them with Pyglets key system.
                keybind = keybind.read()
                keybind = json.loads(keybind)
        # set the model/batch rendering class from earlier to Model()
        self.model = Model()

        # This is the label in the top left.
        # FPS display, x, y, z, version info and controls, etc.
        # Text is set down in the draw_label function.
        self.label = pyglet.text.Label(
            '', font_name='Arial', font_size=18,
            x=10, y=self.height - 10, anchor_x='left',
            anchor_y='top', color=(0, 0, 0, 255),
            multiline=True, width=1000)
        # This just sets the interval for updating.
        pyglet.clock.schedule_interval(self.update, 1.0/240)

    def set_exclusive_mouse(self, exclusive):
        super(unGUI, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def get_sight_vector(self):
        # Gets where the mouse is pointing and returns it.
        x, y = self.rotation
        m = math.cos(math.radians(y))
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)

    def get_motion_vector(self):
        # This is the main movement function.
        # It checks the value of playerMove and applies movement.
        # The direction is based on what the value is,
        # the value ranges from -1 to 1.
        if any(self.playerMove):
            x, y = self.rotation
            playerMove = math.degrees(math.atan2(*self.playerMove))
            y_angle = math.radians(y)
            x_angle = math.radians(x + playerMove)
            # Flies if flying, doesn't if not.
            if self.flying:
                m = math.cos(y_angle)
                dy = math.sin(y_angle)
                if self.playerMove[1]:
                    # left/right movement.
                    dy = 0.0
                    m = 1
                elif self.playerMove[0] > 0:
                    # backward movement.
                    dy *= -1
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return (dx, dy, dz)

    def on_mouse_press(self, x, y, button, modifiers):
        # Mouse functions. Focuses the window if it isn't.
        if self.exclusive:
            # Gets the sight vector for later use with certain objects.
            vector = self.get_sight_vector()
            # If you click with the left mouse button
            # it checks to see what the selected value is.
            # That value is chosen via the number keys.
            # It defaults to cubes.
            if button == mouse.LEFT:
                # This makes a vaguely hallway shaped set of shapes.
                if self.selected == 'Hallway':
                    self.model.addHallway(self.position, vector)
                # This draws the words SEND NUDES.
                # Obviously a very important feature.
                elif self.selected == 'Nudes':
                    self.model.addNudes(self.position)
                # Makes a cube.
                elif self.selected == 'Cubes':
                    self.world = self.model.addCube(self.position, vector)
                # Rectanglex and rectanglez. Retangles of varying angles.
                elif self.selected == 'Rectanglex':
                    self.model.addRectanglex(self.position, vector)
                elif self.selected == 'Rectanglez':
                    self.model.addRectanglez(self.position, vector)
        else:
            self.set_exclusive_mouse(True)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.exclusive:
            # This gets the direction you're pointing for various functions.
            # It changes the self.direction value based on your direction.
            # The way it decides direction is very poor
            # and there are some "blind spots". Mostly works though.
            vector = self.get_sight_vector()
            if (vector[0] >= 0.50 and vector[2] >= -0.50):
                self.direction = 'Forward'
            elif (vector[2] > 0.50 and vector[0] < 0.50):
                self.direction = 'Right'
            elif (vector[2] < -0.50 and vector[0] < 0.50):
                self.direction = 'Left'
            elif (vector[2] <= 0.50 and vector[0] <= -0.50):
                self.direction = 'Backward'
            if vector[1] >= 0.25:
                self.angley = 'Up'
            elif vector[1] <= -0.25:
                self.angley = 'Down'
            elif (vector[1] >= -0.25 and vector[1] <= 0.25):
                self.angley = 'Middle'
            m = 0.15
            x, y = self.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.rotation = (x, y)

    def on_key_press(self, symbol, modifiers):
        # Closes the window.
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        # Toggles focus of the window.
        elif symbol == key.E:
            if self.exclusive:
                self.set_exclusive_mouse(False)
            else:
                self.set_exclusive_mouse(True)
        # WASD controls. Jumping. Other assorted controls.
        elif symbol == key.W:
            self.playerMove[0] -= 1
        elif symbol == key.S:
            self.playerMove[0] += 1
        elif symbol == key.A:
            self.playerMove[1] -= 1
        elif symbol == key.D:
            self.playerMove[1] += 1
        elif symbol == key.SPACE:
            self.dy = config.jump
        elif symbol == key.TAB:
            self.flying = not self.flying
        elif symbol == key.G:
            # Resets your position to 0, 0, 0.
            # Or whatever the default is (which is 0, 0, 0).
            self.position = self.spawnLoc
            self.rotation = self.spawnRot
        elif symbol == key.Q:
            # This stops any falling. Not very useful.
            # Was a planned feature early on when I was actually
            # focused on making a game.
            self.dy = 0
            self.gravity = 0
        # Toggles resolution/fullscreen.
        # Fullscreen may default to the wrong monitor if you have multiple.
        elif symbol == key.F1:
            currentsize = self.get_size()
            if currentsize[0] == 1920:
                playerConfig.res(self, 1600, 900)
            elif currentsize[0] == 1600:
                playerConfig.res(self, 1920, 1080)
        elif symbol == key.F2:
            if self.fullscreen is True:
                self.set_fullscreen(fullscreen=False)
            elif self.fullscreen is False:
                self.set_fullscreen(fullscreen=True)
        # This chooses the object to make when you click.
        elif symbol == key._1:
            self.selected = 'Cubes'
        elif symbol == key._2:
            self.selected = 'Hallway'
        elif symbol == key._3:
            self.selected = 'Nudes'
        elif symbol == key._4:
            self.selected = 'Rectanglex'
        elif symbol == key._5:
            self.selected = 'Rectanglez'

    def on_key_release(self, symbol, modfiers):
        # Resets values when you let go.
        if symbol == key.W:
            self.playerMove[0] += 1
        elif symbol == key.S:
            self.playerMove[0] -= 1
        elif symbol == key.A:
            self.playerMove[1] += 1
        elif symbol == key.D:
            self.playerMove[1] -= 1
        elif symbol == key.Q:
            self.gravity = 20

    def update(self, dt):
        m = 8
        dt = min(dt, 0.2)
        for _ in range(m):
            self._update(dt/m)

    def _update(self, dt):
        # This is the main update part. it updates and applies movement.
        # If you have flying on(toggled via tab) you move at a higher speed.
        if self.flying:
            speed = config.flyingSpeed
        else:
            speed = config.walkingSpeed

        d = dt * speed
        dx, dy, dz = self.get_motion_vector()
        dx, dy, dz = dx * d, dy * d, dz * d
        x, y, z = self.position

        # Checks if you're flying, if not, makes you fall.
        # The "floor" in this case is just a y value of 0.
        # There isn't actually a floor, or in fact, any collision.
        if self.flying is False:
            if y >= 0:
                self.dy -= dt * self.gravity
                self.dy = max(self.dy, -config.terminalVelocity)
                dy += self.dy * dt
            if y < 0:
                self.dy = max(self.dy, 0)
                dy += self.dy * dt

        # Moves the player around.
        self.position = list((x + dx, y + dy, z + dz))

    def on_resize(self, width, height):
        # The resize function.
        # Makes sure that things are moved to account for new window size.
        self.label.y = height - 10
        if self.reticle:
            self.reticle.delete()
        x, y = self.width // 2, self.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(
            4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n)))

    def set2d(self):
        width, height = self.get_size()
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, width, 0, height, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    def set3d(self):
        # 3D viewport settings.
        width, height = self.get_size()
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.gluPerspective(90, width / float(height), 0.1, 60)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        x, y = self.rotation
        gl.glRotatef(x, 0, 1, 0)
        gl.glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.position
        gl.glTranslatef(-x, -y, -z)

    def on_draw(self):
        # Clears anything.
        self.clear()
        # sets the 3d viewport.
        self.set3d()
        gl.glColor3d(1, 1, 1)
        # Draws the main batch.
        self.model.draw()

        # Then it draws the remaining things, the info label and reticle.
        self.set2d()
        self.draw_label()
        self.draw_reticle()

    def draw_reticle(self):
        gl.glColor3d(0, 0, 0)
        self.reticle.draw(gl.GL_LINES)

    def draw_label(self):
        x, y, z = self.position
        vector = self.get_sight_vector()
        dx, dy, dz = vector[0], vector[1], vector[2]
        # TODO: Split this into multiple labels.
        # Honestly, this is just gross.
        self.label.text = f'{int(round(pyglet.clock.get_fps()))} ({int(round(x))}, {int(round(y))}, {int(round(z))})({int(round(dx))}, {int(round(dy))}, {int(round(dz))})\nF1 changes resolution.\nF2 toggles fullscreen\n\n{self.selected}\n{self.direction} : {self.angley}'
        self.label.draw()


def setup_fog():
    # Enables fog.
    gl.glEnable(gl.GL_FOG)
    # Sets fog colour.
    gl.glFogfv(gl.GL_FOG_COLOR, (gl.GLfloat * 4)(0.5, 0.69, 1.0, 1))
    gl.glHint(gl.GL_FOG_HINT, gl.GL_DONT_CARE)
    gl.glFogi(gl.GL_FOG_MODE, gl.GL_LINEAR)
    # Fog distance.
    gl.glFogf(gl.GL_FOG_START, 20.0)
    gl.glFogf(gl.GL_FOG_END, 60.0)


def setup():
    # Sets the color of the sky.
    gl.glClearColor(0.5, 0.69, 1.0, 1)
    gl.glEnable(gl.GL_CULL_FACE)
    # Enables multisampling.
    gl.glEnable(gl.GL_MULTISAMPLE)
    setup_fog()


class playerConfig():
    def configFile(self, usersettings):
        # Makes config files if needed.
        filename = os.path.join('config', 'config.txt')
        if os.path.exists('config') is False:
            os.makedirs('config')
        if os.path.exists(filename) is False:
            open(filename, 'wt')
            with open(filename, 'r+') as userConfig:
                firstset = json.dumps(
                    {'display settings':
                        {'width': usersettings['width'],
                         'height': usersettings['height'],
                         'fullscreen': usersettings['fullscreen'],
                         'vsync': usersettings['vsync']}}, indent=1)
                userConfig.write(firstset)

    def charDef(self):
        # Makes a default characters file if there isn't one.
        filename = os.path.join('saves\character.txt')
        if os.path.exists('saves') is False:
            os.makedirs('saves')
        if os.path.exists(filename) is False:
            open(filename, 'wt')
            with open(filename, 'r+') as charData:
                # These defaults are largely just placeholders.
                # None will actually do anything.
                # Keybindings don't work, as mentioned earlier.
                defaultChar = json.dumps(
                    {'Character':
                        {'Name': 'None', 'Capacitor': '10',
                         'Funds': '0', 'Progress': '0',
                         'Service Time': '0'},
                        'Key Bindings':
                            {'Move Forward': 'W', 'Move Left': 'A',
                             'Move Backward': 'S', 'Move Right': 'D',
                             'Toggle Flight': 'TAB', 'Toggle Fullscreen': 'F2',
                             'Cancel Motion': 'Q', 'Save': 'J'}}, indent=1)
                charData.write(defaultChar)


class main():
    def __init__(self):
        # This will check to see if there's a config file
        # if there is it applies the settings.
        if os.path.exists('config\config.txt') is True:
            with open('config\config.txt') as userConfig:
                userConfig = userConfig.read()
                userConfig = json.loads(userConfig)
                userConfig = userConfig['display settings']
                width = userConfig['width']
                height = userConfig['height']
                fullscreen = userConfig['fullscreen']
                vsync = userConfig['vsync']

        elif os.path.exists('config\config.txt') is False:
            # These are the default values.
            width = 1600
            height = 900
            fullscreen = False
            vsync = True

        # Starts the main Pyglet window and event loop.
        unGUI(
            width=width, height=height,
            caption='Untitled: ', resizable=True,
            fullscreen=fullscreen, vsync=vsync)
        setup()
        pyglet.app.run()


# Generic Python thing that runs everything.
if __name__ == '__main__':
    main()
