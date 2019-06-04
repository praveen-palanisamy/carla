#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import argparse
import math
import random
import time

red = carla.Color(255, 0, 0)
green = carla.Color(0, 255, 0)
blue = carla.Color(47, 210, 231)
cyan = carla.Color(0, 255, 255)
yellow = carla.Color(255, 255, 0)
orange = carla.Color(255, 162, 0)
white = carla.Color(255, 255, 255)

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    args = argparser.parse_args()

    try:
        client = carla.Client(args.host, args.port)
        client.set_timeout(2.0)

        world = client.get_world()
        m = world.get_map()
        debug = world.debug

        # spawn_point1 = carla.Transform()
        # spawn_point1.location.x = -18
        # spawn_point1.location.y = 1.2
        # spawn_point1.location.z = 18
        # spawn_point1.rotation.roll = 0.0
        # spawn_point1.rotation.pitch = 0.0

        # spawn_point2 = carla.Transform()
        # spawn_point2.location.x = -20
        # spawn_point2.location.y = 1.2
        # spawn_point2.location.z = 18
        # spawn_point2.rotation.roll = 0.0
        # spawn_point2.rotation.pitch = 0.0

        # player
        # print(world.get_blueprint_library())
        # exit(1)


        for i in range(50):
            print ("-----------------------------------------")
            spawn_point = carla.Transform()
            spawn_point.location = world.get_random_location_from_navigation()
            print ("SPAWN AT:", spawn_point.location.x, spawn_point.location.y, spawn_point.location.z)
            blueprint = random.choice(world.get_blueprint_library().filter('walker.pedestrian.*'))
            player = None
            while player is None:
                player = world.try_spawn_actor(blueprint, spawn_point)

            blueprint = random.choice(world.get_blueprint_library().filter('controller.ai.walker'))
            walker_controller = world.spawn_actor(blueprint, carla.Transform(), attach_to=player)
            walker_controller.start()

            time.sleep(0.4)


            target = world.get_random_location_from_navigation()
            print ("TARGET AT:", target.x, target.y, target.z)

            walker_controller.go_to_location(target)
            # time.sleep(0.5)

        while (1):
            time.sleep(1);

        # a = carla.Location(-141.789, -143.839, 0.139954)
        # b = carla.Location(-29.7504, -26.8764, 0.270432)
        # points = []
        # points = client.create_walker(a, b)
        # for i in range(len(points)-1):
        #     a1 = carla.Location(points[i].x, points[i].y, points[i].z)
        #     b1 = carla.Location(points[i+1].x, points[i+1].y, points[i+1].z)
        #     # print(a.x, a.y, a.z)
        #     debug.draw_line(a1, b1, color=orange, thickness=0.5, life_time=12)
        #     # debug.draw_line(a, a+carla.Location(z=1000), color=orange, thickness=0.2, life_time=12)
        #     debug.draw_point(a1, 1, red, 12)

    finally:
        pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        pass