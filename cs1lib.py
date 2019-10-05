from math import pi
import sys, os.path
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtWidgets import QApplication, QWidget


# library version number
__version__ = "3.0.7pyqt"

print("Imported cs1lib, version " + __version__)

# hint to window manager where to place graphics window
WINDOW_X = 300
WINDOW_Y = 300

# Global canvas object
canvas = None

# main app is global to allow things like timers to be started before/without graphics loop
app = QApplication(sys.argv)

# used for noop callbacks
def noop(*args, **kwargs):
    pass

# Generic State class used to create objects to pass between callbacks in cs1 examples
#   (Monkey-patched to add variables in early examples.)

class State():
    def __init__(self):
        pass

class CS1Image(QImage):
    def get_pixel(self, x, y):
        p = self.pixel(x, y)

        r = qRed(p) / 255.0
        g = qGreen(p) / 255.0
        b = qBlue(p) / 255.0
        a = qAlpha(p) / 255.0

        return (r, g, b, a)

    def set_pixel(self, x, y, r, g, b, a = 1.0):
        ri  = int(r * 255)
        gi  = int(g * 255)
        bi  = int(b * 255)
        ai  = int(a * 255)

        qrgba = qRgba ( ri, gi, bi, ai )
        self.setPixel(x, y, qrgba)

class CS1Canvas(QWidget):

    def __init__(self, draw_fn, data, window_x, window_y, width, height, title, framerate,
                 mouse_press, mouse_release, mouse_move,
                 key_press, key_release):
        super(CS1Canvas, self).__init__()

        # store callback function
        self.draw_fn = draw_fn
        self.mouse_press = mouse_press
        self.mouse_release = mouse_release
        self.mouse_move = mouse_move
        self.key_press = key_press
        self.key_release = key_release

        # data to pass to callback functions
        self.data = data

        self.window_x = window_x
        self.window_y = window_y

        self.width = width
        self.height = height
        self.title = title
        self.framerate = framerate

        # basic state setup

        self.fill_enabled = True
        self.stroke_enabled = True

        self.stroke_width = 1

        self.clear_color = (1, 1, 1, 1)
        self.pen_color = (0, 0, 0, 1)
        self.fill_color = (0, 0, 0, 1)

        # Initial font

        self.font_name = "Arial"
        self.font_size = 14
        self.font_style = QFont.Normal
        self.font_italic = False

        # initialize image just so that there is one for first redraw
        self.image = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)
        self.init_qt()

        # get the size right this time
        self.image = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)

        self.ipainter = QPainter(self.image)
        self.ipainter.setRenderHint(QPainter.Antialiasing, True)
        self.ipainter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        self.closed = False

        # store the set of currently pressed keys
        self.keys_down = set()

        self.mouse_down = False
        self.mx = -1
        self.my = -1

        #self.clear()
        self.timer = QTimer()
        self.timer.timeout.connect(self.draw)
        self.timer.start(1000 / self.framerate)



    def init_qt(self):

        # self.setGeometry(self.window_x, self.window_y, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle(self.title)

        self.show()

        # enable tracking mouse during mouse move
        self.setMouseTracking(True)

        #self.enable_smoothing()

        self.raise_()

    def paintEvent(self, event):

        screen_painter = QPainter(self)

        screen_painter.drawImage(0, 0, self.image)

        screen_painter.end()


    def closeEvent(self, event):
        # qt unhappy if a reference to ipainter is still hanging
        #   around on close

        self.timer.stop()

        self.ipainter = None



    # used for main rendering loop
    def draw(self):
        #print("draw called")

        if self.data:
            self.draw_fn(self.data)
        else:
            self.draw_fn()

        self.update()


    def mousePressEvent(self, event):
        mx = event.x()
        my = event.y()

        self.mouse_down = True
        self.mx = mx
        self.my = my

        if self.data:
            self.mouse_press(mx, my, self.data)
        else:
            self.mouse_press(mx, my)


    def mouseReleaseEvent(self, event):
        mx = event.x()
        my = event.y()

        self.mouse_down = False
        self.mx = mx
        self.my = my

        if self.data:
            self.mouse_release(mx, my, self.data)
        else:
            self.mouse_release(mx, my)

    def mouseMoveEvent(self, event):
        mx = event.x()
        my = event.y()

        self.mx = mx
        self.my = my

        if self.data:
            self.mouse_move(mx, my, self.data)
        else:
            self.mouse_move(mx, my)

    @staticmethod
    def get_key_str(event):
        key = event.key()
        if ord('A') <= key <= ord('Z'):
            modifiers = event.modifiers()

            if modifiers != Qt.ShiftModifier:   # lowercase?
                key += ord('a') - ord('A')

        if 0 <= key <= 255:
            return chr(key)
        else:
            return None


    def keyPressEvent(self, event):
        key_str= self.get_key_str(event)
        if key_str:
            self.keys_down.add(key_str)
            if 'A' <= key_str <= 'Z':   # if uppercase, lowercase version not pressed
                self.keys_down.discard(chr(ord(key_str) + ord('a') - ord('A')))
            if self.data:
                self.key_press(key_str, self.data)
            else:
                self.key_press(key_str)

    def keyReleaseEvent(self, event):
        key_str = self.get_key_str(event)
        self.keys_down.discard(key_str)
        modifiers = event.modifiers()
        if modifiers != Qt.ShiftModifier:   # if SHIFT released, then no uppercase letters pressed
            self.keys_down = self.keys_down - set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        if key_str:
            if self.data:
                self.key_release(key_str, self.data)
            else:
                self.key_release(key_str)

    def is_key_pressed(self, key):
        return key in self.keys_down

    # Commands that affect state such as color or stroke

    # update functions that update the state of Qt based on
    #  state variables.  Call after changing relevant state variables.

    def enable_smoothing(self):
        # left in only for backwards compatibility.  antialising on by default
        pass

    def update_font(self):
        f = QFont(self.font_name, self.font_size, self.font_style, self.font_italic)
        self.ipainter.setFont(f)

    def update_pen(self):
        # set stroke color and width
        if self.stroke_enabled:
            r = int(self.pen_color[0] * 255)
            g = int(self.pen_color[1] * 255)
            b = int(self.pen_color[2] * 255)
            a = int(self.pen_color[3] * 255)
            pen = QPen(QColor(r, g, b, a))
            pen.setWidth(self.stroke_width)
            self.ipainter.setPen(pen)
        else:
            self.ipainter.setPen(Qt.NoPen)

    def update_brush(self):
        # set fill color
        if self.fill_enabled:
            r = int(self.fill_color[0] * 255)
            g = int(self.fill_color[1] * 255)
            b = int(self.fill_color[2] * 255)
            a = int(self.fill_color[3] * 255)
            self.ipainter.setBrush(QBrush(QColor(r, g, b, a)))
        else:
            self.ipainter.setBrush(Qt.NoBrush)

    def set_clear_color(self, r, g, b, alpha=1.0):
        self.clear_color = (r, g, b, alpha)

    def set_stroke_color(self, r, g, b, alpha=1.0):
        self.pen_color = (r, g, b, alpha)
        self.update_pen()

    def set_stroke_width(self, width):
        self.stroke_width = width
        self.update_pen()

    def set_fill_color(self, r, g, b, alpha=1.0):
        self.fill_color = (r, g, b, alpha)
        self.enable_fill()

    def enable_fill(self):
        self.fill_enabled = True
        self.update_brush()

    def disable_fill(self):
        self.fill_enabled = False
        self.update_brush()

    def enable_stroke(self):
        self.stroke_enabled = True
        self.update_pen()

    def disable_stroke(self):
        self.stroke_enabled = False
        self.update_pen()

    def set_font(self, font_name):
        self.font_name = font_name
        self.update_font()

    def set_font_size(self, size):
        self.font_size = size
        self.update_font()

    def set_font_normal(self):
        self.font_style = QFont.Normal
        self.font_italic = False
        self.update_font()

    def set_font_bold(self):
        self.font_style = QFont.Bold
        self.update_font()

    def set_font_italic(self):
        self.font_italic = True
        self.update_font()


    def rotate(self, angle):
        self.ipainter.rotate(angle)

    def translate(self, x, y):
        self.ipainter.translate(x, y)

    def scale(self, sx, sy):
        self.ipainter.scale(sx, sy)

    def save(self):
        self.ipainter.save()

    def restore(self):
        self.ipainter.restore()

    # Drawing command wrapper methods

    def clear(self):

        r = int(self.clear_color[0] * 255)
        g = int(self.clear_color[1] * 255)
        b = int(self.clear_color[2] * 255)
        a = int(self.clear_color[3] * 255)

        self.ipainter.setBackground(QBrush(QColor(r, g, b, a)))
        #print(self.image.rect())
        self.ipainter.eraseRect(self.image.rect());

    def draw_point(self, x, y):
        self.ipainter.drawPoint(x, y)

    def draw_line(self, x1, y1, x2, y2):
        self.ipainter.drawLine(x1, y1, x2, y2)

    def draw_rectangle(self, x, y, w, h):
        self.ipainter.drawRect(x, y, w, h)

    def draw_polygon(self, vertices):
        qpoints = []

        for vertex in vertices:
            qpoints.append(QPoint(vertex[0], vertex[1]))

        poly = QPolygonF(qpoints)
        self.ipainter.drawPolygon(poly)

    def draw_ellipse(self, x, y, rx, ry):
        self.ipainter.drawEllipse(QRectF(x - rx, y - ry, rx * 2, ry * 2))

    def draw_text(self, s, x, y):

        self.ipainter.drawText(x, y, s)


    def get_text_width(self, str):
        f = QFont(self.font_name, self.font_size, self.font_style, self.font_italic)
        fmetric = QFontMetrics(f)
        #return fmetric.boundingRect(str).width()
        return fmetric.width(str)

    def get_text_height(self):
        f = QFont(self.font_name, self.font_size, self.font_style, self.font_italic)
        fmetric = QFontMetrics(f)
        #return fmetric.boundingRect(str).height()
        return fmetric.height()


    def draw_image(self, image, x, y):
        self.ipainter.drawImage(x, y, image)




# cs1lib drawing commands

#  utility

def is_key_pressed(key):
    return canvas.is_key_pressed(key)

def is_mouse_pressed():
    return canvas.mouse_down

def mouse_x():
    return canvas.mx

def mouse_y():
    return canvas.my

def degrees(rad):
    return 180 * rad / pi

#  state commands

def enable_smoothing():
    pass


def disable_smoothing():
    pass


def enable_fill():
    canvas.enable_fill()


def disable_fill():
    canvas.disable_fill()


def set_fill_color(r, g, b, alpha=1.0):
    canvas.set_fill_color(r, g, b, alpha)


def set_clear_color(r, g, b, alpha=1.0):
    canvas.set_clear_color(r, g, b, alpha)


def enable_stroke():
    canvas.enable_stroke()


def disable_stroke():
    canvas.disable_stroke()


def set_stroke_color(r, g, b, alpha=1.0):
    canvas.set_stroke_color(r, g, b, alpha)


def set_stroke_width(width):
    canvas.set_stroke_width(width)


def set_font(font_name):
    canvas.set_font(font_name)


def set_font_size(font_size):
    canvas.set_font_size(font_size)


def set_font_normal():
    canvas.set_font_normal()


def set_font_bold():
    canvas.set_font_bold()

def set_font_italic():
    canvas.set_font_italic()


#  drawing commands

def clear():
    canvas.clear()

def draw_point(x, y):
    canvas.draw_point(x, y)


def draw_line(x1, y1, x2, y2):
    canvas.draw_line(x1, y1, x2, y2)


def draw_polygon(vertices):
    canvas.draw_polygon(vertices)


def draw_triangle(x1, y1, x2, y2, x3, y3):
    draw_polygon([(x1, y1), (x2, y2), (x3, y3)])


def draw_circle(x, y, r):
    draw_ellipse(x, y, r, r)


def draw_ellipse(x, y, rx, ry):
    assert rx >= 0
    assert ry >= 0

    if rx == 0 or ry == 0:
        return

    canvas.draw_ellipse(x, y, rx, ry)


def draw_rectangle(x, y, w, h):
    canvas.draw_rectangle(x, y, w, h)


def draw_text(string, x, y):
    canvas.draw_text(string, x, y)



## transformations and canvas state functions

def push_state():
    canvas.save()

def pop_state():
    canvas.restore()

def rotate(degrees):
    canvas.rotate(degrees)

def translate(x, y):
    canvas.translate(x, y)

# Images

def draw_image(image, x, y, cx = 0, cy = 0, theta = 0):
    push_state()
    translate(x - cx, y - cy)

    if theta != 0:

        translate(cx, cy)
        rotate(theta)
        translate(-cx, -cy)

    canvas.draw_image(image, 0, 0)

    pop_state()

def load_image(filename):
    img = CS1Image()
    img.load(filename)
    return img


def get_text_width(string):
    return canvas.get_text_width(string)


def get_text_height():
    return canvas.get_text_height()

# Main graphics loop

# the frames parameters gives the number of frames to display on the
#  browser version of cs1lib.  Ignored in qt version.
def start_graphics(draw_func=noop, frames=1, data=None, framerate=40,
                title="cs1", width=400, height=400,
                mouse_press=noop, mouse_release = noop, mouse_move=noop,
                key_press=noop, key_release=noop):

    global canvas

    canvas = CS1Canvas(draw_fn = draw_func, data = data, window_x=WINDOW_X, window_y=WINDOW_Y,
                       width=width, height=height, title=title, framerate=framerate,
                       mouse_press=mouse_press, mouse_release=mouse_release, mouse_move=mouse_move,
                       key_press=key_press, key_release=key_release)



    sys.exit(app.exec_())

def cs1_quit():
    print("cs1_quit called")
    app.quit()
    exit()

# Update the frame rate after the Canvas has been created.
def set_framerate(framerate):
    canvas.framerate = framerate
    canvas.timer.setInterval(1000 / framerate)

# for testing purposes
if __name__ == '__main__':

    vx = 1
    x = 200
    y = 200

    def on_click(mx, my):
        print("Mouse click! " + str(mx) + " " + str(my))

    def on_move(mx, my):
        #print("Mouse move! " + str(mx) + " " + str(my))
        pass

    def on_release(mx, my):
        print("Mouse up! " + str(mx) + " " + str(my))

    def on_keydown(key):
        print("Pressed " + key)

    def on_keyup(key):
        print("Released " + key)


    def draw():
        global x, vx
        clear()

        set_clear_color(.8, .4, .4)
        clear()

        set_fill_color(.2, .5, .9)
        set_stroke_color(1, 1, 0)
        draw_rectangle(100, 100, 200, 200)

        set_stroke_color(0, 0, 0)
        set_fill_color(1, 1, 1)
        draw_circle(200, 200, 100)

        if star_img:
            draw_image(star_img, 200, 200, star_img.width()/2, star_img.height()/ 2, x)


        draw_circle(x, y, 5)


        x += vx

        if x + 5 > 300 or x - 5 < 100:
            vx *= -1

        set_font("Times")
        set_font_bold()
        set_font_italic()
        set_font_size(20)

        text = "Hello, world!"
        w = get_text_width(text)

        draw_text("Hello, world!", 200 - w/2, 277)

        h = get_text_height()
        draw_text(str(mouse_x()), 10, 400)
        draw_text( str(mouse_y()), 10, 400 + h)
        draw_text( str(is_mouse_pressed()), 10, 400 + 2 * h)


    star_img = None
    if os.path.exists("star.png"):
        star_img = load_image("star.png")

    start_graphics(draw, width=500, height=500, mouse_press = on_click, mouse_release = on_release, mouse_move = on_move,
                   key_press=on_keydown, key_release=on_keyup)
