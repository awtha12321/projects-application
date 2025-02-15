import numpy as np


def clockwise(arr, TO_RETURN):
    
    print(arr)
    
    if 0 >= arr.size:
        return TO_RETURN
    else:
        TO_RETURN += arr[0, :].tolist() 
        arr = arr[1:, :]
        
        if arr.size == 0:
            return clockwise(arr, TO_RETURN)
        
        TO_RETURN += arr[:, -1].tolist()
        arr = arr[:,:-1]
        
        
        tmp = arr[-1, :].tolist()
        tmp.reverse()
        TO_RETURN += tmp
        arr = arr[:-1, :]
        
        tmp = arr[:, 0].tolist()
        tmp.reverse()
        TO_RETURN += tmp
        arr = arr[:, 1:]
            
        return clockwise(arr, TO_RETURN)
        

def snail(snail_map):
    
    TO_RETURN = []
    arr = np.array(snail_map)
    
    if arr.size == 0:
        print(arr)
        return []
    
    if arr.size == 1:
        print(arr)
        return arr[0, :]
    else:
        return clockwise(arr, TO_RETURN)