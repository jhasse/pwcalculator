#include "MyFrame.hpp"

#include "password.hpp"

#include <wx/clipbrd.h>
#include <wx/url.h>

enum {
	ID_ALIAS = wxID_HIGHEST + 1,
	ID_SECRET,
};

MyFrame::MyFrame()
: wxFrame(nullptr, wxID_ANY, "Password Calculator", wxDefaultPosition, wxSize(250, 150)),
textAlias(new wxTextCtrl(
	this, ID_ALIAS, "", wxDefaultPosition, wxDefaultSize, wxTE_PROCESS_ENTER
)),
textSecret(new wxTextCtrl(
	this, ID_SECRET, "", wxDefaultPosition, wxDefaultSize, wxTE_PROCESS_ENTER | wxTE_PASSWORD
)),
icon("pwcalculator.svg") {
	auto vbox = new wxBoxSizer(wxVERTICAL);

	vbox->Add(
		textAlias,
		1, wxEXPAND | wxALL, 5
	);
	vbox->Add(
		textSecret,
		1, wxEXPAND | wxALL, 5
	);
	auto button = new wxButton(this, wxID_ANY, "Copy to clipboard");
	Connect(
		wxID_ANY, wxEVT_COMMAND_BUTTON_CLICKED, wxCommandEventHandler(MyFrame::onCopyToClipboard)
	);
	Connect(ID_ALIAS, wxEVT_TEXT_ENTER, wxCommandEventHandler(MyFrame::onCopyToClipboard));
	Connect(ID_SECRET, wxEVT_TEXT_ENTER, wxCommandEventHandler(MyFrame::onCopyToClipboard));
	button->SetDefault();
	vbox->Add(
		button, 1, wxEXPAND | wxALL, 5
	);
	SetSizerAndFit(vbox);
	SetIcon(icon);
}

void MyFrame::onCopyToClipboard(wxCommandEvent&) {
	std::string pw = calculatePassword(
		std::string(textSecret->GetLineText(0).ToUTF8()),
		std::string(textAlias->GetLineText(0).ToUTF8())
	);
	if (wxTheClipboard->Open())	{
		wxTheClipboard->SetData(new wxTextDataObject(pw));
		wxTheClipboard->Flush();
		wxTheClipboard->Close();
	}
	textSecret->Clear();
	Iconize(); // minimize
}
