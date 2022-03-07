# coding=utf8
import argparse
import gunicorn.app.base


from bbchallenge_backend import app


# Custom Gunicorn application: https://docs.gunicorn.org/en/stable/custom.html
class HttpServer(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--worker-class", type=str, default="sync")
    parser.add_argument("--access-logfile", type=str, default="-")
    parser.add_argument("--error-logfile", type=str, default="-")
    parser.add_argument("--bind", type=str, default="0.0.0.0:55055")
    parser.add_argument("-t", type=int, default=30)

    args = parser.parse_args()

    options = {
        "bind": args.bind,
        "workers": args.workers,
        "worker-class": args.worker_class,
        "access-logfile": args.access_logfile,
        "error-logfile": args.error_logfile,
        "timeout": args.t,
    }

    app.config["CUSTOM_GUNICORN"] = True
    HttpServer(app, options).run()
