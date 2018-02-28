#!/usr/bin/env python


"""This script takes 2 arguments:
  * -r / --role
  * -e / --env
  * -x / --exclude [Optional]
and uses a yaml configuration file, default: ./packagelist.yaml
to return a list of package names to be installed.

Example:
./packagelist.py --role account_services --env prod

talpay-account-ibusiness talpay-account-reconnet

See the yaml config to get an idea of including / excluding packages.
"""

import argparse
import io
import sys
import yaml


def setup():
    """Simple setup used to pass arguments to main"""
    parser = argparse.ArgumentParser(
        description='Lists packages for the target role / environment.',
    )

    parser.add_argument('-r', '--role', type=str,
                        help='role to target', required=True)
    parser.add_argument('-e', '--env', type=str,
                        help='environment to target', default=None)
    parser.add_argument('-x', '--exclude',
                        help='output excluded packages', action='store_true')
    parser.add_argument('-v', '--version', type=str,
                        help='package version', default=None)
    parser.add_argument('-f', '--config', type=str,
                        help='configuration file',
                        default="./packagelist.yaml")

    return parser.parse_args()


def main(args):
    """Where the good stuff happens.
    Consider splitting up if it gets too long
    """
    with open(args.config, 'r') as config:
        try:
            role_config = yaml.load(config)[args.role]

            """Load env config if present"""
            try:
                env_config = role_config['environments'][args.env]
            except KeyError:
                env_config = None

            """Load ver config if present"""
            try:
                ver_config = role_config['versions']
            except KeyError:
                ver_config = None

            """Work out the package list for this role"""
            rinc = role_config['include']
            try:
                rexc = role_config['exclude']
            except KeyError:
                rexc = []

            package_list = rinc
            exclude_list = rexc

            """Calculate package list based on environment"""
            if env_config is not None:
                try:
                    einc = env_config['include']
                except KeyError:
                    einc = []
                try:
                    eexc = env_config['exclude']
                except KeyError:
                    eexc = []

                if isinstance(einc, basestring):
                    package_list.append(einc)
                else:
                    package_list.extend(einc)

                if isinstance(eexc, basestring):
                    exclude_list.append(eexc)
                else:
                    exclude_list.extend(eexc)

            """Calculate package list based on version"""
            if args.version is not None:
                v = str(args.version)

                if ver_config is not None:
                    for key, val in ver_config.iteritems():
                        if v.startswith(str(key)):
                            try:
                                vinc = val['include']
                            except KeyError:
                                vinc = []
                            try:
                                vexc = ver_config['exclude']
                            except KeyError:
                                vexc = []

                            if isinstance(vinc, basestring):
                                package_list.append(vinc)
                            else:
                                package_list.extend(vinc)

                            if isinstance(vexc, basestring):
                                exclude_list.append(vexc)
                            else:
                                exclude_list.extend(vexc)

            """Remove excluded packages"""
            package_list = [pkg for pkg in package_list if pkg not in exclude_list]

            """Add a version to the packages if we specify one"""
            if args.version is not None:
                v = str(args.version)
                package_list = [ "%s-%s" % (pkg, v) for pkg in package_list]

            if args.exclude:
                the_list = exclude_list
            else:
                the_list = package_list

            print ' '.join(sorted(the_list))

            return 0

        except yaml.YAMLError as err:
            print(err)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(setup()))
