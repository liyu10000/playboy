import wx

class Calculator(wx.Frame):
    def __init__(self, parent, title):
        super(Calculator, self).__init__(parent, title=title)
        self.InitUI()
        self.Centre()

    def InitUI(self):
        self.expression = ""
        self.restart = False

        self.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL, False,'Times New Roman'))

        # # add dropdown menu
        # menubar = wx.MenuBar()
        # fileMenu = wx.Menu()
        # fileMenu.Append(wx.ID_OPEN, "&Open")
        # fileMenu.Append(wx.ID_SAVE, "&Save")
        # menubar.Append(fileMenu, "&File")
        # self.SetMenuBar(menubar)

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.display = wx.TextCtrl(self, style=wx.TE_RIGHT)
        vbox.Add(self.display, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=1)
        gs = wx.GridSizer(5, 4, 0, 0)
        gs.AddMany( [(wx.Button(self, id=11, label='('), 0, wx.EXPAND),
            (wx.Button(self, id=12, label=')'), 0, wx.EXPAND),
            (wx.Button(self, id=18, label='Delete'), 0, wx.EXPAND),
            (wx.Button(self, id=19, label='Clear'), 0, wx.EXPAND),
            (wx.Button(self, id=7, label='7'), 0, wx.EXPAND),
            (wx.Button(self, id=8, label='8'), 0, wx.EXPAND),
            (wx.Button(self, id=9, label='9'), 0, wx.EXPAND),
            (wx.Button(self, id=16, label='/'), 0, wx.EXPAND),
            (wx.Button(self, id=4, label='4'), 0, wx.EXPAND),
            (wx.Button(self, id=5, label='5'), 0, wx.EXPAND),
            (wx.Button(self, id=6, label='6'), 0, wx.EXPAND),
            (wx.Button(self, id=15, label='*'), 0, wx.EXPAND),
            (wx.Button(self, id=1, label='1'), 0, wx.EXPAND),
            (wx.Button(self, id=2, label='2'), 0, wx.EXPAND),
            (wx.Button(self, id=3, label='3'), 0, wx.EXPAND),
            (wx.Button(self, id=14, label='-'), 0, wx.EXPAND),
            (wx.Button(self, id=0, label='0'), 0, wx.EXPAND),
            (wx.Button(self, id=10, label='.'), 0, wx.EXPAND),
            (wx.Button(self, id=17, label='='), 0, wx.EXPAND),
            (wx.Button(self, id=13, label='+'), 0, wx.EXPAND) ])
        vbox.Add(gs, proportion=1, flag=wx.EXPAND)
        self.SetSizer(vbox)
        
        self.Bind(wx.EVT_BUTTON, self.OnClick)

    def OnClick(self, event):
        pattern = "0123456789.()+-*/="
        if self.restart or event.Id == 19:
            self.expression = ""
            self.display.SetValue(self.expression)
            self.restart = False
        self.expression = self.display.GetValue()
        if event.Id in range(0, 17):
            self.expression += pattern[event.Id]
        elif event.Id == 17:
            result = calculate(self.expression)
            self.expression += "=" + str(result)
            self.restart = True
        elif event.Id == 18:
            self.expression = self.expression[:-1] 
        self.display.SetValue(self.expression)

def calculate(expression):
    """
        expression: "-23.4*(2+4.3/1.2)"
        return: float result or [!]
    """
    # read expression string into operators and values
    tokens = []
    value = ""
    for char in expression:
        if char in "+-" and not value:
            value = char
        elif char in ".0123456789":
            value += char
        elif char.isspace():
            continue
        else:
            if value:
                tokens.append(float(value))
                value = ""
            tokens.append(char)
    if value:
        tokens.append(float(value))
    
    def is_prior(op1, op2):
        if op1 in "*/":
            return True
        if op1 in "+-" and op2 in "+-":
            return True
        return False

    def binary_op(ops_stack, val_stack):
        op = ops_stack.pop()
        val2 = val_stack.pop()
        val1 = val_stack.pop()
        if op == "+":
            val = val1 + val2
        elif op == "-":
            val = val1 - val2
        elif op == "*":
            val = val1 * val2
        elif op == "/":
            val = val1 / val2
        val_stack.append(val)

    try:
        ops_stack = []
        val_stack = []
        for token in tokens:
            if token == "(":
                ops_stack.append(token)
            elif str(token) in "+-*/":
                while ops_stack and is_prior(ops_stack[-1], token):
                    binary_op(ops_stack, val_stack)
                ops_stack.append(token)
            elif token == ")":
                while ops_stack[-1] != "(":
                    binary_op(ops_stack, val_stack)
                ops_stack.pop()
            else:
                val_stack.append(token)
        while ops_stack:
            binary_op(ops_stack, val_stack)
        result = val_stack.pop()
        if result.is_integer():
            result = int(result)
        return result
    except:
        return "[!]"

def main():
    app = wx.App()
    calculator = Calculator(None, title="calculator")
    calculator.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
    # expression = "-23.4 * (1 / (1*4.3 - 1.2))  "
    # print(calculate(expression))