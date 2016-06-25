import RPi.GPIO as GPIO
import requests
import time
import click

from jenkinsapi.jenkins import Jenkins
from config import Config


GPIO.setmode(GPIO.BOARD)


class Shine(Config):
    def __init__(self, project, pins):
        self.PROJECT = project
        self.jenkins = self.get_server_instance()
        pins = [int(pin) for pin in pins.split(",")]
        self.setup_pins(pins)
        RED = zip(pins, self.pin_red)
        GREEN = zip(pins, self.pin_green)
        BLUE = zip(pins, self.pin_blue)
        ALL = zip(pins, self.pin_all)
        STOP = zip(pins, self.pin_stop)
        self.BUILD_COLORS = {
            'ABORTED': RED,
            'FAILURE': RED,
            'SUCCESS': GREEN,
            'UNSTABLE': BLUE,
            'ALL': ALL,
            'NONE': STOP
        }
        self.last = 'ALL'

    def setup_pins(self, pins):
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 1)

    def change_color(self, color):
        for pin, control in color:
            GPIO.output(pin, control)

    def get_server_instance(self):
        server = Jenkins(
            self.JENKINS_URL,
            username=self.LOGIN,
            password=self.PASSWORD)
        return server

    def get_build_status(self):
        project = self.jenkins[self.PROJECT]
        running = self.is_running(project)
        if not running and self.last == "ALL" :
            build = project.get_last_build()
            last = build.get_status()
        else:
            last = self.last
        return (running, last)

    def is_running(self, project=None):
        if not project:
            project = self.jenkins[self.PROJECT]
        if project.is_running():
            result = True
        else:
            result = False
        return result

    def do(self):
        try:
            while True:
                running, self.last = self.get_build_status()

                while running:
                    self.change_color(self.BUILD_COLORS['NONE'])
                    time.sleep(2)
                    self.change_color(self.BUILD_COLORS[self.last])
                    running = self.is_running()
                self.change_color(self.BUILD_COLORS[self.last])
                time.sleep(5)
                
        except KeyboardInterrupt:
            GPIO.cleanup()

        except BaseException, err:
            self.do()
     

@click.command()
@click.option('--project_name', help='Jenkins project name')
@click.option('--pins', help='RGB pin nubmers np."11, 13, 15"')
@click.argument('project_name')
@click.argument('pins')
def disco(project_name, pins):
    shine = Shine(project_name, pins)
    shine.do()


if __name__ == "__main__":
    disco()
