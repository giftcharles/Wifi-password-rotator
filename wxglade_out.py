#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.1 on Wed Mar 20 12:04:36 2019
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

class MyDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((300, 250))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.SetTitle("About")
        self.SetSize((300, 250))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        bitmap_1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap("C:\\Users\\gift\\Desktop\\Wifi password changer\\GUI\\bitmaps\\icon.png", wx.BITMAP_TYPE_ANY))
        sizer_8.Add(bitmap_1, 0, wx.ALIGN_CENTER | wx.BOTTOM | wx.TOP, 12)
        label_3 = wx.StaticText(self, wx.ID_ANY, "Hii Application imetegenezwa na _______.\nv0.1\nKwa mawasiliano piga 0629495961", style=wx.ALIGN_CENTER)
        sizer_8.Add(label_3, 0, wx.ALIGN_CENTER, 0)
        self.SetSizer(sizer_8)
        self.Layout()
        # end wxGlade

# end of class MyDialog


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):

        # variables 
        self.Carriers = ["Vodacom", "Airtel", "Zantel", "TTCL", "Tigo", "Halotel"]
        self.HourMinutesList = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00"]
        self.DayNightList = ["AM", "PM"]

        try:
            current_config = self.__load_pickled_data()
            if current_config == []:
                raise
        except:
            current_config = [
                {"EXTRA_EMAILS": []},
                {"REGISTRY": ''},
                {"_PASSWORD_PREFIX": ''},
                {"_GMAIL_USER": ''},
                {"_GMAIL_USER_PASS": ''},
                {"SSID": ''},
                {"WaitAfterEmail": 120},
                {"CARRIER": 'TTCL'},
                {"HOST_ADDRESS": ''},
                {"HOST_USERNAME": 'admin'},
                {"HOST_PASSWORD": ''},
                {"SERVICE_ACCOUNT_CREDENTIALS": ''},
                {"HourMinute": "00:00", "DayNight": "AM"}
            ]
            
        print(current_config)
        self.carrierIndexInList = self.Carriers.index(current_config[7]['CARRIER'])
        self.WaitAfterEmail = current_config[6]['WaitAfterEmail']
        self.HourMinuteChoice = self.HourMinutesList.index(current_config[12]['HourMinute'])
        self.DayNightChoice = self.DayNightList.index(current_config[12]['DayNight'])
        self.HostAdrressField = current_config[8]['HOST_ADDRESS'].replace('http://', '')
        self.SSID = current_config[5]['SSID']
        self.HostUsername = current_config[9]['HOST_USERNAME']
        self.HostPassword = current_config[10]['HOST_PASSWORD']
        self.SenderEmailAddress = current_config[3]['_GMAIL_USER']
        self.SenderEmailAccountPassword = current_config[4]['_GMAIL_USER_PASS']
        self.SheetName = current_config[1]['REGISTRY']
        self.seviceAccountCreds = current_config[11]['SERVICE_ACCOUNT_CREDENTIALS']
        self.defaultEmailList = current_config[0]['EXTRA_EMAILS']

        with open('logs.log', 'r') as f:
            self.logs = f.read()
        print()


        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.CAPTION | wx.CLIP_CHILDREN | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((600, 600))
        
        # Menu Bar
        self.frame_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "&Save", "Save the settings")
        self.Bind(wx.EVT_MENU, self.OnSaveButton, id=item.GetId())
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(wx.ID_EXIT, "E&xit", "Close the program")
        self.Bind(wx.EVT_MENU, self.OnCancelButton, id=wx.ID_EXIT)
        self.frame_menubar.Append(wxglade_tmp_menu, "&File")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.ID_HELP, "Manual", "Show the application manual")
        self.Bind(wx.EVT_MENU, self.onShowManual, id=wx.ID_HELP)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(wx.ID_ABOUT, "About", "show the about dialog")
        self.frame_menubar.Append(wxglade_tmp_menu, "&Help")
        self.SetMenuBar(self.frame_menubar)
        # Menu Bar end
        self.frame_statusbar = self.CreateStatusBar(1)
        
        # Tool Bar
        self.frame_toolbar = wx.ToolBar(self, -1)
        self.SetToolBar(self.frame_toolbar)
        self.frame_toolbar.AddTool(wx.ID_SAVE, "Save", wx.Bitmap("C:\\Users\\gift\\Desktop\\Wifi password changer\\GUI\\bitmaps\\save-32.png", wx.BITMAP_TYPE_ANY), wx.Bitmap("C:\\Users\\gift\\Desktop\\Wifi password changer\\GUI\\bitmaps\\save-32.png", wx.BITMAP_TYPE_ANY), wx.ITEM_NORMAL, "Save the current settings", "")
        self.frame_toolbar.AddTool(1324, "Run", wx.Bitmap("C:\\Users\\gift\\Desktop\\Wifi password changer\\GUI\\bitmaps\\start-green-play-icon-1.png", wx.BITMAP_TYPE_ANY), wx.Bitmap("C:\\Users\\gift\\Desktop\\Wifi password changer\\GUI\\bitmaps\\start-green-play-icon-1.png", wx.BITMAP_TYPE_ANY), wx.ITEM_NORMAL, "Run the wifi rotater prrogram", "")
        self.frame_toolbar.AddTool(7685, "Stop", wx.Bitmap("C:\\Users\\gift\\Desktop\\Wifi password changer\\GUI\\bitmaps\\iconfinder_lowercase_letter_x_red_3052270.png", wx.BITMAP_TYPE_ANY), wx.Bitmap("C:\\Users\\gift\\Desktop\\Wifi password changer\\GUI\\bitmaps\\iconfinder_lowercase_letter_x_red_3052270.png", wx.BITMAP_TYPE_ANY), wx.ITEM_NORMAL, "Stop Wifi Rotater Execution", "")
        self.frame_toolbar.AddSeparator()
        self.frame_toolbar.AddTool(wx.ID_ABOUT, "About", wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_OTHER, (32, 32)), wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_OTHER, (32, 32)), wx.ITEM_NORMAL, "show the about dialogue", "")
        # Tool Bar end
        self.notebook_1 = wx.Notebook(self, wx.ID_ANY, style=wx.NB_FIXEDWIDTH | wx.NB_FLAT | wx.NB_TOP)
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.radio_box_1 = wx.RadioBox(self.notebook_1_pane_2, wx.ID_ANY, "Carrier", choices=self.Carriers, majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.slider_1 = wx.Slider(self.notebook_1_pane_2, wx.ID_ANY, self.WaitAfterEmail, 0, 720, style=wx.SL_HORIZONTAL | wx.SL_LABELS | wx.SL_SELRANGE)
        self.choice_1 = wx.Choice(self.notebook_1_pane_2, wx.ID_ANY, choices=self.HourMinutesList)
        self.choice_2 = wx.Choice(self.notebook_1_pane_2, wx.ID_ANY, choices=self.DayNightList)
        self.ntoebook_1_pane_3 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.text_ctrl_6 = wx.TextCtrl(self.ntoebook_1_pane_3, wx.ID_ANY, "")
        self.text_ctrl_11 = wx.TextCtrl(self.ntoebook_1_pane_3, wx.ID_ANY, "")
        self.text_ctrl_10 = wx.TextCtrl(self.ntoebook_1_pane_3, wx.ID_ANY, "")
        self.text_ctrl_8 = wx.TextCtrl(self.ntoebook_1_pane_3, wx.ID_ANY, "", style=wx.TE_PASSWORD)
        self.notebook_1_pane_4 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.text_ctrl_1 = wx.TextCtrl(self.notebook_1_pane_4, wx.ID_ANY, "", style=wx.TE_AUTO_URL | wx.TE_MULTILINE | wx.TE_RICH | wx.TE_RICH2 | wx.TE_WORDWRAP)
        self.text_ctrl_9 = wx.TextCtrl(self.notebook_1_pane_4, wx.ID_ANY, "")
        self.text_ctrl_3 = wx.TextCtrl(self.notebook_1_pane_4, wx.ID_ANY, "")
        self.notebook_1_pane_6 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.text_ctrl_5 = wx.TextCtrl(self.notebook_1_pane_6, wx.ID_ANY, "")
        self.text_ctrl_7 = wx.TextCtrl(self.notebook_1_pane_6, wx.ID_ANY, "", style=wx.TE_PASSWORD)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.text_ctrl_2 = wx.TextCtrl(self.notebook_1_pane_1, wx.ID_ANY, "", style=wx.TE_AUTO_URL | wx.TE_MULTILINE | wx.TE_RICH | wx.TE_RICH2 | wx.TE_WORDWRAP)
        self.button_1 = wx.Button(self, wx.ID_SAVE, "")
        self.button_2 = wx.Button(self, wx.ID_CANCEL, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TOOL, self.OnSaveButton, id=wx.ID_SAVE)
        self.Bind(wx.EVT_TOOL, self.RunTrayIcon, id=1324)
        self.Bind(wx.EVT_TOOL, self.shutdownTrayIcon, id=7685)
        self.Bind(wx.EVT_TOOL, self.onAboutShow, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_BUTTON, self.OnSaveButton, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.OnCancelButton, self.button_2)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Wifi Password Rotater")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("C:\\Users\\gift\\Desktop\\Wifi password changer\\GUI\\bitmaps\\icon.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        self.frame_statusbar.SetStatusWidths([-1])
        
        # statusbar fields
        frame_statusbar_fields = ["statusbar"]
        for i in range(len(frame_statusbar_fields)):
            self.frame_statusbar.SetStatusText(frame_statusbar_fields[i], i)
        self.frame_toolbar.Realize()
        self.radio_box_1.SetSelection(self.carrierIndexInList)
        self.choice_1.SetSelection(self.HourMinuteChoice)
        self.choice_2.SetSelection(self.DayNightChoice)
        self.text_ctrl_1.SetToolTip("Email zisizobadilika za watu watakaoipata password ")
        self.text_ctrl_1.SetFocus()
        self.text_ctrl_2.SetToolTip("Email zisizobadilika za watu watakaoipata password ")
        self.text_ctrl_2.Enable(False)
        self.text_ctrl_6.write(self.HostAdrressField)
        self.text_ctrl_11.write(self.SSID)
        self.text_ctrl_10.write(self.HostUsername)
        self.text_ctrl_8.write(self.HostPassword)
        self.text_ctrl_5.write(self.SenderEmailAddress)
        self.text_ctrl_7.write(self.SenderEmailAccountPassword)
        self.text_ctrl_2.write(self.logs)
        for email in self.defaultEmailList:
            self.text_ctrl_1.write(email + '\n')
        self.text_ctrl_9.write(self.SheetName)
        self.text_ctrl_3.write(self.seviceAccountCreds)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(1, 2, 0, 9)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_2 = wx.FlexGridSizer(2, 2, 4, 4)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_3 = wx.FlexGridSizer(2, 2, 3, 0)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_4 = wx.FlexGridSizer(4, 2, 4, 4)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.radio_box_1, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 12)
        label_2 = wx.StaticText(self.notebook_1_pane_2, wx.ID_ANY, "Wait time(seconds): ")
        sizer_2.Add(label_2, 0, wx.LEFT | wx.RIGHT | wx.TOP, 12)
        sizer_2.Add(self.slider_1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 12)
        static_line_1 = wx.StaticLine(self.notebook_1_pane_2, wx.ID_ANY)
        sizer_2.Add(static_line_1, 0, wx.BOTTOM | wx.EXPAND | wx.TOP, 12)
        label_1 = wx.StaticText(self.notebook_1_pane_2, wx.ID_ANY, "Run time: ")
        sizer_4.Add(label_1, 0, wx.RIGHT | wx.TOP, 4)
        sizer_4.Add(self.choice_1, 0, 0, 0)
        sizer_4.Add(self.choice_2, 0, 0, 0)
        sizer_2.Add(sizer_4, 1, wx.ALL | wx.EXPAND, 12)
        self.notebook_1_pane_2.SetSizer(sizer_2)
        label_6 = wx.StaticText(self.ntoebook_1_pane_3, wx.ID_ANY, "Address:")
        label_6.SetToolTip("The Email to be used for sending Emails to customers")
        grid_sizer_4.Add(label_6, 0, wx.RIGHT | wx.TOP, 4)
        grid_sizer_4.Add(self.text_ctrl_6, 0, 0, 0)
        label_12 = wx.StaticText(self.ntoebook_1_pane_3, wx.ID_ANY, "SSID")
        label_12.SetToolTip("The Email to be used for sending Emails to customers")
        grid_sizer_4.Add(label_12, 0, wx.RIGHT | wx.TOP, 4)
        grid_sizer_4.Add(self.text_ctrl_11, 0, 0, 0)
        label_11 = wx.StaticText(self.ntoebook_1_pane_3, wx.ID_ANY, "Username:")
        label_11.SetToolTip("The Email to be used for sending Emails to customers")
        grid_sizer_4.Add(label_11, 0, wx.RIGHT | wx.TOP, 4)
        grid_sizer_4.Add(self.text_ctrl_10, 0, 0, 0)
        label_8 = wx.StaticText(self.ntoebook_1_pane_3, wx.ID_ANY, "Password: ")
        grid_sizer_4.Add(label_8, 0, wx.RIGHT | wx.TOP, 4)
        grid_sizer_4.Add(self.text_ctrl_8, 0, 0, 0)
        sizer_5.Add(grid_sizer_4, 1, wx.ALL | wx.EXPAND, 12)
        self.ntoebook_1_pane_3.SetSizer(sizer_5)
        sizer_6.Add(self.text_ctrl_1, 3, wx.EXPAND, 0)
        label_9 = wx.StaticText(self.notebook_1_pane_4, wx.ID_ANY, "Sheet name:")
        label_9.SetToolTip("The name of the google sheets document.")
        grid_sizer_3.Add(label_9, 0, wx.RIGHT | wx.TOP, 4)
        grid_sizer_3.Add(self.text_ctrl_9, 0, 0, 0)
        label_10 = wx.StaticText(self.notebook_1_pane_4, wx.ID_ANY, "Sevice Account Credentials")
        label_10.SetToolTip("The name of the google sheets document.")
        grid_sizer_3.Add(label_10, 0, wx.RIGHT | wx.TOP, 4)
        grid_sizer_3.Add(self.text_ctrl_3, 0, 0, 0)
        sizer_6.Add(grid_sizer_3, 1, wx.ALL, 12)
        self.notebook_1_pane_4.SetSizer(sizer_6)
        label_5 = wx.StaticText(self.notebook_1_pane_6, wx.ID_ANY, "Email:")
        label_5.SetToolTip("The Email to be used for sending Emails to customers")
        grid_sizer_2.Add(label_5, 0, wx.RIGHT | wx.TOP, 4)
        grid_sizer_2.Add(self.text_ctrl_5, 0, 0, 0)
        label_7 = wx.StaticText(self.notebook_1_pane_6, wx.ID_ANY, "Password: ")
        grid_sizer_2.Add(label_7, 0, wx.RIGHT | wx.TOP, 4)
        grid_sizer_2.Add(self.text_ctrl_7, 0, 0, 0)
        sizer_3.Add(grid_sizer_2, 1, wx.ALL | wx.EXPAND, 12)
        self.notebook_1_pane_6.SetSizer(sizer_3)
        sizer_7.Add(self.text_ctrl_2, 3, wx.EXPAND, 0)
        self.notebook_1_pane_1.SetSizer(sizer_7)
        self.notebook_1.AddPage(self.notebook_1_pane_2, "General")
        self.notebook_1.AddPage(self.ntoebook_1_pane_3, "Host")
        self.notebook_1.AddPage(self.notebook_1_pane_4, "Spreadsheet")
        self.notebook_1.AddPage(self.notebook_1_pane_6, "Email")
        self.notebook_1.AddPage(self.notebook_1_pane_1, "Logs")
        sizer_1.Add(self.notebook_1, 1, wx.ALL | wx.EXPAND, 12)
        grid_sizer_1.Add(self.button_1, 0, 0, 0)
        grid_sizer_1.Add(self.button_2, 0, 0, 0)
        sizer_1.Add(grid_sizer_1, 0, wx.ALIGN_RIGHT | wx.ALL, 12)
        self.SetSizer(sizer_1)
        sizer_1.SetSizeHints(self)
        self.Layout()
        # end wxGlade

    import _pickle as cPickle
    thePickledObjectsFile = './Profile_settings.pkl'

    def __load_pickled_data(self):
        try:
            with open(self.thePickledObjectsFile, "rb") as f: 
                return self.cPickle.load(f)
        except:
            return list()

    def OnSaveButton(self, event):  # wxGlade: MyFrame.<event_handler>
        newConfig = list()
        emails = list()
        x = 0
        while x < self.text_ctrl_1.GetNumberOfLines():
            email = self.text_ctrl_1.GetLineText(x)
            if email != '':
                emails.append(email)
            x += 1
        newConfig.append( { 'EXTRA_EMAILS' : emails } )
        newConfig.append( {'REGISTRY': self.text_ctrl_9.GetLineText(0)} )
        newConfig.append( {'_PASSWORD_PREFIX': 'Normet2019-'} )
        newConfig.append( {'_GMAIL_USER': self.text_ctrl_5.GetLineText(0)} )
        newConfig.append( {'_GMAIL_USER_PASS': self.text_ctrl_7.GetLineText(0)} )
        newConfig.append( {'SSID': self.text_ctrl_11.GetLineText(0)} )
        newConfig.append( {'WaitAfterEmail': self.slider_1.GetValue()} )
        newConfig.append( {'CARRIER': self.Carriers[self.radio_box_1.GetSelection()]} )
        newConfig.append( {'HOST_ADDRESS': 'http://' + self.text_ctrl_6.GetLineText(0)} )
        newConfig.append( {'HOST_USERNAME': self.text_ctrl_10.GetLineText(0)} )
        newConfig.append( {'HOST_PASSWORD': self.text_ctrl_8.GetLineText(0)} )
        newConfig.append( {'SERVICE_ACCOUNT_CREDENTIALS': self.text_ctrl_3.GetLineText(0)} )
        newConfig.append( {'HourMinute': self.HourMinutesList[self.choice_1.GetSelection()], 
                            'DayNight' : self.DayNightList[self.choice_2.GetSelection()] } )
        
        with open(self.thePickledObjectsFile, "wb") as f:
            self.cPickle.dump(newConfig, f)
    
        print('the data has been pickled')

    def OnCancelButton(self, event):  # wxGlade: MyFrame.<event_handler>
        quit()

    def onShowManual(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'onShowManual' not implemented!")
        event.Skip()

    def onAboutShow(self, event):  # wxGlade: MyFrame.<event_handler>
        a = MyDialog(self, title="Dialog").ShowModal() 

    def RunTrayIcon(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'RunTrayIcon' not implemented!")
        event.Skip()
    def shutdownTrayIcon(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'shutdownTrayIcon' not implemented!")
        event.Skip()
# end of class MyFrame

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    Settings = MyApp(0)
    Settings.MainLoop()