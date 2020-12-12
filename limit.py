# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 14:29:33 2020

@author: Daniel
"""

import multiprocessing as mp
import time as t

def p_limit(p_num, p_max, func, params, kwparams):
    """
    Runs a limited number of processes running at one time.

    Parameters
    ----------
    p_num : int
        The total number of processes.
    p_max : int
        The amount of process that can be ran at one time.
    func : function
        The function to be ran.
    params : list
        A list of tuples. The tuples are the parameter lists for each process.
        Length must be p_num long.
    kwparams : list
        A list of dictionaries. The kwargs for func. Length must be p_num long.

    Returns
    -------
    None.

    """
    
    assert len(params) == p_num, "params must be the name length as p_num"
    assert len(kwparams) == p_num, "kwparams must be the name length as p_num"
    
    wait_list = []
    running_list = []
    
    for i in range(p_num):
        proc = mp.Process(name="mp_tools_limit_" + str(i), target=func, args=params[i], kwargs=kwparams[i])
        wait_list.append(proc)
    
    for i in range(p_max):
        proc = wait_list[i]
        proc.start()
        running_list.append(proc)
        wait_list.remove(proc)
    
    while len(wait_list) != 0:
        remove_list = []
        for i in running_list:
            if not i.is_alive():
                print("Process finished")
                i.join()
                remove_list.append(i)
        
        for i in remove_list:
            running_list.remove(i)
            proc = wait_list.pop(0)
            proc.start()
            running_list.append(proc)

def test(ee, rr="a"):
    t.sleep(5)
    print(ee + rr)

if __name__ == "__main__":
    p_limit(10, 2, test, [("a"),("a"),("a"),("a"),("a"),("a"),("a"),("a"),("a"),("a")], [{"rr": "d"},{"rr": "d"},{"rr": "d"},{"rr": "d"},{"rr": "d"},{"rr": "d"},{"rr": "d"},{"rr": "d"},{"rr": "d"},{"rr": "d"},])
    