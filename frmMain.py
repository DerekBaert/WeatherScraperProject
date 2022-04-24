# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class fraMain
###########################################################################

class fraMain ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Weather Scraper", pos = wx.DefaultPosition, size = wx.Size( 724,412 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Box Plot", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		self.m_staticText2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

		bSizer6.Add( self.m_staticText2, 0, wx.ALL, 5 )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Starting Year:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		self.m_staticText3.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

		bSizer7.Add( self.m_staticText3, 0, wx.ALL, 5 )

		drp_StartYearChoices = []
		self.drp_StartYear = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, drp_StartYearChoices, 0 )
		self.drp_StartYear.SetSelection( 0 )
		bSizer7.Add( self.drp_StartYear, 0, wx.ALL, 5 )


		bSizer6.Add( bSizer7, 0, wx.EXPAND, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Ending Year:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		self.m_staticText4.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

		bSizer8.Add( self.m_staticText4, 0, wx.ALL, 5 )

		drp_EndYearChoices = []
		self.drp_EndYear = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, drp_EndYearChoices, 0 )
		self.drp_EndYear.SetSelection( 0 )
		bSizer8.Add( self.drp_EndYear, 0, wx.ALL, 5 )


		bSizer6.Add( bSizer8, 0, wx.EXPAND, 5 )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		self.btnBox = wx.Button( self, wx.ID_ANY, u"Generate Box Plot", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.btnBox, 0, wx.ALL, 5 )


		bSizer6.Add( bSizer13, 1, wx.EXPAND, 5 )


		bSizer4.Add( bSizer6, 1, wx.EXPAND, 5 )


		bSizer3.Add( bSizer4, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )

		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Line Plot", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		self.m_staticText5.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

		bSizer9.Add( self.m_staticText5, 0, wx.ALL, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText51 = wx.StaticText( self, wx.ID_ANY, u"Month:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )

		self.m_staticText51.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

		bSizer11.Add( self.m_staticText51, 0, wx.ALL, 5 )

		drp_MonthChoices = [ u"January", u"February", u"March", u"April", u"May", u"June", u"July", u"August", u"September", u"October", u"November", u"December" ]
		self.drp_Month = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, drp_MonthChoices, 0 )
		self.drp_Month.SetSelection( 0 )
		bSizer11.Add( self.drp_Month, 0, wx.ALL, 5 )


		bSizer9.Add( bSizer11, 0, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Year:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		self.m_staticText6.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

		bSizer10.Add( self.m_staticText6, 0, wx.ALL, 5 )

		drp_YearChoices = []
		self.drp_Year = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, drp_YearChoices, 0 )
		self.drp_Year.SetSelection( 0 )
		bSizer10.Add( self.drp_Year, 0, wx.ALL, 5 )


		bSizer9.Add( bSizer10, 0, wx.EXPAND, 5 )

		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		self.btnLine = wx.Button( self, wx.ID_ANY, u"Generate Line Plot", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.btnLine, 0, wx.ALL, 5 )


		bSizer9.Add( bSizer14, 0, wx.EXPAND, 5 )


		bSizer3.Add( bSizer9, 1, wx.EXPAND, 5 )


		bSizer2.Add( bSizer3, 1, wx.EXPAND, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

		self.btnUpdate = wx.Button( self, wx.ID_ANY, u"Update Dataset", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.btnUpdate, 0, wx.ALL, 5 )

		self.btnDownload = wx.Button( self, wx.ID_ANY, u"Download Dataset", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.btnDownload, 0, wx.ALL, 5 )

		self.lbl_Error = wx.StaticText( self, wx.ID_ANY, u"Error Message", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_Error.Wrap( -1 )

		self.lbl_Error.SetForegroundColour( wx.Colour( 164, 0, 0 ) )
		self.lbl_Error.Hide()

		bSizer1.Add( self.lbl_Error, 0, wx.ALL, 5 )

		self.lbl_Status = wx.StaticText( self, wx.ID_ANY, u"Status Message", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_Status.Wrap( -1 )

		self.lbl_Status.Hide()

		bSizer1.Add( self.lbl_Status, 0, wx.ALL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.btnBox.Bind( wx.EVT_BUTTON, self.btnBox_Click )
		self.btnLine.Bind( wx.EVT_BUTTON, self.btnLine_Click )
		self.btnUpdate.Bind( wx.EVT_BUTTON, self.btnUpdate_Click )
		self.btnDownload.Bind( wx.EVT_BUTTON, self.btnDownload_Click )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def btnBox_Click( self, event ):
		event.Skip()

	def btnLine_Click( self, event ):
		event.Skip()

	def btnUpdate_Click( self, event ):
		event.Skip()

	def btnDownload_Click( self, event ):
		event.Skip()


