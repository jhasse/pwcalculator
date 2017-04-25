#!/usr/bin/env python

import os
import sys
from waflib import Options, Configure
Configure.autoconfig = True

def options(ctx):
	ctx.load('compiler_cxx')
	if sys.platform in ["msys", "win32"]:
		ctx.load('winres')
	gr = ctx.get_option_group('configure options')
	gr.add_option('--release', action='store_true', help='build release binaries')

def configure(ctx):
	ctx.load('compiler_cxx')
	if sys.platform in ["msys", "win32"]:
		ctx.load('winres')

	if Options.options.release:
		ctx.env.CXXFLAGS = ['-O2']
	else:
		ctx.env.CXXFLAGS = ['-g']

	ctx.env.append_value('CXXFLAGS', ['-Wall', '-Wextra', '-std=c++11'])

	if ((os.getenv("CLICOLOR", "1") != "0" and sys.stdout.isatty()) or
	    os.getenv("CLICOLOR_FORCE", "0") != "0"):
		ctx.env.append_value('CXXFLAGS', ['-fdiagnostics-color'])
	ctx.check_cfg(
		path='wx-config', args='--cflags --libs', package='',
		uselib_store='WXWIDGETS'
	)
	ctx.check_cfg(args='--cflags --libs', package='openssl', uselib_store='OPENSSL')

def build(ctx):
	source_files = ctx.path.ant_glob('src/*.cpp')
	if sys.platform in ["msys", "win32"]:
		source_files.append("src/windows/main.rc")
	ctx.program(
		source=source_files,
		target='pwcalculator',
		use='WXWIDGETS',
	)

	ctx.install_files('${PREFIX}/share/applications', 'com.bixense.PasswordCalculator.desktop')
	ctx.install_files('${PREFIX}/share/icons', 'share/icons/com.bixense.PasswordCalculator.svg')
	ctx.install_files('${PREFIX}/share/appdata',
	                  'share/appdata/com.bixense.PasswordCalculator.appdata.xml')
