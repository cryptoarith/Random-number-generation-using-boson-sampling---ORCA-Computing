def VonNuemann(modes):
    #Von-Nuemann Algorithm
    code = ''
    final_String = ''
    res = {}
    S1 = []
    S2 = []
    #modes = my_Modes2
    for k in range(len(modes)):
        for i in range(len(modes)):
            if i != (len(modes)-1):
                S1.append((modes[k]))
                S2.append((modes[i]))
            for j in range(len(modes[k])):
                if i == (len(modes)-1):
                    break
                if (int(modes[k][j]) == 0) & (int(modes[i][j]) == 0):
                    if j == 5:
                        code = code + ("/")
                        #print('code is: ', code)
                        break
                elif (int(modes[k][j]) == 0) & (int(modes[i][j]) != 0):
                    code = code + '1'
                    if j == 5:
                        code = code + ("/")
                        #print('code is: ', code)
                        break
                elif (int(modes[k][j]) != 0) & (int(modes[i][j]) == 0):
                    code = code + '0'
                    if j == 5:
                        code = code + ("/")
                        #print('code is: ', code)
                        break
                elif (int(modes[k][j]) != 0) & (int(modes[i][j]) != 0):
                    if j == 5:
                        code = code + ("/")
                        #print('code is: ', code)
                        break

    #we have shown (the states that don't generate code) with "/", then we split them by "/".
    final_String = code.split("/")
    #Remove empty strings from final String.
    final_String[:] = [x for x in final_String if x]
    #We count final String to get the probability of repeating them.

    for i in final_String:
        res[i] = final_String.count(i)
        
    return (S1, S2, code, final_String, res)

#We prepare Final String and find the probability


def prepareData(res):
    pre_Final_String = list(res.keys())
    count_Of_No = list(res.values())
    probabilities = count_Of_No
    sum_No = 0
    for e in range(len(count_Of_No)):
        sum_No = sum_No + count_Of_No[e]

    for e in range(len(count_Of_No)):
        probabilities[e] = count_Of_No[e]/sum_No
    return (pre_Final_String, probabilities)


def finalInt(list_Of_String):
    str1 = ''
    list_Of_Int = []
    for i in range(len(list_Of_String)):
        str1 = str1 + list_Of_String[i]
    list_Of_Int = [int(i) for i in str1]
    return list_Of_Int
