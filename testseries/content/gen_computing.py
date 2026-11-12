"""Programming and computer science. Code-output questions are answered by actually running the snippet; SQL ones by
running the query on an in-memory SQLite table; data-structure ones by simulating the structure."""
import contextlib
import io
import sqlite3

from .core import generator, mcq, near, numerical, register, table_topics

CSE, CMP = 'CSE1', 'CMP1'


def rows(block):
    return [tuple(x.strip() for x in line.split('|')) for line in block.strip().splitlines()]


def run_python(code):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(code, {'__builtins__': {'print': print, 'range': range, 'len': len, 'sum': sum, 'sorted': sorted, 'list': list,
                                     'str': str, 'int': int, 'max': max, 'min': min, 'set': set, 'dict': dict, 'abs': abs,
                                     'enumerate': enumerate, 'reversed': reversed, 'tuple': tuple, 'map': map}})
    return out.getvalue().strip()


def code_q(rng, lang, code, variants, difficulty, explanation):
    """MCQ 'What is the output?' – the correct option is the real output; wrong ones are outputs of near-miss variants."""
    answer = run_python(code) if lang == 'python' else code[1]
    shown = code if lang == 'python' else code[0]
    wrong = []
    for v in variants:
        try:
            wrong.append(run_python(v) if lang == 'python' else v)
        except Exception:
            wrong.append('Error')
    wrong += ['Error', 'None']
    return mcq(rng, f"What is the output of the following {lang.title() if lang != 'c' else 'C'} code?\n```\n{shown}\n```",
               answer, wrong, difficulty, explanation)


@generator('programming.python', CSE, 'Python Programming')
def python_output(rng):
    kind = rng.randrange(10)
    if kind == 0:
        n, a, b = rng.randint(5, 9), rng.randint(0, 3), rng.randint(4, 8)
        code = f"nums = list(range({n}))\nprint(nums[{a}:{b}])"
        return code_q(rng, 'python', code, [f"print(list(range({n}))[{a}:{b + 1}])", f"print(list(range({n}))[{a + 1}:{b}])",
                                            f"print(list(range(1, {n + 1}))[{a}:{b}])"], 'easy', "Slicing stops before the end index.")
    if kind == 1:
        n, step = rng.randint(5, 12), rng.choice([1, 2, 3])
        code = f"total = 0\nfor i in range(0, {n}, {step}):\n    total += i\nprint(total)"
        return code_q(rng, 'python', code, [f"print(sum(range(0, {n + 1}, {step})))", f"print(sum(range(1, {n}, {step})))", f"print({n})"],
                      'easy', f"Adds 0, {step}, {2 * step}, … below {n}.")
    if kind == 2:
        word = rng.choice(['banana', 'programming', 'mississippi', 'committee', 'balloon', 'success'])
        ch = rng.choice(sorted(set(word)))
        code = f"s = '{word}'\nprint(s.count('{ch}'), s.find('{ch}'))"
        return code_q(rng, 'python', code, [f"print('{word}'.count('{ch}') + 1, '{word}'.find('{ch}'))",
                                            f"print('{word}'.count('{ch}'), '{word}'.find('{ch}') + 1)",
                                            f"print('{word}'.count('{ch}'), '{word}'.rfind('{ch}'))"], 'medium',
                      "count() counts all occurrences; find() returns the first index (0-based).")
    if kind == 3:
        a, b = rng.randint(10, 50), rng.randint(3, 9)
        code = f"a, b = {a}, {b}\nprint(a // b, a % b)"
        return code_q(rng, 'python', code, [f"print({a} // {b} + 1, {a} % {b})", f"print({a} % {b}, {a} // {b})", f"print({a} // {b}, {b})"],
                      'easy', "// is floor division, % is the remainder.")
    if kind == 4:
        nums = rng.sample(range(1, 20), 5)
        code = f"nums = {nums}\nprint([x * 2 for x in nums if x % 2 == 0])"
        return code_q(rng, 'python', code, [f"print([x * 2 for x in {nums} if x % 2 == 1])", f"print([x for x in {nums} if x % 2 == 0])",
                                            f"print([x * 2 for x in {nums}])"], 'medium', "Keeps even numbers, then doubles them.")
    if kind == 5:
        k = rng.randint(2, 5)
        code = f"d = {{'a': 1, 'b': 2}}\nd['c'] = {k}\nd['a'] += {k}\nprint(len(d), d.get('z', 0), d['a'])"
        return code_q(rng, 'python', code, [f"print(2, 0, {k + 1})", f"print(3, None, {k + 1})", f"print(3, 0, {k})"], 'medium',
                      "Adding a new key grows the dict; get() returns the default for a missing key.")
    if kind == 6:
        n = rng.randint(3, 6)
        code = f"def f(n):\n    if n <= 1:\n        return 1\n    return n * f(n - 1)\nprint(f({n}))"
        return code_q(rng, 'python', code, [f"print({n} * {n - 1})", f"print({n} + {n - 1})", f"print({n} ** 2)"], 'medium',
                      f"Recursive factorial: {n}!.")
    if kind == 7:
        word = rng.choice(['python', 'django', 'indore', 'coding', 'binary'])
        code = f"s = '{word}'\nprint(s[::-1], s[1:3].upper())"
        return code_q(rng, 'python', code, [f"print('{word}', '{word}'[1:3].upper())", f"print('{word}'[::-1], '{word}'[0:3].upper())",
                                            f"print('{word}'[::-1], '{word}'[1:4].upper())"], 'easy', "[::-1] reverses; [1:3] takes indices 1 and 2.")
    if kind == 8:
        a, b = rng.sample(range(1, 9), 4), rng.sample(range(1, 9), 4)
        code = f"a = set({a})\nb = set({b})\nprint(len(a & b), len(a | b))"
        return code_q(rng, 'python', code, [f"print(len(set({a}) | set({b})), len(set({a}) & set({b})))", f"print(len(set({a}) - set({b})), len(set({a}) | set({b})))",
                                            f"print(len(set({a}) & set({b})), 8)"], 'medium', "& is intersection, | is union.")
    n = rng.randint(10, 40)
    code = f"x = {n}\ncount = 0\nwhile x > 1:\n    x = x // 2\n    count += 1\nprint(count)"
    return code_q(rng, 'python', code, ["print(0)", f"print({n} // 2)", f"print({n.bit_length()})"], 'medium', "Counts how many times x can be halved.")


@generator('programming.c', CSE, 'C Programming')
def c_output(rng):
    kind = rng.randrange(6)
    if kind == 0:
        a, b = rng.randint(10, 60), rng.randint(3, 9)
        code = (f"#include <stdio.h>\nint main() {{\n    int a = {a}, b = {b};\n    printf(\"%d %d\", a / b, a % b);\n    return 0;\n}}", f"{a // b} {a % b}")
        return code_q(rng, 'c', code, [f"{a / b:.2f} {a % b}", f"{a // b + 1} {a % b}", f"{a % b} {a // b}"], 'easy',
                      "Integer division truncates; % gives the remainder.")
    if kind == 1:
        n = rng.randint(4, 9)
        s = sum(range(1, n + 1))
        code = (f"#include <stdio.h>\nint main() {{\n    int i, s = 0;\n    for (i = 1; i <= {n}; i++)\n        s += i;\n    printf(\"%d\", s);\n    return 0;\n}}", str(s))
        return code_q(rng, 'c', code, [str(s - n), str(s + n + 1), str(n)], 'easy', f"1 + 2 + … + {n} = {s}.")
    if kind == 2:
        x = rng.randint(2, 9)
        code = (f"#include <stdio.h>\nint main() {{\n    int x = {x};\n    int y = x++;\n    int z = ++x;\n    printf(\"%d %d %d\", x, y, z);\n    return 0;\n}}",
                f"{x + 2} {x} {x + 2}")
        return code_q(rng, 'c', code, [f"{x + 2} {x + 1} {x + 2}", f"{x + 1} {x} {x + 1}", f"{x} {x} {x}"], 'medium',
                      "Post-increment returns the old value; pre-increment returns the new one.")
    if kind == 3:
        arr = rng.sample(range(1, 30), 5)
        i = rng.randrange(5)
        code = (f"#include <stdio.h>\nint main() {{\n    int a[] = {{{', '.join(map(str, arr))}}};\n    int *p = a;\n    printf(\"%d\", *(p + {i}));\n    return 0;\n}}",
                str(arr[i]))
        return code_q(rng, 'c', code, [str(arr[(i + 1) % 5]), str(arr[i] + i), str(i)], 'medium', f"*(p + {i}) is a[{i}].")
    if kind == 4:
        n = rng.choice([5, 6, 7, 8, 10, 12, 15])
        code = (f"#include <stdio.h>\nint main() {{\n    int n = {n};\n    printf(\"%d\", n & 1 ? 1 : 0);\n    return 0;\n}}", str(n & 1))
        return code_q(rng, 'c', code, [str(1 - (n & 1)), str(n), "2"], 'easy', "n & 1 is 1 for odd numbers.")
    n = rng.randint(3, 6)
    code = (f"#include <stdio.h>\nint main() {{\n    int i = 0;\n    while (i < {n}) {{\n        i += 2;\n    }}\n    printf(\"%d\", i);\n    return 0;\n}}",
            str(n + (n % 2)))
    return code_q(rng, 'c', code, [str(n), str(n + (n % 2) - 2), str(n + 2 + (n % 2))], 'easy', "The loop stops at the first even value ≥ n.")


@generator('programming.number_systems', CMP, 'Number Systems & Data Representation')
def number_systems(rng):
    kind = rng.randrange(5)
    n = rng.randint(10, 255)
    if kind == 0:
        return mcq(rng, f"The binary equivalent of decimal {n} is ___.", bin(n)[2:], [bin(x)[2:] for x in (n + 1, n - 1, n ^ 4, n + 8)], 'easy',
                   "Repeated division by 2.")
    if kind == 1:
        b = bin(n)[2:]
        return mcq(rng, f"The decimal value of binary {b} is ___.", str(n), [str(x) for x in (n + 1, n - 2, n ^ 8, n * 2)], 'easy', "Sum of powers of 2.")
    if kind == 2:
        return mcq(rng, f"The hexadecimal equivalent of decimal {n} is ___.", format(n, 'X'), [format(x, 'X') for x in (n + 1, n + 16, n - 1, n ^ 15)],
                   'medium', "Divide by 16.")
    if kind == 3:
        return mcq(rng, f"The octal equivalent of decimal {n} is ___.", format(n, 'o'), [format(x, 'o') for x in (n + 1, n + 8, n - 1, n * 2)],
                   'medium', "Divide by 8.")
    m = rng.randint(1, 127)
    tc = format((256 - m) & 0xFF, '08b')
    return mcq(rng, f"The 8-bit two's complement representation of −{m} is ___.", tc,
               [format(m, '08b'), format((255 - m) & 0xFF, '08b'), format((256 - m + 1) & 0xFF, '08b'), format(m | 128, '08b')], 'hard',
               "Invert the bits of +m and add 1.")


@generator('dsa.structures', CSE, 'Data Structures & Algorithms')
def structures(rng):
    kind = rng.randrange(6)
    if kind == 0:
        ops, stack, desc = [], [], []
        for _ in range(rng.randint(5, 8)):
            if stack and rng.random() < 0.4:
                stack.pop()
                desc.append("POP")
            else:
                v = rng.randint(1, 9)
                stack.append(v)
                desc.append(f"PUSH {v}")
        top = str(stack[-1]) if stack else 'Stack is empty'
        return mcq(rng, f"Starting with an empty stack, the operations are: {', '.join(desc)}. What is on top of the stack?", top,
                   [str(x) for x in range(1, 10) if str(x) != top][:6] + ['Stack is empty'], 'medium', "Simulate last-in, first-out.")
    if kind == 1:
        a, b, c = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 9)
        op1, op2 = rng.choice(['+', '*', '-']), rng.choice(['+', '*'])
        expr = f"{a} {b} {op1} {c} {op2}"
        val = eval(f"({a} {op1} {b}) {op2} {c}")
        return mcq(rng, f"Evaluate the postfix expression: {expr}", str(val), near(rng, val) + [str(eval(f"{a} {op1} ({b} {op2} {c})"))],
                   'medium', f"({a} {op1} {b}) {op2} {c} = {val}.")
    if kind == 2:
        keys = rng.sample(range(10, 99), 6)
        root = None

        def insert(node, k):
            if node is None:
                return [k, None, None]
            if k < node[0]:
                node[1] = insert(node[1], k)
            else:
                node[2] = insert(node[2], k)
            return node

        for k in keys:
            root = insert(root, k)

        def pre(n):
            return [] if n is None else [n[0]] + pre(n[1]) + pre(n[2])

        def post(n):
            return [] if n is None else post(n[1]) + post(n[2]) + [n[0]]

        order, fn = rng.choice([('preorder', pre), ('postorder', post)])
        ans = ' '.join(map(str, fn(root)))
        wrong = [' '.join(map(str, sorted(keys))), ' '.join(map(str, keys)), ' '.join(map(str, (pre if fn is post else post)(root))),
                 ' '.join(map(str, sorted(keys, reverse=True)))]
        return mcq(rng, f"The keys {', '.join(map(str, keys))} are inserted in this order into an empty binary search tree. What is its {order} traversal?",
                   ans, wrong, 'hard', "Build the BST, then traverse (inorder would simply be the sorted order).")
    if kind == 3:
        arr = rng.sample(range(1, 50), 6)
        a = arr[:]
        for j in range(len(a) - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
        ans = ' '.join(map(str, a))
        return mcq(rng, f"After the first pass of bubble sort (ascending) on [{', '.join(map(str, arr))}], the array is ___.", ans,
                   [' '.join(map(str, sorted(arr))), ' '.join(map(str, arr)), ' '.join(map(str, [min(arr)] + [x for x in arr if x != min(arr)]))],
                   'medium', "One pass bubbles the largest element to the end.")
    if kind == 4:
        h = rng.randint(2, 6)
        return mcq(rng, f"The maximum number of nodes in a binary tree of height {h} (root at height 0) is ___.", str(2 ** (h + 1) - 1),
                   [str(2 ** h), str(2 ** h - 1), str(2 ** (h + 1)), str(h * 2)], 'medium', "2^(h+1) − 1.")
    n = rng.randint(4, 12)
    return mcq(rng, f"The number of edges in a complete undirected graph with {n} vertices is ___.", str(n * (n - 1) // 2),
               [str(n * (n - 1)), str(n - 1), str(n * n), str(n * (n + 1) // 2)], 'easy', "n(n − 1)/2.")


@generator('dbms.sql', CSE, 'DBMS & SQL')
def sql(rng):
    names = ['Asha', 'Bilal', 'Chetan', 'Divya', 'Esha', 'Farhan', 'Gita', 'Harsh']
    depts = ['HR', 'IT', 'Sales']
    data = [(i + 1, n, rng.choice(depts), rng.randrange(20000, 90000, 5000)) for i, n in enumerate(rng.sample(names, 6))]
    db = sqlite3.connect(':memory:')
    db.execute("CREATE TABLE emp (id INTEGER, name TEXT, dept TEXT, salary INTEGER)")
    db.executemany("INSERT INTO emp VALUES (?, ?, ?, ?)", data)
    table = "id | name | dept | salary\n" + "\n".join(f"{i} | {n} | {d} | {s}" for i, n, d, s in data)
    d = rng.choice(depts)
    limit = rng.randrange(30000, 80000, 10000)
    queries = [
        (f"SELECT COUNT(*) FROM emp WHERE dept = '{d}';", 'Counts rows in that department.'),
        (f"SELECT COUNT(*) FROM emp WHERE salary > {limit};", 'Counts rows above the salary.'),
        (f"SELECT MAX(salary) FROM emp WHERE dept <> '{d}';", 'Highest salary outside that department.'),
        ("SELECT COUNT(DISTINCT dept) FROM emp;", 'Number of different departments.'),
        (f"SELECT SUM(salary) FROM emp WHERE dept = '{d}';", 'Total salary in that department.'),
    ]
    q, expl = rng.choice(queries)
    ans = db.execute(q).fetchone()[0]
    ans = 'NULL' if ans is None else str(ans)
    wrong = [str(x) for x in ({0, 1, 2, 3, 4, 5, 6} if 'COUNT' in q else {int(ans) + 5000 if ans != 'NULL' else 0, 90000, 20000, 150000}) if str(x) != ans]
    return mcq(rng, f"Table emp:\n{table}\n\nWhat does this query return?\n```\n{q}\n```", ans, wrong + ['NULL'], 'medium', expl)


@generator('digital.logic', CSE, 'Digital Logic & Boolean Algebra')
def logic(rng):
    a, b, c = rng.randint(0, 1), rng.randint(0, 1), rng.randint(0, 1)
    exprs = [
        ("(A AND B) OR C", (a & b) | c), ("NOT (A OR B)", 1 - (a | b)), ("A XOR B", a ^ b), ("(A OR B) AND NOT C", (a | b) & (1 - c)),
        ("A NAND B", 1 - (a & b)), ("(A XOR B) XOR C", a ^ b ^ c), ("A NOR C", 1 - (a | c)),
    ]
    e, v = rng.choice(exprs)
    return mcq(rng, f"For A = {a}, B = {b}, C = {c}, the value of {e} is ___.", str(v), [str(1 - v), 'Undefined', 'Both 0 and 1'], 'easy',
               "Evaluate inner operations first.")


COMPLEXITY = rows("""
Binary search on a sorted array|O(log n)
Linear search|O(n)
Bubble sort (worst case)|O(n²)
Merge sort (worst case)|O(n log n)
Quick sort (worst case)|O(n²)
Quick sort (average case)|O(n log n)
Heap sort (worst case)|O(n log n)
Insertion sort (best case)|O(n)
Accessing an array element by index|O(1)
Inserting at the head of a linked list|O(1)
Search in a balanced BST|O(log n)
BFS on a graph with V vertices and E edges|O(V + E)
Building a heap from n elements|O(n)
Floyd–Warshall all-pairs shortest path|O(V³)
""")
table_topics('dsa.complexity', CSE, 'Time Complexity', COMPLEXITY, [
    ("The time complexity of {a} is ___.", 'b', "{a}: {b}."),
], difficulty='medium')

CS_THEORY = [
    ("Which data structure is used for BFS traversal of a graph?", ['Queue', 'Stack', 'Heap', 'Tree'], 'easy', "BFS visits level by level using a FIFO queue."),
    ("Which data structure is used for recursion and DFS?", ['Stack', 'Queue', 'Deque', 'Hash table'], 'easy', "The call stack."),
    ("A deadlock requires all of mutual exclusion, hold and wait, no pre-emption and ___.", ['Circular wait', 'Starvation', 'Paging', 'Thrashing'], 'medium', "Coffman conditions."),
    ("Thrashing in an OS is caused by ___.", ['Excessive paging', 'Too many CPUs', 'Deadlock', 'Fast disks'], 'medium', "The system spends its time swapping pages."),
    ("Which scheduling algorithm can cause starvation?", ['Shortest Job First', 'Round Robin', 'FCFS', 'None'], 'medium', "Long jobs may wait forever."),
    ("Belady's anomaly occurs with ___ page replacement.", ['FIFO', 'LRU', 'Optimal', 'LFU'], 'hard', "More frames can cause more faults with FIFO."),
    ("A semaphore is used for ___.", ['Process synchronisation', 'Memory allocation', 'Disk scheduling', 'Compilation'], 'easy', "wait() and signal()."),
    ("Which normal form removes partial dependency?", ['2NF', '1NF', '3NF', 'BCNF'], 'medium', "Non-key attributes depend on the whole key."),
    ("Which normal form removes transitive dependency?", ['3NF', '2NF', '1NF', '4NF'], 'medium', "Non-key attributes depend only on the key."),
    ("ACID in databases stands for Atomicity, Consistency, Isolation and ___.", ['Durability', 'Dependency', 'Distribution', 'Data'], 'easy', "Committed data survives failures."),
    ("Which SQL command removes all rows but keeps the table structure?", ['TRUNCATE', 'DROP', 'DELETE TABLE', 'REMOVE'], 'medium', "DROP removes the table itself."),
    ("A primary key ___.", ['Must be unique and not NULL', 'Can be NULL', 'Can repeat', 'Must be numeric'], 'easy', "It identifies each row."),
    ("Which layer of the OSI model handles routing?", ['Network layer', 'Transport layer', 'Data link layer', 'Session layer'], 'easy', "Layer 3, IP."),
    ("TCP is a ___ protocol.", ['Connection-oriented', 'Connectionless', 'Physical-layer', 'Broadcast-only'], 'easy', "Reliable, ordered delivery."),
    ("The default port of HTTPS is ___.", ['443', '80', '21', '25'], 'easy', "HTTP uses 80."),
    ("Which protocol resolves IP addresses to MAC addresses?", ['ARP', 'DNS', 'DHCP', 'ICMP'], 'medium', "Address Resolution Protocol."),
    ("DNS translates ___.", ['Domain names to IP addresses', 'IP to MAC addresses', 'Emails to IP addresses', 'Ports to services'], 'easy', "Domain Name System."),
    ("How many bits are in an IPv4 address?", ['32', '64', '128', '16'], 'easy', "IPv6 uses 128."),
    ("In OOP, the ability of different classes to respond to the same method call differently is ___.", ['Polymorphism', 'Encapsulation', 'Inheritance', 'Abstraction'], 'easy', "Many forms."),
    ("Bundling data with the methods that operate on it is ___.", ['Encapsulation', 'Polymorphism', 'Inheritance', 'Overloading'], 'easy', "Data hiding."),
    ("Which of these is NOT a Java primitive type?", ['String', 'int', 'boolean', 'char'], 'easy', "String is a class."),
    ("In Java, which keyword prevents a class from being inherited?", ['final', 'static', 'abstract', 'private'], 'medium', "final class."),
    ("Which language feature lets a C function call itself?", ['Recursion', 'Iteration', 'Pointers', 'Macros'], 'easy', "Recursion."),
    ("The size of int in C is ___.", ['Implementation-defined (commonly 4 bytes)', 'Always 2 bytes', 'Always 8 bytes', '1 byte'], 'medium', "The standard only sets a minimum."),
    ("Which of these is an immutable type in Python?", ['tuple', 'list', 'dict', 'set'], 'easy', "Tuples cannot be changed after creation."),
    ("In Python, `len({1, 2, 2, 3})` returns ___.", ['3', '4', '2', 'Error'], 'easy', "Sets drop duplicates."),
    ("A compiler translates ___.", ['The whole program to machine code before running', 'One line at a time while running', 'Machine code to source', 'Only assembly'], 'easy', "An interpreter runs line by line."),
    ("Which is the first phase of a compiler?", ['Lexical analysis', 'Syntax analysis', 'Code generation', 'Optimisation'], 'medium', "Produces tokens."),
    ("The language accepted by a finite automaton is ___.", ['Regular', 'Context-free', 'Context-sensitive', 'Recursively enumerable'], 'medium', "DFA/NFA ↔ regular expressions."),
    ("A pushdown automaton accepts ___ languages.", ['Context-free', 'Regular only', 'Context-sensitive', 'All'], 'medium', "Finite automaton + stack."),
    ("Cache memory is placed between ___.", ['CPU and main memory', 'Main memory and disk', 'Disk and printer', 'Keyboard and CPU'], 'easy', "To speed up memory access."),
    ("Which memory is volatile?", ['RAM', 'ROM', 'Hard disk', 'Flash drive'], 'easy', "Loses data when power is off."),
    ("In the waterfall model, testing comes ___.", ['After implementation', 'Before design', 'Before requirements', 'In parallel with requirements'], 'easy', "Sequential phases."),
    ("Git command to create a copy of a remote repository is ___.", ['git clone', 'git init', 'git pull', 'git fork'], 'easy', "Copies the repo locally."),
    ("HTML stands for ___.", ['HyperText Markup Language', 'HighText Machine Language', 'Hyperlink Text Mode Language', 'Home Tool Markup Language'], 'easy', "Structure of web pages."),
    ("Which CSS property changes the text colour?", ['color', 'font-color', 'text-color', 'foreground'], 'easy', "color: red;"),
    ("In JavaScript, `typeof null` returns ___.", ['"object"', '"null"', '"undefined"', '"number"'], 'hard', "A long-standing quirk of the language."),
    ("Which HTTP method is normally used to submit a form that creates data?", ['POST', 'GET', 'HEAD', 'TRACE'], 'easy', "GET is for reading."),
]
register('cs.theory', CSE, 'Computer Science Fundamentals', rows=CS_THEORY)

COMPUTER_AWARENESS = [
    ("The brain of the computer is the ___.", ['CPU', 'RAM', 'Hard disk', 'Monitor'], 'easy', "Central Processing Unit."),
    ("1 kilobyte equals ___ bytes.", ['1024', '1000', '512', '2048'], 'easy', "2¹⁰ bytes."),
    ("Which of these is an input device?", ['Scanner', 'Monitor', 'Printer', 'Speaker'], 'easy', "It sends data into the computer."),
    ("Which of these is an output device?", ['Plotter', 'Keyboard', 'Mouse', 'Scanner'], 'easy', "It produces drawings."),
    ("Which of these is system software?", ['Operating system', 'MS Word', 'Photoshop', 'Chrome'], 'easy', "Manages hardware."),
    ("The shortcut to copy selected text in Windows is ___.", ['Ctrl + C', 'Ctrl + V', 'Ctrl + X', 'Ctrl + P'], 'easy', "Ctrl + V pastes."),
    ("The shortcut to undo the last action is ___.", ['Ctrl + Z', 'Ctrl + Y', 'Ctrl + U', 'Ctrl + A'], 'easy', "Ctrl + Y redoes."),
    ("In MS Excel, a formula always begins with ___.", ['=', '+', '#', '@'], 'easy', "e.g. =SUM(A1:A5)."),
    ("In MS Excel, the intersection of a row and a column is a ___.", ['Cell', 'Range', 'Sheet', 'Field'], 'easy', "Named like B3."),
    ("Which function in Excel returns the largest value?", ['MAX()', 'LARGE()', 'TOP()', 'HIGH()'], 'medium', "LARGE() returns the k-th largest."),
    ("A virus that disguises itself as useful software is a ___.", ['Trojan horse', 'Worm', 'Spyware', 'Adware'], 'easy', "It does not self-replicate."),
    ("Phishing is ___.", ['Tricking users into revealing personal information', 'A type of firewall', 'Data compression', 'A backup method'], 'easy', "Usually by fake emails or sites."),
    ("Which of these is a web browser?", ['Firefox', 'Windows', 'Excel', 'Oracle'], 'easy', "Browsers display web pages."),
    ("URL stands for ___.", ['Uniform Resource Locator', 'Universal Resource Link', 'Uniform Reference Locator', 'Unique Resource Locator'], 'easy', "A web address."),
    ("Which of these is a search engine?", ['Google', 'Facebook', 'WhatsApp', 'Linux'], 'easy', "Bing and DuckDuckGo are others."),
    ("Email attachments are sent using the ___ protocol.", ['SMTP', 'FTP', 'HTTP', 'POP3 only'], 'medium', "Simple Mail Transfer Protocol sends mail."),
    ("The first page of a website is the ___.", ['Home page', 'Index card', 'Landing slide', 'Cookie'], 'easy', "Home page."),
    ("Which generation of computers used transistors?", ['Second', 'First', 'Third', 'Fourth'], 'medium', "First: vacuum tubes; third: ICs."),
    ("The father of the computer is ___.", ['Charles Babbage', 'Alan Turing', 'John von Neumann', 'Bill Gates'], 'easy', "Designed the Analytical Engine."),
    ("Which storage device has the largest capacity typically?", ['Hard disk', 'CD', 'DVD', 'Floppy disk'], 'easy', "Terabytes."),
    ("BIOS is stored in ___.", ['ROM (firmware)', 'RAM', 'Hard disk', 'Cache'], 'medium', "Runs at start-up."),
    ("A LAN covers ___.", ['A small area such as a building', 'A country', 'The whole world', 'A city only'], 'easy', "Local Area Network."),
    ("Which device connects different networks and forwards packets?", ['Router', 'Hub', 'Repeater', 'Modem only'], 'easy', "Works at the network layer."),
    ("In MS Word, Ctrl + B is used to ___.", ['Make text bold', 'Open a new document', 'Print', 'Bookmark'], 'easy', "Bold."),
    ("Which file extension is used for a PowerPoint presentation?", ['.pptx', '.docx', '.xlsx', '.pdf'], 'easy', "Microsoft PowerPoint."),
    ("Cloud computing means ___.", ['Using computing resources over the internet', 'Weather forecasting by computers', 'Storing data only on a pen drive', 'Wireless printing'], 'easy', "On-demand remote resources."),
    ("An IP address of the form 192.168.x.x is a ___ address.", ['Private', 'Public', 'Broadcast', 'Loopback'], 'medium', "Reserved for private networks."),
    ("Which key is used to refresh a web page?", ['F5', 'F1', 'F12', 'Esc'], 'easy', "F1 is help."),
]
register('cs.awareness', CMP, 'Computer Awareness', rows=COMPUTER_AWARENESS)


def _code_numeric(rng):
    n = rng.randint(4, 12)
    return numerical(f"What does this Python code print?\n```\ntotal = 0\nfor i in range(1, {n} + 1):\n    if i % 2 == 0:\n        total += i\nprint(total)\n```",
                     sum(i for i in range(1, n + 1) if i % 2 == 0), 'medium', "Sum of the even numbers up to n.")


register('programming.python', CSE, '', numeric=_code_numeric)
