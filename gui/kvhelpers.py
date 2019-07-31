from kivy.core.window import Window
from kivy.properties import StringProperty, DictProperty, BooleanProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.factory import Factory


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
    def __init__(self, **kwargs):
        self.border = 10, 10, 10, 10
        super(HoverButton, self).__init__(**kwargs)

    def on_hover(self):
        self.opacity = 0.92

    def on_exit(self):
        self.opacity = 1.0


Factory.register('MouseOver', MouseOver)
