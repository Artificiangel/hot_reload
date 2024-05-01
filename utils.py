from modules.logging_colors import logger
originals = {}


def replace(module, before: callable, after: callable):
    key = len(originals)

    if hasattr(before, '__original_func__'):
        key = getattr(before, '__original_func__')
        before = originals[key]

    else:
        originals[key] = before

    def wrapped(*a, **kw):
        return after(*a, **kw)

    wrapped.__original_func__ = key
    setattr(module, before.__name__, wrapped)
    logger.info(f'[HotReload]: Replaced function: {before.__name__} with {after.__name__}')


def restore(module, func: callable):
    if not hasattr(func, '__original_func__'):
        logger.warning(f'[HotReload]: Failed to restore: {func.__name__}')
        return

    key = getattr(func, '__original_func__')
    before = originals[key]
    setattr(module, before.__name__, before)
    logger.info(f'[HotReload]: Restored function: {before.__name__}')
