import praw
import re
import sys
import datetime
import time
from time import sleep
from praw.helpers import comment_stream

def handle_ratelimit(func, *args, **kwargs):
    while True:
        try:
            func(*args, **kwargs)
            break
        except praw.errors.RateLimitExceeded as error:
            print '\tRate limit exceeded!  Sleeping for %d seconds starting at %s' % (error.sleep_time, datetime.datetime.now())
            time.sleep(error.sleep_time)
        except praw.errors.APIException, e:
            print "[praw.errors.APIException]:", e
            break
        except requests.exceptions.HTTPError, e:
            print "[requests.exceptions.HTTPError]:", e
            break

def main():
    r = praw.Reddit("any platform/1.0 (by /u/dont_call_it_cali)")
    r.login("dont_call_it_cali", "*******")

    target_text = r"^.*\bcali\b.*$"
    response_text = r'''http://i.imgur.com/sdrbmHj.jpeg

The name of the state is California.'''

    blacklist = ['CoDCompetitive', 'MMA', 'OpTicGaming', 'SuicideWatch', 'Colombia', 'leagueoflegends']
    processed = []

    while True:
        for c in comment_stream(r, 'all'):
            if re.match(target_text, c.body, re.IGNORECASE):
                if c.link_id not in processed:
                    if c.subreddit.display_name in blacklist:
                        # subreddit is on the black list, skip replying to it
                        print "skipping comment because subreddit", c.subreddit.display_name, "is in blacklist..."
                        continue

                    handle_ratelimit(c.reply, response_text)
                    processed.append(c.link_id)
                    print "replied to", c.author.name, "in", c.link_url, "at", datetime.datetime.now()
                else:
                    print "skipping because we already replied in this thread:", c.link_id, c.link_url, "at", datetime.datetime.now()

if __name__ == '__main__':
    sys.exit(main())
