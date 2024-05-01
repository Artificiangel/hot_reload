from extensions.hot_reload.utils import restore, replace

import modules.text_generation
from modules.text_generation import generate_reply_HF, generate_reply_custom


def test_generator(*a, **kw):
    output = ''
    for letter in "This is a test.":
        output += letter
        yield output

# # Uncomment to replace generator
# replace(modules.text_generation, generate_reply_HF, test_generator)
# replace(modules.text_generation, generate_reply_custom, test_generator)

# # Uncomment to restore original behavior
# restore(modules.text_generation, generate_reply_HF)
# restore(modules.text_generation, generate_reply_custom)
