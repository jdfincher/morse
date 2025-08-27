import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GLib
from data import english_to_morse, morse_to_english
from sound import play_sound
import pygame

flag = True

class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Morse Generator")
        self.set_default_size(400,500)
        self.set_resizable(False)
        
        logo = Gtk.Picture.new_for_filename("image/logo.png")
        logo.set_vexpand(True)
        logo.set_content_fit(Gtk.ContentFit.CONTAIN)
        logo.set_margin_bottom(5)
        logo.set_name("logo")

        play = Gtk.Button.new_with_label("PLAY")
        stop = Gtk.Button.new_with_label("STOP")
        clear = Gtk.Button.new_with_label("CLEAR")

        input = Gtk.TextView()
        input.set_name("input")
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
        output.set_name("output")
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
        bot_box.append(clear)
                
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_halign(Gtk.Align.CENTER)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        main_box.append(logo)
        main_box.append(top_box)
        main_box.append(mid_box)
        main_box.append(bot_box)
        
        clear.connect('clicked', self.clear_buffer,input_buffer,output_buffer)
        input_buffer.connect('changed', self.english_to_morse_trans,output_buffer)
        self.set_child(main_box)
        play.connect('clicked', self.play_morse, output_buffer)
        stop.connect('clicked', self.stop_morse)
        
        
        css = Gtk.CssProvider()
        css.load_from_path('src/style.css')
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),
                                                  css,
                                                  Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                                                  )

    def english_to_morse_trans(self, input_buffer, output_buffer):
        if input_buffer:
            input_start = input_buffer.get_start_iter()
            input_end = input_buffer.get_end_iter()
            input_text = input_buffer.get_text(input_start, input_end, True).lower()
            translated = []
            for char in input_text:
                if char in english_to_morse:
                    translated.append(english_to_morse[char])
                    output_buffer.set_text(' '.join(translated))
                elif not char:
                    output_buffer.set_text("")
    
    def clear_buffer(self, button, input_buffer, output_buffer):
        output_buffer.set_text("")
        input_buffer.set_text("")
    
        
    def play_next(self, index, text):
        dit = 0.15
        dah = 0.45
        global flag
        while index < len(text) and not flag == False:
            for char in text[index]:
                if char == chr(183):
                    play_sound(dit)
                    index += 1
                    GLib.timeout_add((dit*1000)+50, self.play_next, index, text)
                    return False
                elif char == '-':
                    play_sound(dah)
                    index += 1
                    GLib.timeout_add((dah*1000)+50, self.play_next, index, text)
                    return False
                else:
                    index += 1
                    GLib.timeout_add(dit*1000, self.play_next, index, text)
                    return False
        return False

    def play_morse(self,button,output_buffer):
        global flag
        index = 0
        start = output_buffer.get_start_iter()
        end = output_buffer.get_end_iter()
        text = output_buffer.get_text(start, end, True)
        if index < len(text):
            flag = True
            self.play_next(index, text)

    def stop_morse(self, button):
        global flag
        if not pygame.mixer.get_init() is None:
            flag = False
            pygame.mixer.stop()





class MorseApp(Gtk.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        win = Window(self)
        win.present()
    
    
   

