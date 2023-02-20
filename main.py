import requests
import json
import re

class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)

def test():
    print("test")

def divide_geojson_files(dir:str, filename:str, outdir:str, type:str):
    with open(dir + "/" + filename, 'r', encoding='utf-8') as geojson_f:
        geojson_load = json.load(geojson_f, cls=LazyDecoder)
        data = geojson_load["features"]

        for school in data:
            if school["type"] == "Feature":
                if type == "elementary":
                    new_filename =  filename.split(".")[0] + "_" + school["properties"]["A27_002"] + school["properties"]["A27_004"] + ".geojson"
                elif type == "juniorhigh":
                    new_filename = filename.split(".")[0] + "_" + school["properties"]["A32_002"] + school["properties"]["A32_004"] + ".geojson"
                print(new_filename)

                with open(outdir + "/" + new_filename, mode="w") as output_f:
                    output_f.write(json.dumps(school, ensure_ascii = False))

if __name__ == '__main__':
    #test()

    for num in range(1, 48):
        elementary_file = "A27-21_" + str(num).zfill(2) + ".geojson"
        divide_geojson_files("./geojson_elementary", elementary_file, "./geojson_elementary_each", "elementary")
