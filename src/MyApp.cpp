#include "MyApp.hpp"

#include "MyFrame.hpp"

bool MyApp::OnInit() {
	SetAppName("Password Calculator");
	auto frame = new MyFrame;
	frame->Show(true);
	return true;
}
