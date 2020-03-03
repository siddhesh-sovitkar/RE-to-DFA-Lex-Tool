# RE-to-DFA-Lex-Tool
A lex tool using python to convert regular expression to a minimized DFA.

sample i/p : 
Enter the i/p alphabet set: ab
enter the regular expression: (a+b)^*.a.b.b

o/p : (actual o/p produced by the code)
NFA table:
 state type State_id         E     b     a
0           S       q0      NULL    q1  NULL
1           S       q1        q5  NULL  NULL
2           S       q2      NULL  NULL    q3
3           S       q3        q5  NULL  NULL
4           S       q4  [q0, q2]  NULL  NULL
5           S       q5  [q7, q4]  NULL  NULL
6           I       q6  [q4, q7]  NULL  NULL
7           S       q7        q8  NULL  NULL
8           S       q8      NULL  NULL    q9
9           S       q9       q10  NULL  NULL
10          S      q10      NULL   q11  NULL
11          S      q11       q12  NULL  NULL
12          S      q12      NULL   q13  NULL
13          F      q13      NULL  NULL  NULL

DFA table:
 state type state id  a  b
0          I        A  B  C
1          S        B  B  D
2          S        C  B  C
3          S        D  B  E
4          F        E  B  C

Minimized DFA table:
 state type state id  a  b
0          I        A  B  A
1          S        B  B  D
3          S        D  B  E
4          F        E  B  A
