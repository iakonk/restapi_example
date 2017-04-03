import logging
import os


def init_logging(args, fmt='%(asctime)s [%(process)s] %(module)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', log_filter=None):
    fmt = logging.Formatter(fmt, datefmt=datefmt)
    if not args.verbose:
        level = logging.WARNING
    elif len(args.verbose) == 1:
        level = logging.INFO
    elif len(args.verbose) >= 2:
        level = logging.DEBUG

    root_logger = logging.getLogger('')
    root_logger.setLevel(logging.DEBUG)

    if hasattr(args, 'logdir') and args.logdir:
        debug_fh = logging.FileHandler(os.path.join(args.logdir, 'all-debug.log'))
        debug_fh.setLevel(logging.DEBUG)
        debug_fh.setFormatter(fmt)
        root_logger.addHandler(debug_fh)
        info_fh = logging.FileHandler(os.path.join(args.logdir, 'all-info.log'))
        info_fh.setLevel(logging.INFO)
        info_fh.setFormatter(fmt)
        root_logger.addHandler(info_fh)
        warning_fh = logging.FileHandler(os.path.join(args.logdir, 'all-warning.log'))
        warning_fh.setLevel(logging.WARNING)
        warning_fh.setFormatter(fmt)
        root_logger.addHandler(warning_fh)
        error_fh = logging.FileHandler(os.path.join(args.logdir, 'all-error.log'))
        error_fh.setLevel(logging.ERROR)
        error_fh.setFormatter(fmt)
        root_logger.addHandler(error_fh)

    console_fh = logging.StreamHandler()
    console_fh.setLevel(level)
    console_fh.setFormatter(fmt)
    root_logger.addHandler(console_fh)

    if log_filter:
        for handler in logging.root.handlers:
            handler.addFilter(log_filter)
