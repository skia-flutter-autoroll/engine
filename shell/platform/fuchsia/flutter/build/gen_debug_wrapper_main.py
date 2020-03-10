#!/usr/bin/env python
# Copyright 2013 The Flutter Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
import argparse
import os
import re
import sys
def main():
  parser = argparse.ArgumentParser(
    sys.argv[0],
    description="Generate main file for Fuchsia dart test")
  parser.add_argument("--out",
                      help="Path to .dart file to generate",
                      required=True)
  parser.add_argument("--main-dart",
                      help="Path to main.dart file to import",
                      required=True)
  args = parser.parse_args()
  out_dir = os.path.dirname(args.out)
  assert os.path.isfile(os.path.join(os.path.dirname(args.out), args.main_dart))
  outfile = open(args.out, 'w')

  # Ignores relative lib imports due to a few modules that complain about
  # this. It is also possible that a future may be unawaited given that main
  # may not always be synchronous across all functions.
  outfile.write('''// Generated by ''')
  outfile.write(os.path.basename(__file__))
  outfile.write('''


// ignore_for_file: avoid_relative_lib_imports
import 'dart:async';

import 'package:flutter_driver/driver_extension.dart';
''')
  outfile.write("import '%s' as flutter_app_main;\n" % args.main_dart)
  outfile.write('''
void main() async {
  assert(await (() async {
    // TODO(awdavies): Use the logger instead.
    print('Overriding app main method because flutter_driver_extendable '
        'is enabled in the build file');

    try {
      // Enables Flutter Driver VM service extension
      //
      // This extension is required for tests that use package:flutter_driver
      // to drive applications from a separate process.
      enableFlutterDriverExtension();

      // TODO(awdavies): Use the logger instead.
      print('flutter driver extensions enabled.');
      //ignore: avoid_catches_without_on_clauses
    } catch (e) {
      // TODO(awdavies): Use the logger instead.
      // Noop.
      print('flutter driver extensions not enabled. $e');
    }
    // Always return true so that the assert succeeds.
    return true;
  }()));
  // Execute the main method of the app under test
  var res = (flutter_app_main.main as dynamic)();
  if (res != null && res is Future) {
    await res;
  }
}
''')
  outfile.close()

if __name__ == '__main__':
  main()

