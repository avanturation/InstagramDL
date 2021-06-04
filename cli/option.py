from optparse import OptionParser


def option_parser():
    parser = OptionParser(usage="usage: $prog [options]")

    parser.add_option(
        "-V",
        "--verbose",
        help="print verbose things",
        action="store_true",
        dest="debug",
    )

    parser.add_option(
        "--post",
        help="instagram post to download",
        dest="post",
        default=None,
        type=str,
    )

    parser.add_option(
        "--user",
        help="instagram user to download",
        dest="user_id",
        default=None,
        type=str,
    )

    parser.add_option(
        "--stories",
        help="download stories but not posts",
        action="store_true",
        dest="stories",
    )

    return parser
