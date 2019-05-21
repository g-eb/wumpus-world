from wumpus_world.app import App


def restart_app(app, event):
    app.quit()
    app = App()
    app.start()


if __name__ == "__main__":
    app = App()
    app.bind("r", lambda event: restart_app(app, event))
    app.start()
