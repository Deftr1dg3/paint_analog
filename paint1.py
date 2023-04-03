#!/usr/bin/env python3

import wx


class Up_Menu(wx.MenuBar):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)


class Frame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.SetSize((800, 528))
        self.SetTitle('Paint')
        self.SetMenuBar(Up_Menu())

        self.SetBackgroundColour(wx.Colour(32, 32, 32, 1))

        self.InitOptions()
        self.InitDispaly()

    def InitOptions(self):

        self.panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # ...............Options.................................................

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.options_panel = wx.Panel(self.panel)
        self.options_panel.SetBackgroundColour('#323232')

        hbox_options = wx.BoxSizer(wx.HORIZONTAL)

        self.colours_to_choose = ['Black', 'White', 'Green', 'Red', 'Blue', 'Yellow', 'Orange',
                                  'Purple', 'Default', 'Transparent']

        txt1 = wx.StaticText(self.options_panel, label='Background:')
        hbox_options.Add(txt1, flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10)

        self.background_colours = wx.ComboBox(self.options_panel,
                                              choices=self.colours_to_choose, style=wx.CB_READONLY)
        self.background_colours.SetValue('Default')
        hbox_options.Add(self.background_colours, 0, wx.LEFT | wx.TOP, 7)

        txt2 = wx.StaticText(self.options_panel, label='Pen:')
        hbox_options.Add(txt2, flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10)

        self.pen_colours = wx.ComboBox(self.options_panel,
                                       choices=self.colours_to_choose, style=wx.CB_READONLY)
        hbox_options.Add(self.pen_colours, 0, wx.LEFT | wx.TOP, 7)

        txt3 = wx.StaticText(self.options_panel, label='Size:')
        hbox_options.Add(txt3, flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10)

        self.pen_sizes = wx.ComboBox(self.options_panel,
                                     choices=[str(i) for i in range(1, 31)], style=wx.CB_READONLY)
        self.pen_sizes.SetValue('4')
        hbox_options.Add(self.pen_sizes, 0, wx.LEFT | wx.TOP, 7)

        self.draw = wx.RadioButton(self.options_panel, label='Draw')
        self.draw.SetValue(True)
        hbox_options.Add(self.draw, 0, wx.LEFT | wx.TOP, 10)

        self.eraise = wx.RadioButton(self.options_panel, label='Eraise')
        hbox_options.Add(self.eraise, 0, wx.LEFT | wx.TOP, 10)

        self.options_panel.SetSizer(hbox_options)

        hbox1.Add(self.options_panel, 1, flag=wx.EXPAND)

        vbox.Add(hbox1, 0, wx.EXPAND)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        self.display = wx.Panel(self.panel)

        hbox2.Add(self.display, 1, wx.EXPAND)

        vbox.Add(hbox2, 1, wx.EXPAND)

        self.panel.SetSizer(vbox)

    # ..............Display...............................................

    def InitDispaly(self):

        self.display.SetFocus()

        self.background = self.background_colours.GetStringSelection()
        self.pen_colour = self.pen_colours.GetStringSelection()
        self.pen_size = int(self.pen_sizes.GetStringSelection())

        self.drawn = []
        self.drawn_temp = []

        self.point_ind = 0
        self.point_coords = ()
        self.drawn_points = []

        self.background_dafault_colour = '#323232'

        self.display.SetBackgroundColour(self.background_dafault_colour)

        self.back_colours = {
            'Black': 'Black',
            'White': '#E1DFDF',
            'Green': '#2CA31E',
            'Red': '#CF4131',
            'Blue': '#343CA6',
            'Yellow': '#C4AD1A',
            'Orange': '#E2A923',
            'Purple': '#70236E',
            'Default': self.background_dafault_colour,
            'Transparent': wx.Colour(32, 32, 32, 1)
        }

        self.display.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.display.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

        self.display.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        self.Bind(wx.EVT_COMBOBOX, self.OnCombo)

        self.display.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton)

        self.display.Bind(wx.EVT_PAINT, self.OnPaint)

        self.display.Bind(wx.EVT_MOTION, self.OnMotion)

    def OnPaint(self, e):

        dc = wx.PaintDC(self.display)

        if self.drawn_points:
            for row in self.drawn_points:
                self.drawPoint(dc, row[2], row[0], row[1])

        if self.point_ind:
            x, y = self.point_coords
            self.drawPoint(dc, (x, y), self.pen_colour, self.pen_size)
            self.drawn_points += [[self.pen_colour, self.pen_size, (x, y)]]
            self.point_ind = 0

        if self.drawn:
            for row in self.drawn:
                for index in range(len(row[2][:-1])):
                    self.drawLine(dc, row[2][index], row[2][index + 1],
                                  row[0], row[1])

        if self.drawn_temp:
            for index in range(len(self.drawn_temp[:-1])):
                self.drawLine(dc, self.drawn_temp[index], self.drawn_temp[index + 1],
                              self.pen_colour, self.pen_size)

    def drawLine(self, dc, coords1, coords2, pen_colour, pen_size):

        x, y = coords1
        x1, y1 = coords2
        dc.SetPen(wx.Pen(pen_colour, pen_size))
        dc.DrawLine(x, y, x1, y1)
        self.Refresh()

    def drawPoint(self, dc, coords, pen_colour, pen_size):

        x, y = coords
        dc.SetPen(wx.Pen(pen_colour, pen_size))
        dc.DrawLine(x, y, x, y)
        self.Refresh()

    def OnMotion(self, e):

        if e.LeftIsDown():
            x, y = e.GetPosition()
            self.drawn_temp += [(x, y)]
        self.Refresh()

    def OnLeftDown(self, e):

        self.point_coords = e.GetPosition()
        self.point_ind = 1
        self.Refresh()

    def OnLeftUp(self, e):

        self.drawn += [[self.pen_colour, self.pen_size, self.drawn_temp]]
        self.drawn_temp = []

    def OnRightDown(self, e):
        self.Undo()

    def OnKeyDown(self, e):
        keycode = chr(e.GetKeyCode())
        if keycode == 'Z':
            self.Undo()
        elif keycode == 'C':
            self.Clear()

    def OnCombo(self, e):

        self.background = self.background_colours.GetStringSelection()
        self.pen_colour = self.pen_colours.GetStringSelection()
        self.pen_size = int(self.pen_sizes.GetStringSelection())

        self.display.SetBackgroundColour(self.back_colours[self.background])

        self.Refresh()

    def OnRadioButton(self, e):

        if self.draw.GetValue():
            self.pen_colour = self.pen_colours.GetStringSelection()
            self.pen_size = int(self.pen_sizes.GetStringSelection())
        else:
            self.OnEraiser()

    def Undo(self):
        if self.drawn:
            del self.drawn[-1]
        if self.drawn_points:
            del self.drawn_points[-1]
        self.Refresh()

    def Clear(self):
        self.drawn = []
        self.drawn_points = []
        self.Refresh()

    def OnEraiser(self):
        self.pen_colour = self.back_colours[self.background]
        self.pen_size = 30


# ----------------------------Launch the App--------------------------------------------------------

def main():
    app = wx.App()
    Frame(None).Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
