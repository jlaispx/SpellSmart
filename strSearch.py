

def searchString(matchStr, strArray, i):
    if i > len(strArray) - 1:
        return "No"
    if matchStr == strArray[i]:
        return "Yes"
    else:
        return searchString(matchStr, strArray, i+1)


print(searchString("A",["B","D","A"],0))