#pragma once

#include <wx/wx.h>

class MyFrame : public wxFrame {
public:
	MyFrame();
private:
	void onCopyToClipboard(wxCommandEvent&);

	wxPanel* panel;
	wxTextCtrl* textAlias;
	wxTextCtrl* textSecret;
	wxTimer timer;
	wxIcon icon;
};
