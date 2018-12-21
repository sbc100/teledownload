#!/usr/bin/env python3
# Copyright (C) Sam Clegg <sam@superduper.net>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Download all medea media files from a conversation with a telegram users.
"""

import argparse
import logging
import os
import sys

from telethon import TelegramClient, events, sync
from telethon.tl.types import PeerUser
from telethon.tl.types import InputMessagesFilterPhotoVideo, MessageMediaPhoto


def run(client, options):
    print('Downloaded messages from: %s' % options.username)

    user = client.get_entity(options.username)
    total = client.get_messages(user).total

    print('Found user: %s %s (%s)' % (user.first_name, user.last_name,
                                      user.username))
    print('Total messages: %s' % total)

    if not os.path.isdir(options.outdir):
        os.makedirs(options.outdir)

    for message in client.iter_messages(user):
        if not message.media:
            continue
        if not isinstance(message.media, MessageMediaPhoto):
            continue

        date = message.date
        filename = '{}-{:02}-{:02}_{:02}-{:02}-{:02}.jpg'.format(
                date.year, date.month, date.day,
                date.hour, date.minute, date.second,
        )
        filename = os.path.join(options.outdir, filename)
        if os.path.exists(filename):
            print("Skipping photo.. %s" % filename)
            if not os.path.getsize(filename):
                print("OOOOO")
            continue

        print("Downloading photo.. %s" % filename)
        message.download_media(filename)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d', '--debug', action='store_true',
        help='enable logging')
    parser.add_argument('username', metavar='USER',
        help='username/phone number of converstaion to download')
    parser.add_argument('outdir', metavar='DIR',
        help='directory in which to download media')
    options = parser.parse_args()
    if options.debug:
        logging.basicConfig(level=logging.DEBUG)

    api_hash = os.environ.get('TG_API_HASH')
    api_id = os.environ.get('TG_API_ID')
    if api_id is None:
        print('TG_API_ID environment variable not set')
        return 1
    if api_hash is None:
        print('TG_API_HASH environment variable not set')
        return 1
    with TelegramClient('teledownload', api_id, api_hash) as client:
        run(client, options)


if __name__ == '__main__':
    sys.exit(main())
