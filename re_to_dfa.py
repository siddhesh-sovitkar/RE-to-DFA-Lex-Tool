import pandas as pd
import collections


id_int = 0
map_key = 0
table_list = []
dfa_id = 'A'
new_state_list = []
nslp = 0
nons = 0
fv = 0
dfa_state_map = [['NULL']]
dfa_id_map = ['@']



def push_state_id(s_id,state_name):
    global dfa_state_map, dfa_id_map

    dfa_state_map.append(state_name)
    dfa_id_map.append(s_id)


def get_state_id(state_name):
    global dfa_state_map, dfa_id_map
    for i in dfa_state_map:
        if(collections.Counter(i)==collections.Counter(state_name)):
            y = i
            break

    id = dfa_state_map.index(y)
    return dfa_id_map[id]



def det_moves(E_closure, table):
    global alph,fv
    moves_dict = {}
    for k in list(alph):
        temp = []
        for i in E_closure:
            jumps = table.loc[table['State_id']==i][k]
            jumps = jumps.tolist()
            jumps = jumps[0]
            if (jumps != 'NULL'):
                if (isinstance(jumps, list)):
                    for s in jumps:
                        temp.append(s)
                else:
                    temp.append(jumps)
        if(fv==0):
            if(len(temp)!=0):
                moves_dict[k] = [temp]
            else:
                moves_dict[k] = [['NULL']]
        else:
            if (len(temp) != 0):
                moves_dict[k] = temp
            else:
                moves_dict[k] = ['NULL']


    print(moves_dict)
    fv = 1
    return moves_dict



def bfs(E_closure, table):
    queue = []
    for j in E_closure:
        queue.append(j)


    while(len(queue)!= 0):

        temp_states = table.loc[table['State_id']==queue[0]]['E']
        temp_states = temp_states.tolist()
        temp_states = temp_states[0]
        queue.pop(0)
        if(temp_states != 'NULL'):
            if(isinstance(temp_states,list)):
                for i in temp_states:
                    queue.append(i)
                    E_closure.append(i)
            else:
                queue.append(temp_states)
                E_closure.append(temp_states)

    return E_closure



def gen_dfa_state_id():
    global dfa_id
    t = dfa_id
    dfa_id = chr(ord(dfa_id)+1)
    return t


def get_new_state(table, state_id):
    global new_state_list,alph
    temp = []
    nf = 0
    n = 'NULL'
    N = ['NULL']

    for k in list(alph):
        s = table.loc[table['state id']==state_id][k]
        s = s.tolist()
        temp.extend(s)

    print("templist = "+str(temp))

    if(len(new_state_list)==0):
        for i in temp:
            new_state_list.append(i)





        while n in new_state_list:
            new_state_list.remove(n)
        while N in new_state_list:
            new_state_list.remove(N)


        print("new state list = " + str(new_state_list))
        return


    for j in temp:
        for l in new_state_list:
            if(collections.Counter(j) == collections.Counter(l)):
                nf = 1

        if(nf==0):
            new_state_list.append(j)
        nf = 0

    while n in new_state_list:
        new_state_list.remove(n)
    while N in new_state_list:
        new_state_list.remove(N)

    print("new state list = "+str(new_state_list))










def nfa_to_dfa(table):
    global alph,new_state_list,nslp,nons,dfa_id_map,dfa_state_map
    E_closure = []
    st_type = 'I'

    nfa_initial_state = table.loc[table['state type'] == 'I']['State_id']
    nfa_initial_state = nfa_initial_state.tolist()
    nfa_initial_state = nfa_initial_state[0]

    nfa_final_state = table.loc[table['state type']=='F']['State_id']
    nfa_final_state = nfa_final_state.tolist()
    nfa_final_state = nfa_final_state[0]

    e_states = table.loc[table['state type']=='I']['E']
    e_states = e_states.tolist()
    e_states = e_states[0]
    if (isinstance(e_states, list)):
        for i in e_states:
            E_closure.append(i)
    else:
        E_closure.append(e_states)


    print(E_closure)
    if(E_closure[0]=='NULL'):
        E_closure = [nfa_initial_state]

    else:
        E_closure = bfs(E_closure, table)
        print(E_closure)

    for i in E_closure:
        if (i == nfa_final_state):
            st_type = 'IF'
            break

    moves_dict = det_moves(E_closure,table)
    t = gen_dfa_state_id()
    temp_dict = {'state type': st_type,'state id':t}
    temp_dict.update(moves_dict)
    dfa = pd.DataFrame(temp_dict)
    dfa = dfa.astype('object')
    print(dfa)
    get_new_state(dfa,t)
    push_state_id(t,nfa_initial_state)


    while(nslp!=len(new_state_list)):
            E_closure = []
            st_type = 'S'
            s1 = new_state_list[nslp]
            nslp += 1
            print("nslp  = "+str(nslp))
            if(isinstance(s1,str)):


                e_states = table.loc[table['State_id'] == s1]['E']
                e_states = e_states.tolist()
                e_states = e_states[0]
                if (isinstance(e_states, list)):
                    for i in e_states:
                        E_closure.append(i)
                else:
                    E_closure.append(e_states)


                if (E_closure[0] == 'NULL'):
                    E_closure = [s1]

                else:
                    E_closure = bfs(E_closure, table)
                    print(E_closure)
                    for i in E_closure:
                        if(i == nfa_final_state):
                            st_type = 'F'
                            break
            elif(isinstance(s1,list)):
                print("s1 = "+str(s1))
                for state in s1:
                    temp_closure = []
                    if (state == nfa_final_state):
                        st_type = 'F'
                    e_states = table.loc[table['State_id'] == state]['E']
                    e_states = e_states.tolist()
                    e_states = e_states[0]
                    print(e_states)
                    if (isinstance(e_states, list)):
                        for i in e_states:
                            temp_closure.append(i)
                    else:
                        temp_closure.append(e_states)



                    if(temp_closure[0] == 'NULL'):
                        continue
                    else:

                        temp_closure = bfs(temp_closure, table)

                    print("temp closure = " + str(temp_closure))
                    E_closure.extend(temp_closure)
                    print("E_closure = " + str(E_closure))

                for i in E_closure:
                    if (i == nfa_final_state):
                        st_type = 'F'
                        break

            E_closure = list(collections.OrderedDict.fromkeys(E_closure))
            print("E_closure = " + str(E_closure))
            moves_dict = det_moves(E_closure, table)
            t = gen_dfa_state_id()
            push_state_id(t,s1)
            temp_dict = {'state type': st_type, 'state id': t}
            temp_dict.update(moves_dict)
            dfa = dfa.append(temp_dict,ignore_index=True)
            print(dfa)
            get_new_state(dfa,t)

    print(dfa_id_map)
    print(dfa_state_map)

    for i in range(0,dfa.shape[0]):
        for k in list(alph):
            x = dfa.iloc[i][k]

            dfa.iloc[i][k] = get_state_id(x)

    print(dfa)
    return dfa


def gen_state_id(num):
    global id_int
    t1 = []
    for i in range(0, num):
        t1.append('q'+str(id_int))
        id_int += 1
    return t1

def tablemap_entry(table):
    global table_list, map_key
    table_list.append(table)
    temp = map_key
    map_key +=1
    return temp


def tablemap_get_table(key):
    global table_list
    df = table_list[int(key)]
    return df


def union(rgt,lft):

    global alph
    if(isinstance(rgt,str)):
        states = gen_state_id(2)
        temp = list(alph)
        temp.remove(rgt)
        union_dict = {'state type': ['I', 'F'], 'State_id': states, 'E': ['NULL', 'NULL'], rgt: [states[1], 'NULL']}
        union_table1 = pd.DataFrame(union_dict)
        null_list = ['NULL', 'NULL']
        for k in temp:
            union_table1[k]= null_list
    else:
        union_table1 = tablemap_get_table(rgt)

    if (isinstance(lft,str)):
        states = gen_state_id(2)
        temp = list(alph)
        temp.remove(lft)
        union_dict = {'state type': ['I', 'F'], 'State_id': states, 'E': ['NULL', 'NULL'], lft: [states[1], 'NULL']}
        union_table2 = pd.DataFrame(union_dict)
        null_list = ['NULL','NULL']
        for k in temp:
            union_table2[k]= null_list

    else:
        union_table2 = tablemap_get_table(lft)

    ustate = gen_state_id(2)
    s1 = union_table1.loc[union_table1['state type']=='I']['State_id']
    s2 = union_table2.loc[union_table2['state type']=='I']['State_id']

    s1 = s1.tolist()
    s2 = s2.tolist()

    s_list = s1 + s2
    union_table1.loc[union_table1['state type']=='F','E'] = ustate[1]
    union_table2.loc[union_table2['state type']=='F','E'] = ustate[1]


    union_dict = {'state type':['I','F'],'State_id': ustate,'E':[s_list, 'NULL']}
    union_table3 = pd.DataFrame(union_dict)
    null_list = ['NULL', 'NULL']
    for k in list(alph):
        union_table3[k] = null_list
    df = pd.concat([union_table1,union_table2,union_table3],ignore_index=True,sort=False)
    df.loc[(df['State_id']!=ustate[0])&(df['State_id']!=ustate[1]),['state type']]='S'
    return df







def concat(rgt,lft):
    global alph
    if (isinstance(rgt, str)):
        states = gen_state_id(2)
        temp = list(alph)
        temp.remove(rgt)
        concat_dict = {'state type': ['I', 'F'], 'State_id': states, 'E': ['NULL', 'NULL'], rgt: [states[1], 'NULL']}
        concat_table1 = pd.DataFrame(concat_dict)
        null_list = ['NULL', 'NULL']
        for k in temp:
            concat_table1[k] = null_list
    else:
        concat_table1 = tablemap_get_table(rgt)

    if (isinstance(lft, str)):
        states = gen_state_id(2)
        temp = list(alph)
        temp.remove(lft)
        concat_dict = {'state type': ['I', 'F'], 'State_id': states, 'E': ['NULL', 'NULL'], lft: [states[1], 'NULL']}
        concat_table2 = pd.DataFrame(concat_dict)
        null_list = ['NULL', 'NULL']
        for k in temp:
            concat_table2[k] = null_list

    else:
        concat_table2 = tablemap_get_table(lft)


    s1 = concat_table1.loc[concat_table1['state type']=='I']['State_id']
    s1 = s1.tolist()
    s1 = s1[0]
    concat_table1.loc[concat_table1['state type'] == 'I','state type'] = 'S'
    concat_table2.loc[concat_table2['state type']=='F','E'] = s1
    concat_table2.loc[concat_table2['state type']=='F','state type'] = 'S'


    df = pd.concat([concat_table2,concat_table1],ignore_index=True,sort=False)
    return df


def closure(rgt,lft):
    global alph
    if (isinstance(lft, str)):
        states = gen_state_id(2)
        temp = list(alph)
        temp.remove(lft)
        closure_dict = {'state type': ['I', 'F'], 'State_id': states, 'E': ['NULL', 'NULL'], lft: [states[1], 'NULL']}
        closure_table1 = pd.DataFrame(closure_dict)
        null_list = ['NULL', 'NULL']
        for k in temp:
            closure_table1[k] = null_list

    else:
        closure_table1 = tablemap_get_table(lft)

    kc_states = gen_state_id(2)
    null_list = ['NULL', 'NULL']
    closure_dict = {'state type': ['I', 'F'], 'State_id': kc_states, 'E': ['NULL', 'NULL']}
    kc_table = pd.DataFrame(closure_dict)
    for k in list(alph):
        kc_table[k] = null_list
    s1 = closure_table1.loc[closure_table1['state type'] == 'I']['State_id']
    s1 = s1.tolist()
    s1 = s1[0]
    closure_table1.loc[closure_table1['state type'] == 'I', 'state type'] = 'S'


    if(rgt=='*'):

        state_list = [s1, kc_states[1]]
        kc_table.loc[kc_table['state type'] == 'I', 'E'] = [state_list]

    else:

        kc_table.loc[kc_table['state type'] == 'I', 'E'] = s1

    state_list = [kc_states[1], s1]
    closure_table1.loc[closure_table1['state type'] == 'F', 'E'] = [state_list]
    closure_table1.loc[closure_table1['state type'] == 'F', 'state type'] = 'S'
    df = pd.concat([closure_table1, kc_table], ignore_index=True, sort=False)
    df.loc[(df['state type'] != 'I') & (df['state type'] != 'F'), 'state type'] = 'S'
    return df








def priority(var):
    if(var=='^'):
        return 5
    elif(var=="."):
        return 4
    elif(var=="+"):
        return 3
    elif(var==")"):
        return 2
    else:
        return 1


def inf_to_post(exp):
    pc_flag = 0
    stack = []
    tos = -1
    temp_list = []
    for i in exp:
        #print(str(stack)+"  tos = "+str(tos)+"   postfix =  "+str(temp_list))
        if(i.isalpha() or pc_flag==1 or i=='0' or i=='1'):
            if(pc_flag == 1 and i=='+'):
                i = '$'

            pc_flag = 0
            temp_list.append(i)

        elif(len(stack)==0):
            if(i=='^'):
                pc_flag = 1
            stack.append(i)
            tos+=1

        else:
            if(i=="("):
                stack.append(i)
                tos+=1
                continue
            if(i=='^'):
                pc_flag = 1

            while(tos>=0 and priority(stack[tos])>= priority(i)):
                s = stack.pop()
                temp_list.append(s)
                tos-=1
            if(i==")"):
                stack.pop()
                tos-=1
                continue

            stack.append(i)
            tos+=1

    while(tos>=0):
        s = stack.pop()
        temp_list.append(s)
        tos -= 1

    return "".join(temp_list)



def check_equality(string, dfa,state_list):
    global alph
    ret_list = []
    set_list = []
    set_no = []
    set_count = 1
    for i in range(0,len(string)-1):
        for j in range(i+1,len(string)):
            print("i = "+str(string[i])+" j = "+str(string[j]))
            count = 0
            for k in alph:
                s1 = dfa.loc[dfa['state id'] == string[i]][k]
                s1 = s1.tolist()
                s1 = s1[0]
                s2 = dfa.loc[dfa['state id'] == string[j]][k]
                s2 = s2.tolist()
                s2 = s2[0]

                print("s1 = " + str(s1) + " s2 = " + str(s2))

                for s in state_list:
                    if(s1 in s and s2 in s):
                        count += 1
                print("count = "+str(count))
            if(count == len(alph)):
                if(string[i]  in set_list and string[j]  in set_list):
                    continue
                if(string[i] not in set_list and string[j] not in set_list):
                    set_list.append(string[i])
                    set_list.append(string[j])
                    set_no.append(set_count)
                    set_no.append(set_count)
                    set_count += 1
                    print("set list = " + str(set_list) + "\nset count = " + str(set_no))
                    continue
                if(string[i] in set_list):
                    set_list.append(string[j])
                    set_no.append(set_no[set_list.index(string[i])])
                    print("set list = " + str(set_list) + "\nset count = " + str(set_no))
                    continue
                if(string[j] in set_list):
                    set_list.append(string[i])
                    set_no.append(set_no[set_list.index(string[j])])
                    print("set list = " + str(set_list) + "\nset count = " + str(set_no))
                    continue


    for i in string:
        if i not in set_list:
            set_list.append(i)
            set_no.append(set_count)
            set_count += 1

    for i in range(0,set_count):
        t_list = [ h for h in set_list if set_no[set_list.index(h)]==(i+1)]
        print(t_list)
        t = "".join(t_list)
        if(len(t)!=0):
            ret_list.append(t)

    print("ret_list = " + str(ret_list))
    return ret_list




def minimized_dfa(dfa):

    global alph
    final_states = []
    non_final_states = []

    for i in range(0,dfa.shape[0]):
        if(dfa.iloc[i]['state type']=='I' or dfa.iloc[i]['state type']=='S'):
            final_states.append(dfa.iloc[i]['state id'])
        else:
            non_final_states.append(dfa.iloc[i]['state id'])
    print(final_states)
    print(non_final_states)

    state_list = ["".join(final_states) , "".join(non_final_states)]
    print(state_list)

    prev_list = []

    while(state_list != prev_list):
        temp_list = []
        for i in state_list:
            if(len(i)!=1):
                print(i)
                sl = check_equality(i,dfa,state_list)
                temp_list.extend(sl)

            else:
                print(i)
                temp_list.append(i)
        prev_list = state_list
        state_list = temp_list
        print(state_list)


    if(len(state_list)==dfa.shape[0]):
        return dfa

    for i in state_list:
        if(len(i)==1):
            continue
        else:
            ret_state = i[0]


            for k in alph:
                f = dfa.loc[dfa['state id']==ret_state][k]
                f = f.tolist()
                print(f)
                f = f[0]
                if(f in i):
                        dfa.loc[dfa['state id'] == ret_state,k] = ret_state
            for f in i:
                if(f!=ret_state):
                    ind = dfa.index[dfa['state id']==f]
                    dfa = dfa.drop(ind)

            for j in range(0,dfa.shape[0]):
                 for d in alph:
                    l = dfa.iloc[j][d]

                    if l in i and l != ret_state:
                        dfa.iloc[j][d] = ret_state
    print(dfa)





def postfix_eval(postfix):
    global alph
    stack=[]
    tos = -1
    for j in postfix:
        if(j.isalpha() or j=="*" or j=="$" or j=="0" or j=="1"):
            stack.append(j)
            tos+=1
        else:
            if(j=="."):
                rgt = stack.pop()
                lft = stack.pop()
                tos -= 2
                tf = concat(rgt,lft)
                t_key = tablemap_entry(tf)
                stack.append(t_key)
                tos += 1

            if(j=="+"):
                rgt = stack.pop()
                lft = stack.pop()
                tos -= 2
                tf = union(rgt,lft)
                t_key = tablemap_entry(tf)
                stack.append(t_key)
                tos += 1
            if(j=="^"):
                rgt = stack.pop()
                lft = stack.pop()
                tos -= 2
                tf = closure(rgt,lft)
                t_key = tablemap_entry(tf)
                stack.append(t_key)
                tos += 1

    t_key = stack.pop()
    tdf = tablemap_get_table(t_key)
    return tdf






alph = input("Enter the i/p alphabet set: ")
exp = input("enter the regular expression: ")
postfix = inf_to_post(exp)
print(postfix)
final_nfa_table = postfix_eval(postfix)
print(final_nfa_table)
dfa_table = nfa_to_dfa(final_nfa_table)
minimized_dfa(dfa_table)
