import os
import re

from text import TEXT_PATH


def prepare_text(text: str) -> str:
    return ' '.join(
        ''.join(
            re.findall(r'[a-zA-Z., ]', text.replace('\n', ' '))
        ).lower().split()
    )


def generate():
    with open(TEXT_PATH, 'w') as out:
        sample_dir = 'sample/'
        out.write(
            ''.join(
                map(
                    lambda name: prepare_text(
                        open(sample_dir + name, 'r').read()
                    ),
                    filter(
                        lambda name: name != 'sample.txt',
                        next(os.walk(sample_dir))[2]
                    )
                )
            )
        )


generate()
