import wx

app = wx.App(False)
d = {}


def wMouseDown(e):
    print("!!!", e.GetEventObject())


def MouseDown(e):
    o = e.GetEventObject()
    sx, sy = panel.ScreenToClient(o.GetPositionTuple())
    dx, dy = panel.ScreenToClient(wx.GetMousePosition())
    o._x, o._y = (sx - dx, sy - dy)
    d['d'] = o


def MouseMove(e):
    try:
        if 'd' in d:
            o = d['d']
            x, y = wx.GetMousePosition()
            o.SetPosition(wx.Point(x + o._x, y + o._y))
    except e:
        pass


def MouseUp(e):
    try:
        if 'd' in d:
            del d['d']
    except e:
        pass


frame = wx.Frame(None, -1, 'simple.py')
panel = wx.Panel(frame)
box = wx.BoxSizer(wx.VERTICAL)
button1 = wx.Button(panel, -1, "foo")
box.Add(button1, 0, wx.ALL, 10)
button2 = wx.Button(panel, -1, "bar")
box.Add(button2, 0, wx.ALL, 10)

button1.Bind(wx.EVT_LEFT_DOWN, MouseDown)
button2.Bind(wx.EVT_LEFT_DOWN, MouseDown)

button1.Bind(wx.EVT_MOTION, MouseMove)
button2.Bind(wx.EVT_MOTION, MouseMove)

button1.Bind(wx.EVT_LEFT_UP, MouseUp)
button2.Bind(wx.EVT_LEFT_UP, MouseUp)

panel.Bind(wx.EVT_MOTION, MouseMove)
panel.Bind(wx.EVT_LEFT_UP, MouseUp)

panel.SetSizer(box)
panel.Layout()
frame.Show()

app.MainLoop()
