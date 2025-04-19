# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 19:08:42 2025

@author: Pradiv
"""

from cx_Freeze import setup, Executable

Executables = [Executable("machine.py", base ="Win32GUI", icon="icon.ico")]

setup(
    name="EnigmaMachineSimulator",
    version="1.0",
    description="Enigma machine simulator (GUI based: with encryption saving",
    executables=Executables
)