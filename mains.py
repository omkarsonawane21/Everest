import time
import mysql.connector
mydb = mysql.connector.connect(user='root', host='127.0.0.1', port=3306, password='#Sonawane@21', database='masaladb')
mycursor = mydb.cursor()


class node:
    def __init__(self, sc, amt, stk, mn, astk, bstk, sstk, aestk, bestk, sestk):
        self.stock_code = sc
        self.amount = amt
        self.stock = stk
        self.masala_name = mn
        self.aunstk = astk
        self.balstk = bstk
        self.sanstk = sstk
        self.aunexpstk = aestk
        self.balexpstk = bestk
        self.sanexpstk = sestk
        self.left = self.right = None


class r_node:
    def __init__(self, c, nm, add, cno, bill_amt, amt, ph, ap, pd, md, cash, rsa, esa, qty, rqty):
        self.code = c
        self.name = nm
        self.address = add
        self.contact_num = cno
        self.bill = bill_amt
        self.amount_paid = ap
        self.balance = amt
        self.previous_history = ph
        self.paid = pd
        self.mode = md
        self.cd = cash
        self.return_stk_amt = rsa
        self.expiry_stk_amt = esa
        self.quantity = qty
        self.return_qty = rqty
        self.left = self.right = None


def sortedArrayToBST(arr):
    if not arr:
        return None

    mid = (len(arr)) / 2
    mid = int(mid)
    root = node(arr[mid], 0.00, 0, "", 0, 0, 0, 0, 0, 0)
    root.left = sortedArrayToBST(arr[:mid])
    root.right = sortedArrayToBST(arr[mid + 1:])
    return root


def search(root, key):
    # Base Cases: root is null or key is present at root
    if root is None or root.stock_code == key:
        return root

    # Key is greater than root's key
    if root.stock_code < key:
        return search(root.right, key)

    # Key is smaller than root's key
    return search(root.left, key)


def inorder_insert():
    mycursor.execute("SELECT * FROM masala")
    myresult = mycursor.fetchall()
    mas_count = mycursor.rowcount

    arrayofmasalacode = []
    for masala_code in range(1, mas_count + 1):
        arrayofmasalacode.append(masala_code)

    root = sortedArrayToBST(arrayofmasalacode)

    if root is None:
        return None

    i = 0
    while i < mas_count:
        t = search(root, arrayofmasalacode[i])
        for x in myresult:
            if x[0] == getattr(t, 'stock_code'):
                setattr(t, 'stock_code', x[0])
                setattr(t, 'masala_name', x[1])
                setattr(t, 'amount', x[2])
                setattr(t, 'stock', x[3])
                setattr(t, 'aunstk', x[4])
                setattr(t, 'balstk', x[5])
                setattr(t, 'sanstk', x[6])
                setattr(t, 'aunexpstk', x[7])
                setattr(t, 'balexpstk', x[8])
                setattr(t, 'sanexpstk', x[9])
        i += 1
    return root


def masinorder(root, flag):
    current = root
    stack = []
    mas = ""
    global name

    if flag == 0:
        name = 'stock'
    elif flag == 1:
        name = 'aunstk'
    elif flag == 2:
        name = 'balstk'
    elif flag == 3:
        name = 'sanstk'

    while True:
        if current is not None:
            stack.append(current)
            current = current.left
        elif stack:
            node = stack.pop()
            if flag != 0 and getattr(node, name) != 0:
                mas = mas + "\n\nName : " + getattr(node, 'masala_name') + "\nStock : " + str(getattr(node, name)) + \
                      "     Total Amount : " + str(round(getattr(node, name) * getattr(node, 'amount'), 2))
            elif flag == 0:
                mas = mas + "\n\nName : " + getattr(node, 'masala_name') + "\nStock : " + str(getattr(node, name)) + "       Unit price : " + str(getattr(node, 'amount'))
            current = node.right
        else:
            break
    return mas


def masalasearch(root, x):
    if root is None:
        return None

    nodeStack = [root]
    searchstack = []

    j = len(x)
    match_flag = i = 0
    while len(nodeStack):
        node = nodeStack[0]

        while j > 0:
            if node.masala_name[i] is x[i] or ord(node.masala_name[i]) == ord(x[i]) - 32:

                match_flag = 1
                j -= 1
                i += 1

            else:
                match_flag = 0
                break

        if match_flag == 1:
            searchstack.append(nodeStack[0])

        nodeStack.pop(0)
        if node.right:
            nodeStack.append(node.right)
        if node.left:
            nodeStack.append(node.left)

        i = 0
        j = len(x)

    return searchstack


# button --- update
def update(root, mas, quantity):        # mas and quantity is received from textbox
    if root is None:
        return None

    nodeStack = [root]      # Create an empty stack for preorder traversal and append root to it
    # nodeStack.append(root)

    j = len(mas)  # length of the masala to be searched
    match_flag = i = 0  # flag and index set to 0
    # Do iterative preorder traversal to search x
    while len(nodeStack):  # loop until stack is not empty
        # See the top item from stack and check if it is same as x
        node = nodeStack[0]

        while j > 0:  # loop until length of masala
            if node.masala_name[i] == mas[i] or ord(node.masala_name[i]) == ord(mas[i]) - 32:
                match_flag = 1
            else:
                match_flag = 0
                break  # goes for further traversal
            j -= 1
            i += 1

        if match_flag == 1:             # mas is the complete name of masala & found then update and break loop
            setattr(nodeStack[0], 'stock', getattr(nodeStack[0], 'stock') + quantity)
            break

        nodeStack.pop(0)
        # append right and left children of the popped node to stack
        if node.right:
            nodeStack.append(node.right)
        if node.left:
            nodeStack.append(node.left)

        i = 0
        j = len(mas)


# button -- Save changes
def savechange(root):         # root is the masala tree

    current = root      # Set current to root of binary tree
    stack = []  # initialize stack

    while True:
        if current is not None:     # Reach the left most Node of the current Node
            stack.append(current)    # Place pointer to a tree node on the stack before traversing the node's left subtree
            current = current.left
        # BackTrack from the empty subtree and visit the Node at the top of the stack; however, if the stack is empty you are done
        elif stack:
            current = stack.pop(0)
            sql = "UPDATE masala SET stock = %s WHERE code = %s"            # updated in database
            val = (getattr(current, 'stock'), getattr(current, 'stock_code'))
            mycursor.execute(sql, val)
            mydb.commit()

            current = current.right     # We visited node and its left subtree. Now, it's right subtree's turn
        else:
            break


def sortedArrayToRST(arr):
    if not arr:
        return None
    mid = (len(arr)) / 2
    mid = int(mid)
    root = r_node(arr[mid], "", "", "", 0.00, 0.00, 0.00, 0.00, 1, "", 0.00, 0.00, 0.00, 0, 0)
    root.left = sortedArrayToRST(arr[:mid])
    root.right = sortedArrayToRST(arr[mid + 1:])
    return root


def ret_search(root, key):

    if root is None or root.code == key:
        return root

    if root.code < key:
        return ret_search(root.right, key)

    return ret_search(root.left, key)


def retsearch(root, retname):
    if root is None:
        return None

    nodestack = [root]
    searchstack = []

    j = len(retname)
    match_flag = i = 0

    while len(nodestack):
        node = nodestack[0]

        while j > 0:
            if node.name[i] == retname[i] or ord(node.name[i]) == ord(retname[i]) - 32:
                match_flag = 1
            else:
                match_flag = 0
                break
            j -= 1
            i += 1

        if match_flag == 1:
            searchstack.append(nodestack[0])

        nodestack.pop(0)
        if node.right:
            nodestack.append(node.right)
        if node.left:
            nodestack.append(node.left)

        i = 0
        j = len(retname)

    return searchstack


def retailer_inorder_insert(val):
    mycursor.execute("SELECT * FROM " + val)
    myresult = mycursor.fetchall()
    ret_count = mycursor.rowcount

    array_of_retailercode = []
    for retailer_code in range(1, ret_count + 1):
        array_of_retailercode.append(retailer_code)

    root = sortedArrayToRST(array_of_retailercode)

    if root is None:
        return None

    i = 0
    while i < ret_count:
        t = ret_search(root, array_of_retailercode[i])
        for x in myresult:
            if x[0] == getattr(t, 'code'):
                setattr(t, 'code', x[0])
                setattr(t, 'name', x[1])
                setattr(t, 'address', x[2])
                setattr(t, 'contact_num', x[3])
                setattr(t, 'bill', x[4])
                setattr(t, 'amount_paid', x[5])
                setattr(t, 'balance', x[6])
                setattr(t, 'previous_history', x[7])
                setattr(t, 'paid', x[8])
                setattr(t, 'mode', x[9])
                setattr(t, 'cd', x[10])
                setattr(t, 'return_stk_amt', x[11])
                setattr(t, 'expiry_stk-amt', x[12])
                setattr(t, 'quantity', x[13])
                setattr(t, 'ret_qty', x[14])
        i += 1
    return root


# flag = 1 => all retailers & 0 => pending retailers
def retinorder(root, flag):

    ret = ""
    if root is None:
        return ret
    stack = []
    current = root
    while True:
        if current is not None:
            stack.append(current)
            current = current.left
        elif stack:
            node = stack.pop()
            if getattr(node, 'paid') == 0 or flag:
                ret = ret + "\n\nName : " + getattr(node, 'name') + "\nContact : " + getattr(node,
                                                                                             'contact_num') + "\nAddress : " + getattr(
                    node, 'address') + "\nBill : " + str(round(getattr(node, 'bill'),2)) + "        Amount Paid :" + str(round(getattr(node,
                                                                                                               'amount_paid'),2)) + "\nBalance History : " + str(round(getattr(
                    node, 'balance'),2)) + "      Previous history : " + str(round(getattr(node, 'previous_history'),2))
            current = node.right
        else:
            break
    return ret


def transactions(root):
    Total = [0, 0, 0, 0, 0, 0, 0]
    if root is None:
        return Total
    stack = []
    current = root
    while True:
        if current is not None:
            stack.append(current)
            current = current.left
        elif stack:
            node = stack.pop()
            Total[0] += float(node[4])
            Total[1] += float(node[5])
            Total[2] += float(node[6])
            Total[3] += float(node[7])
            Total[4] += float(node[10])
            Total[5] += float(node[11])
            Total[6] += float(node[12])
            current = node.right
        else:
            break
    return Total


start = time.time()
mas_tree = inorder_insert()
aun_tree = retailer_inorder_insert("aundh")
bal_tree = retailer_inorder_insert("balewadi")
san_tree = retailer_inorder_insert("sangvi")
end = time.time()

print(end - start)