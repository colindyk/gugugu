import io
import os
import tqdm
import jsonlines



def load_jsonlines(fpath):
    if os.path.exists(fpath):
        f = open(fpath, "r")
        reader = jsonlines.Reader(f)
        res = list(reader)
        f.close()
    else:
        res = None
    return res


