@echo off
python src/emulator.py --vfs tests/vfs_min.xml --script tests/start_stage3.txt
python src/emulator.py --vfs tests/vfs_med.xml --script tests/start_stage3.txt
python src/emulator.py --vfs tests/vfs_deep.xml --script tests/start_stage3.txt