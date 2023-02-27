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

def divide_geojson_files(dir:str, filename:str, outdir:str, schooltype:str):
    pattern = '''((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])'''
    with open(dir + "/" + filename, 'r', encoding='utf-8') as geojson_f:
        geojson_load = json.load(geojson_f, cls=LazyDecoder)
        data = geojson_load["features"]


        for school in data:
            if school["type"] == "Feature":
                city = ""

                if schooltype == "elementary":
                    city = school["properties"]["A27_005"]
                    if city:
                        result = re.match(pattern, city)        
                        if result:
                            print(result.group(1))
                            new_filename =  filename.split(".")[0] + "_" + result.group(1) + "立"  + school["properties"]["A27_004"] + ".geojson"
                
                elif schooltype == "juniorhigh":
                    city = school["properties"]["A32_002"]
                    if city:
                        result = re.match(pattern, city)
                        if result:
                            print(result.group(1))
                            new_filename = filename.split(".")[0] + "_" + result.group(1) + "立" + school["properties"]["A32_004"] + ".geojson"
                print(new_filename)

                with open(outdir + "/" + new_filename, mode="w") as output_f:
                    output_f.write(json.dumps(school, ensure_ascii = False))

def update_city_name(dir:str, filename:str, schooltype:str):
    pattern = '''((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])'''

    with open(dir + "/" + filename, 'r', encoding='utf-8') as geojson_f:
        geojson_load = json.load(geojson_f, cls=LazyDecoder)
        data = geojson_load["features"]

        for school in data:
            city = ""
            if schooltype == "juniorhigh":
                city = school["properties"]["A32_005"]
            else:
                city = school["properties"]["A27_005"]
            
            if city:
                result = re.match(pattern, city)
                print(city)
                if result:
                    print(result.group(1))
                else:
                    print("result error: city is" + city)
            else:
                print("error school is" + str(school))

if __name__ == '__main__':
    #test()

    for num in range(1, 48):
        elementary_file = "A27-21_" + str(num).zfill(2) + ".geojson"
        divide_geojson_files("./geojson_elementary", elementary_file, "./geojson_elementary_each", "elementary")

    for num in range(1, 48):
        juniorhigh_file = "A32-21_" + str(num).zfill(2) + ".geojson"
        divide_geojson_files("./geojson_juniorhigh", juniorhigh_file, "./geojson_juniorhigh_each", "juniorhigh")
    

    """
    for num in range(1, 48):
        elementary_file = "A27-21_" + str(num).zfill(2) + ".geojson"
        update_city_name("./geojson_elementary", elementary_file, "elementary")


    for num in range(1, 48):
        juniorhigh_file = "A32-21_" + str(num).zfill(2) + ".geojson"
        update_city_name("./geojson_juniorhigh", juniorhigh_file, "juniorhigh")
    """

