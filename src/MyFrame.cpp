#include "MyFrame.hpp"

#include "password.hpp"

#include <wx/clipbrd.h>
#include <wx/stdpaths.h>
#include <wx/filename.h>

enum {
	ID_ALIAS = wxID_HIGHEST + 1,
	ID_SECRET,
};

MyFrame::MyFrame()
: wxFrame(nullptr, wxID_ANY, "Password Calculator"), panel(new wxPanel(this)),
textAlias(new wxTextCtrl(
	panel, ID_ALIAS, "", wxDefaultPosition, wxDefaultSize, wxTE_PROCESS_ENTER
)),
textSecret(new wxTextCtrl(
	panel, ID_SECRET, "", wxDefaultPosition, wxDefaultSize, wxTE_PROCESS_ENTER | wxTE_PASSWORD
)),
icon(
	wxFileName(wxStandardPaths::Get().GetExecutablePath()).GetPath() +
	"/../share/icons/com.bixense.PasswordCalculator.svg"
) {
#ifdef _WIN32
	SetIcon(wxICON(MAINICON));
#else
	SetIcon(icon);
#endif
	auto vbox = new wxBoxSizer(wxVERTICAL);
	vbox->SetMinSize(200, 0);

	vbox->Add(new wxStaticText(panel, wxID_ANY, "Alias:"), 0, wxLEFT | wxRIGHT | wxTOP, 9);
	vbox->AddSpacer(2);
	vbox->Add(
		textAlias,
		0, wxEXPAND | wxLEFT | wxRIGHT | wxBOTTOM, 9
	);
	vbox->Add(new wxStaticText(panel, wxID_ANY, "Secret:"), 0, wxLEFT | wxRIGHT | wxTOP, 9);
	vbox->AddSpacer(2);
	vbox->Add(
		textSecret,
		0, wxEXPAND | wxLEFT | wxRIGHT | wxBOTTOM, 9
	);
	auto button = new wxButton(panel, wxID_ANY, "Copy to clipboard");
	Connect(
		wxID_ANY, wxEVT_COMMAND_BUTTON_CLICKED, wxCommandEventHandler(MyFrame::onCopyToClipboard)
	);
	Connect(ID_ALIAS, wxEVT_TEXT_ENTER, wxCommandEventHandler(MyFrame::onCopyToClipboard));
	Connect(ID_SECRET, wxEVT_TEXT_ENTER, wxCommandEventHandler(MyFrame::onCopyToClipboard));
	button->SetDefault();
	vbox->AddSpacer(9);
	vbox->Add(
		button, 1, wxEXPAND | wxALL, 9
	);
	panel->SetSizer(vbox);
	vbox->SetSizeHints(this);
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
