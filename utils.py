def write_file(input_file,
               path):
    with open("/{}/{}".format(path, input_file), "wb+") as fout:
        for chunk in input_file.chunks():
            fout.write(chunk)
