import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

class MainWindow(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.morse.generator")

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self)
        window.set_title("Morse Generator")
        #window.set_default_size(400, 300)
        window.present()

if __name__ == "__main__":
    app = MainWindow()
    app.run(None)
