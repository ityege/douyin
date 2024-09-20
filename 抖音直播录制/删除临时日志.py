import os

files = os.listdir("record_tmp_path")
for file in files:
    print(os.path.join(os.getcwd(), "record_tmp_path", file))
    try:
        os.remove(os.path.join(os.getcwd(), "record_tmp_path", file))
    except Exception as e:
        print(e)
        pass

