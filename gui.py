import tkinter as tk
import keyboard
from config_file import config_create
from configparser import ConfigParser
from listener import start_loop_with_key_event
from get_coordinates import coordinate_get


class CustomKeybindManager(tk.Tk):
    def __init__(self):
        super().__init__()

        # List for all active hotkeys for listener
        self.active_hotkeys = {}

        self.config_create = config_create()

        # Read the config file
        self.config = ConfigParser()
        self.config.read('config.ini')

        # Get the x,y
        self.x = int(self.config.get('General', 'coordinates_x'))
        self.y = int(self.config.get('General', 'coordinates_y'))

        # hotkey for activating the loop
        self.active_hotkeys[self.config.get('General', 'keybind')] = keyboard.add_hotkey(
            self.config.get('General', 'keybind'),
            lambda: start_loop_with_key_event(self.x, self.y)
        )

        # Title
        self.title("Auto Clicker V2.1")
        self.key_in_config = self.config.get('General', 'keybind')

        # Create a label widget and add it to the window
        self.label_text = f"Hello There, Press [{self.key_in_config.upper()}] to start"
        self.key_main_label = tk.Label(self, text=self.label_text)
        self.key_main_label.pack(pady=10)

        # Status label and coordinates
        self.location_message = f"X={self.x} Y={self.y}"
        self.location = f"{self.location_message}"
        self.status_label = tk.Label(self, text=f"Coordinates: {self.location}", font=('Arial', 12, 'bold'))
        self.status_label.pack()

        # Change keybind
        self.keybind_button = tk.Button(text="Change keybind", width=50, command=self.change_keybind)
        self.keybind_button.pack(pady=10)

        # Change coordinates
        self.coordinates_button = tk.Button(text="Change coordinates", width=50, command=self.change_coord)
        self.coordinates_button.pack(pady=10)

    # Change the keybind main function
    def change_keybind(self):
        self.status_label.config(text="Press Any Key")
        self.after(100, self.read_key_event)

    # Change the coordinate main function
    def change_coord(self):
        self.status_label.config(text="Capturing Coordinates in 5 seconds")
        self.after(5000, self.change_x_y)

    # Side function for change_coord
    def change_x_y(self):
        """
        Get the x,y and then change the config file and the current
        self.x and self.y to avoid restarting to save changes
        """

        # Get the x y
        x, y = coordinate_get()
        self.x = x
        self.y = y

        # Change the config files
        self.config.set('General', 'coordinates_x', str(x))
        self.config.set('General', 'coordinates_y', str(y))
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

        # Update the status label
        self.status_label.config(text=f"Coordinates: X={self.x} Y={self.y}")

    # Part of change keybind
    def read_key_event(self):
        """
        Get the key pressed and then rewrite the keybind
        in the config file while putting, then remove all
        hotkey put inside the active hotkey dictionary and
        make a new one putting it to the same dictionary
        """

        # Get the key pressed and put it to the ini file
        event = keyboard.read_event()
        key_pressed = ""
        if event.event_type == keyboard.KEY_DOWN:
            key_pressed = event.name

            self.config.set('General', 'keybind', key_pressed)
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)

        # Change some widget text
        self.status_label.config(text=f"Coordinates: {self.location}")
        self.key_main_label.config(text=f"Hello There, Press [{key_pressed.upper()}] to start")

        # Remove all current hot key for the listener
        for key, active_key in list(self.active_hotkeys.items()):
            keyboard.remove_hotkey(active_key)
            del self.active_hotkeys[key]

        # Make a new one putting it to the dictionary
        self.active_hotkeys[key_pressed] = keyboard.add_hotkey(
            key_pressed, lambda: start_loop_with_key_event(self.x, self.y)
        )


def main():
    app = CustomKeybindManager()
    app.mainloop()


if __name__ == "__main__":
    main()
