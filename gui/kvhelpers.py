from kivy.clock import Clock
import kivy.metrics as metrics
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty, DictProperty, BooleanProperty, ObjectProperty


# MARK: Extra Functionality
class MouseOver(Widget):
    def __init__(self, **kwargs):
        Window.bind(mouse_pos=self._mouse_move)
        self.hovering = BooleanProperty(False)
        self.poi = ObjectProperty(None)
        self.register_event_type('on_hover')
        self.register_event_type('on_exit')
        super(MouseOver, self).__init__(**kwargs)

    def _mouse_move(self, *args):
        if not self.get_root_window():
            return
        is_collide = self.collide_point(*self.to_widget(*args[1]))
        if self.hovering == is_collide:
            return
        self.poi = args[1]
        self.hovering = is_collide
        self.dispatch('on_hover' if is_collide else 'on_exit')

    def on_hover(self):
        pass

    def on_exit(self):
        pass


class HoverButton(Button, MouseOver):
    def on_hover(self):
        self.opacity = 0.92

    def on_exit(self):
        self.opacity = 1.0


class Toast(AnchorLayout):
    text = StringProperty("Oops! Error")

    def __init__(self, **kwargs):
        super(Toast, self).__init__(**kwargs)

    def show(self, desc):
        self.text = desc
        anim = Animation(y = metrics.dp(50), t = 'in_out_expo')
        anim.start(self)
        Clock.schedule_once(self.exit, 2)

    def exit(self, dt):
        Clock.unschedule(self.exit)
        anim = Animation(y = metrics.dp(-50), t = 'in_out_expo')
        anim.start(self)

    def on_text(self, instance, value):
        self.ids.label.text = value


Factory.register('MouseOver', MouseOver)
