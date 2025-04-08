import json
import os

class Config:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.default_config = {
            "screen_width": 800,
            "screen_height": 600,
            "fullscreen": False,
            "fps_cap": 60,
            "sound_volume": 0.7,
            "music_volume": 0.5,
            "controls": {
                "move_up": "w",
                "move_down": "s",
                "move_left": "a",
                "move_right": "d",
                "fire": "space"
            }
        }
        self.config = self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.default_config.copy()
        else:
            self.save_config(self.default_config)
            return self.default_config.copy()
    
    def save_config(self, config=None):
        if config is None:
            config = self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save_config()