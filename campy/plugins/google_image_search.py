#
# Copyright (c) 2011 Ben Belchak <ben@belchak.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import traceback
import re
import simplejson
import httplib2

from plugin import CampyPlugin
import settings

class GoogleImage(CampyPlugin):
    def handle_message(self, campfire, room, message):
        body = message['body']
        if not body:
            return

        if not body.startswith(settings.CAMPFIRE_BOT_NAME):
            return

        m = re.match('%s: gis (?P<search_string>\w+)$' % settings.CAMPFIRE_BOT_NAME, body)
        if m:
            try:
                headers, content = httplib2.Http().request(
                    "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=%s" %
                    m.group('search_string'))
                json = simplejson.loads(content)
                self.speak_image_url(room, json['responseData']['results'][0]['unescapedUrl'])
            except (KeyError,):
                print traceback.format_exc()


    def speak_image_url(self, room, url):
        room.speak(unicode(url))
