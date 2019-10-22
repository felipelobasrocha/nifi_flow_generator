from nipyapi import canvas

def to_propertie(name, properties):
    try:
        temp = dict()
        for key, value in properties.items():
            if name.lower() in key.lower():
                temp[str(key.split("@")[0])+"."+str(key.split(".")[1])] = value
            
        properties.update(temp)

        return properties

    except Exception as e:
        return str(e)