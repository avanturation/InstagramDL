import sys
import logging
import asyncio
from utils import Logger
from api import Requester
from cli import header, option_parser

if __name__ == "__main__":
    header()

    optparser = option_parser()
    (options, args) = optparser.parse_args(sys.argv)

    if options.debug is not None:
        logging.getLogger().setLevel(logging.DEBUG)

    else:
        logging.getLogger().setLevel(logging.INFO)

    logger = Logger.generate("Main")

    if options.user_id is None and options.post is None:
        logger.error(
            "Either instagram user or post can not be detected. Check your arguments again."
        )
        exit()

    if options.user_id and options.post:
        logger.error(
            "You can only download a post or all posts of a user. Check your arguments again."
        )
        exit()

    user_id, story_dl, post = None, False, None

    if options.user_id:
        user_id = options.user_id

        if options.stories is not None:
            story_dl = True

        else:
            story_dl = False

    if options.post:
        post = options.post

    logger.debug(
        f"Passed Arguments\nPost: {post}\nUser ID: {user_id}\nStory Download: {story_dl}"
    )

    req = Requester()
    asyncio.run(req.login(user=options.user_login, passwd=options.passwd))
