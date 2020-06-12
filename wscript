#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import tempfile
from waflib import Options, Configure, Logs
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
	if os.path.exists('Password Calculator.app'):
		Logs.warn('Password Calculator.app/ already exists, moving to trash.')
		if shutil.which('trash') is None:
			ctx.fatal('Please install trash command using `brew install trash`.')
		subprocess.check_call(['trash', 'Password Calculator.app'])

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

		res_dir = 'Password Calculator.app/Contents/Resources/'
		os.makedirs(res_dir)
		shutil.move(os.path.join(d, 'Password Calculator.icns'), res_dir)

		macos_dir = 'Password Calculator.app/Contents/MacOS/'
		os.makedirs(macos_dir)
		shutil.copy('build/pwcalculator', macos_dir)

		frameworks_dir = 'Password Calculator.app/Contents/Frameworks/'
		os.makedirs(frameworks_dir)
		subprocess.check_call(['dylibbundler', '-p', '@executable_path/../Frameworks/', '-x', "'" + macos_dir + 'pwcalculator' + "'", '-b', '-cd', '-d', "'" + frameworks_dir + "'"])

		for dirpath, dirs, files in os.walk(frameworks_dir):
			for f in files:
				fn = os.path.join(dirpath, f)
				subprocess.check_call([
					'codesign', '--options=runtime', '--verify', '--verbose', '--sign', 
					'Developer ID Application: Jan Niklas Hasse (4DMBNMNYSA)', fn
				])

		with open('Password Calculator.app/Contents/Info.plist', 'w') as info:
			info.write('''<?xml version="1.0" encoding="UTF-8"?>
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
		<key>CFBundleExecutable</key>
		<string>pwcalculator</string>
		<key>CFBundleIconFile</key>
		<string>Password Calculator</string>
		<key>NSPrincipalClass</key>
		<string>NSApplication</string>
	</dict>
	</plist>''')

		subprocess.check_call(['codesign', '--options=runtime', '--verify', '--verbose', '--sign',
			'Developer ID Application: Jan Niklas Hasse (4DMBNMNYSA)', 'Password Calculator.app'])

	Logs.info('App Bundle created. Zip it using `zip -r pwcalculator.zip Password\\ Calculator.app`.')
	Logs.info('Then run `xcrun altool --notarize-app --primary-bundle-id '
		     '"com.bixense.PasswordCalculator" --username <Apple ID> --password <Password> '
		     '--asc-provider <Team Short Name, see xcrun altool --list-providers> --file '
		     'pwcalculator.zip` to notarize the app.')
	Logs.info('After notarization finishes, run `xcrun stapler staple Password\\ Calculator.app`')