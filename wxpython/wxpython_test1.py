import wx

class InfoPanel(wx.Frame):
	def __init__(self, parent, title):
		super(InfoPanel, self).__init__(parent, title=title, size=(600,600))
		self.InitUI()
		self.Centre()

	def InitUI(self):
		self.panel = wx.Panel(self)
		self.panel.SetBackgroundColour("gray")
		font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
		font.SetPointSize(12)
		


def main():
	app = wx.App()
	infoPanel = InfoPanel(None, title="password_recorder")
	infoPanel.Show()
	app.MainLoop()

if __name__ == "__main__":
	main()