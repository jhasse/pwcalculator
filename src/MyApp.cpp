#include "MyApp.hpp"

#include "MyFrame.hpp"

bool MyApp::OnInit() {
	auto frame = new MyFrame;
	frame->Show(true);
	return true;
}
