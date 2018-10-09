import re
def process(txt):
    print(txt)
    out = re.sub(r'[^ক-হৎড়-য়-অ-ঔ- ঁ-া-ী-েি্ে]', '', txt)
    out = re.sub(r'[-]', '', out)
    return out

print("ok")
