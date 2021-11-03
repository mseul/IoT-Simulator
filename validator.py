import global_settings

def validateInput(theData):
    splitData = theData.split("##")
    if not (len(splitData) == 2):
        return False
    
    try:
        intConvert = int(splitData[1])
    except:
        return False

    if intConvert > global_settings.curveCeiling:
        return False

    if intConvert < global_settings.curveFloor:
        return False
      
    return True