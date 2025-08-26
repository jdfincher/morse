import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from data import *

class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Morse Generator")
        self.set_default_size(600,400)

        play = Gtk.Button.new_with_label("Play")
        stop = Gtk.Button.new_with_label("Stop")

        input = Gtk.TextView()
        input_buffer = input.get_buffer()

        input.set_left_margin(10)
        input.set_right_margin(10)
        input.set_wrap_mode(wrap_mode=Gtk.WrapMode.WORD)
        input.set_pixels_above_lines(10)
        input.set_pixels_below_lines(10)
        input.set_justification(Gtk.Justification.CENTER)

        input_scroll = Gtk.ScrolledWindow()
        input_scroll.set_child(input)
        input_scroll.set_min_content_height(100)
        input_scroll.set_min_content_width(450)
        input_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        input_scroll.set_size_request(450,-1)

        input_frame = Gtk.Frame()
        input_frame_label = Gtk.Label()
        input_frame_label.set_markup("<span size='large' weight='bold'>Input Message</span>")
        input_frame.set_label_widget(input_frame_label)
        input_frame.set_label_align(0.5)
        input_frame.set_child(input_scroll)

        output = Gtk.TextView()
        output_buffer = output.get_buffer()
        output.set_left_margin(10)
        output.set_right_margin(10)
        output.set_pixels_above_lines(10)
        output.set_pixels_below_lines(10)
        output.set_wrap_mode(wrap_mode=Gtk.WrapMode.WORD)
        output.set_editable(False)
        output.set_cursor_visible(False)
        output.set_justification(Gtk.Justification.CENTER)

        output_scroll = Gtk.ScrolledWindow()
        output_scroll.set_child(output)
        output_scroll.set_min_content_height(100)
        output_scroll.set_min_content_width(450)
        output_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        output_scroll.set_size_request(450,-1)

        output_frame = Gtk.Frame()
        output_frame_label = Gtk.Label()
        output_frame_label.set_markup("<span size='large' weight='bold'>Output Message</span>")
        output_frame.set_label_widget(output_frame_label)
        output_frame.set_label_align(0.5)
        output_frame.set_child(output_scroll)

        top_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10) 
        mid_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        bot_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        bot_box.set_halign(Gtk.Align.CENTER)
        bot_box.set_valign(Gtk.Align.CENTER)
    
        top_box.append(input_frame)
        mid_box.append(output_frame)
        bot_box.append(play)
        bot_box.append(stop)
                
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_halign(Gtk.Align.CENTER)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        main_box.append(top_box)
        main_box.append(mid_box)
        main_box.append(bot_box)

        input_buffer.connect('changed', self.english_to_morse_trans,output_buffer)
        self.set_child(main_box)
    
    def english_to_morse_trans(self, input_buffer, output_buffer):
        if input_buffer:
            input_start = input_buffer.get_start_iter()
            input_end = input_buffer.get_end_iter()
            input_text = input_buffer.get_text(input_start, input_end, True)
            translated = []
            for char in input_text:
                translated.append(english_to_morse[char])
                output_buffer.set_text(' '.join(translated))


class MorseApp(Gtk.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        win = Window(self)
        win.present()
    
    
   

