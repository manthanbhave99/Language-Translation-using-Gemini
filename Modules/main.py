from modules.api_config import load_api
from modules.gui import launch_gui

def main():
    api = load_api()
    print("API Key Loaded:", bool(api))

    launch_gui()

if __name__ == "__main__":
    main()
