# Purpose
This is an extension for developers who want to probe the insides of the webui.
Replace bits here and there without waiting those few painfully slow seconds restarting the webui every time you change a line of code.

I developed this while debugging ways to implement parallel text generation, that is why the focus of the examples are on the text generation function!

# How it works
Create a python file or use the existing `test_playground.py` to write your test code.
As you hit save you will notice the code is automatically run.
### Replacing functions
Import the module and function from the webui.
For example
```py
# Tools from the extension
from extensions.hot_reload.utils import restore, replace

import modules.text_generation
from modules.text_generation import generate_reply_HF, generate_reply_custom
```
Write your replacement code you want to test.
```py
def test_generator(*a, **kw):
    output = ''
    for letter in "This is a test.":
        output += letter
        yield output
```
And use the provided `replace` function to overwrite it, **While keeping a backup of the original code safe!**
```py
replace(modules.text_generation, generate_reply_HF, test_generator)
replace(modules.text_generation, generate_reply_custom, test_generator)
```
### Restoring the original behavior
Utilize the `restore` function to revert to the old behavior without having to restart the webui.
Provide the module, and current function that has been overwritten.
```py
restore(modules.text_generation, generate_reply_HF)
restore(modules.text_generation, generate_reply_custom)
```

### Notes
Feel free to make as many test files as you want.
The `extensions/hot_reload` folder is scanned for changes every couple seconds.

# Installation
**Sessions** page: `Install or update an extension` -> `https://github.com/Artificiangel/hot_reload`

Restart the webui.

Start the webui with `--extensions hot_reload`
