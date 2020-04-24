#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from waflib import Options, Configure
Configure.autoconfig = True

def options(ctx):
	ctx.load('compiler_cxx boost')
	if sys.platform in ["msys", "win32"]:
		ctx.load('winres')
	gr = ctx.get_option_group('configure options')
	gr.add_option('--release', action='store_true', help='build release binaries')

def check_flag(ctx, flag):
	ctx.env.CXXFLAGS_TMP = ''
	if not ctx.check_cxx(cxxflags=[flag], msg="Checking for '{}'".format(flag), mandatory=False,
	                     uselib_store='TMP'):
		return False
	ctx.env.append_value('CXXFLAGS', ctx.env.CXXFLAGS_TMP)
	return True

def configure(ctx):
	ctx.load('compiler_cxx boost')
	ctx.check_boost()
	if sys.platform in ["msys", "win32"]:
		ctx.load('winres')

	if Options.options.release:
		ctx.env.CXXFLAGS = ['-O2']
	else:
		ctx.env.CXXFLAGS = ['-g']

	if not check_flag(ctx, '-std=c++11'):
		ctx.env.append_value('CXXFLAGS', ['-std=c++0x'])
	ctx.env.append_value('CXXFLAGS', ['-Wall', '-Wextra'])

	if ((os.getenv("CLICOLOR", "1") != "0" and sys.stdout.isatty()) or
	    os.getenv("CLICOLOR_FORCE", "0") != "0"):
		check_flag(ctx, '-fdiagnostics-color')
	ctx.check_cfg(
		path='wx-config', args='--cflags --libs', package='',
		uselib_store='WXWIDGETS', msg='Checking for wxWidgets',
	)

def build(ctx):
	source_files = ctx.path.ant_glob('src/*.cpp')
	if sys.platform in ["msys", "win32"]:
		source_files.append("src/windows/main.rc")
	ctx.program(
		source=source_files,
		target='pwcalculator',
		use='WXWIDGETS BOOST',
	)

	ctx.install_files('${PREFIX}/share/applications', 'com.bixense.PasswordCalculator.desktop')
	ctx.install_files('${PREFIX}/share/icons', 'share/icons/com.bixense.PasswordCalculator.svg')
	ctx.install_files('${PREFIX}/share/appdata',
	                  'share/appdata/com.bixense.PasswordCalculator.appdata.xml')

def mac(ctx):
	with tempfile.TemporaryDirectory() as d:
		iconset = os.path.join(d, 'Password Calculator.iconset')
		os.mkdir(iconset)
		subprocess.check_call(['sips', '-z', '16', '16', 'pwcalculator.png', '--out', '{}/icon_16x16.png'.format(iconset)])
		subprocess.check_call(['sips', '-z', '32', '32', 'pwcalculator.png', '--out', '{}/icon_16x16@2x.png'.format(iconset)])
		subprocess.check_call(['sips', '-z', '32', '32', 'pwcalculator.png', '--out', '{}/icon_32x32.png'.format(iconset)])
		subprocess.check_call(['sips', '-z', '64', '64', 'pwcalculator.png', '--out', '{}/icon_32x32@2x.png'.format(iconset)])
		subprocess.check_call(['sips', '-z', '128', '128', 'pwcalculator.png', '--out', '{}/icon_128x128.png'.format(iconset)])
		shutil.copyfile('pwcalculator.png', '{}/icon_128x128@2x.png'.format(iconset))
		shutil.copyfile('pwcalculator.png', '{}/icon_256x256.png'.format(iconset))
		subprocess.check_call(['iconutil', '-c', 'icns', iconset])

		zipf = zipfile.ZipFile('Password Calculator.zip', 'w', zipfile.ZIP_DEFLATED)
		zipf.write(os.path.join(d, 'Password Calculator.icns'), 'Password Calculator.app/Contents/Resources/Password Calculator.icns')

		subprocess.check_call(['dylibbundler', '-p', '@executable_path/../Frameworks/', '-x', 'build/pwcalculator', '-b', '-cd', '-d', os.path.join(d, 'Frameworks')])

		for dirpath, dirs, files in os.walk(os.path.join(d, 'Frameworks')):
			for f in files:
				fn = os.path.join(dirpath, f)
				zipf.write(fn, os.path.join('Password Calculator.app/Contents/Frameworks', f))

		zipf.write('build/pwcalculator', 'Password Calculator.app/Contents/MacOS/pwcalculator')

		with zipf.open('Password Calculator.app/Contents/Info.plist', 'w') as info:
			info.write(b'''<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
	<dict>
		<key>CFBundleName</key>
		<string>Password Calculator</string>
		<key>CFBundleDisplayName</key>
		<string>Password Calculator</string>
		<key>CFBundleIdentifier</key>
		<string>com.bixense.PasswordCalculator</string>
		<key>CFBundleVersion</key>
		<string>1.0.0</string>
		<key>CFBundlePackageType</key>
		<string>APPL</string>
		<key>CFBundleSignature</key>
		<string>????</string>
		<key>CFBundleExecutable</key>
		<string>pwcalculator</string>
		<key>CFBundleIconFile</key>
		<string>Password Calculator</string>
		<key>NSPrincipalClass</key>
		<string>NSApplication</string>
	</dict>
	</plist>''')
