import os


def write_file(input_file,
               path):
    with open("/{}/{}".format(path, input_file), "wb+") as fout:
        for chunk in input_file.chunks():
            fout.write(chunk)


def chmod_file(input_file,
               mod=400):
    os.system("chmod {}".format(mod))
