# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 16:38:48 2025

@author: Pradiv
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
import threading

class Rotor:
    def __init__(self, wiring, notch):
        self.wiring = wiring
        self.notch = notch
        self.position = 0
        
    def rotate(self):
        self.position = (self.position + 1) % 26
    
    def encode(self, letter):
        index = (ord(letter) - ord('A') + self.position) % 26
        encodedLetter = self.wiring[index]
        return chr((ord(encodedLetter) - ord('A') - self.position) % 26 + ord('A'))
    
    def at_notch(self):
        return self.wiring[self.position] in self.notch
    

class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring
        
    def reflect(self, letter):
        index = ord(letter) - ord('A')
        return self.wiring[index]


class EnigmaMachine:
    def __init__(self, rotors, reflector):
        self.rotors = rotors
        self.reflector = reflector
        
    def encrypt(self, message):
        encryptedmessage = []
        for letter in message:
            if letter.isalpha():
                letter.upper()
                self.step_rotors()
                for rotor in self.rotors:
                    letter = rotor.encode(letter)
                letter = self.reflector.reflect(letter)
                for rotor in reversed(self.rotors):
                    letter = rotor.encode(letter)
                encryptedmessage.append(letter)
            else:
                encryptedmessage.append(letter)
        return ''.join(encryptedmessage)
    
    def step_rotors(self):
        for i in range(len(self.rotors)):
            self.rotors[i].rotate()
            if not self.rotors[i].at_notch():
                break
            
class EnigmaGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initGUI()
        
    def initGUI(self):
        self.setWindowTitle('Enigma Machine Simulator')
        
        #layout setup
        layout = QVBoxLayout()
        
        self.inputLabel = QLabel('Enter messages (for multiple message separate by semi-colon):')
        self.inputField = QLineEdit()
        self.encryptButton = QPushButton('Encrypt')
        self.encryptButton.clicked.connect(self.encrypt_messages)
        layout.addWidget(self.inputLabel)
        layout.addWidget(self.inputField)
        layout.addWidget(self.encryptButton)
        
        self.outputLabel = QLabel('Encrypted Messages:')
        self.outputFiled = QTextEdit()
        self.outputFiled.setReadOnly(True)
        layout.addWidget(self.outputLabel)
        layout.addWidget(self.outputFiled)
        
        
        self.setLayout(layout)
        
        rotor1Wiring = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
        rotor2Wiring = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
        rotor3Wiring = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
        reflectorWiring = "YRUHQSLDPXNGOKIETZJWVFMCBA"
        
        self.rotors = [
            Rotor(rotor1Wiring, "Q"),
            Rotor(rotor2Wiring, "E"),
            Rotor(rotor3Wiring, "V")
            ]
        
        self.reflector = Reflector(reflectorWiring)
        self.enigmaMachine = EnigmaMachine(self.rotors, self.reflector)
        
    def encrypt_messages(self):
        messages = self.inputField.text().split(';')
        messages = [msg.strip() for msg in messages]
        results = [None] * len(messages)
        
        threads = []
        for i, message in enumerate(messages):
            thread = threading.Thread(target=self.encode_message, args=(message, results, i))
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()
            
        self.outputFiled.clear()
        for original, encoded in zip(messages, results):
            self.outputFiled.append(f"Original: {original} -> Encoded: {encoded}")
        
        self.save_result_file(results)
    
    def encode_message(self, message, results, index):
        try:
            results[index] = self.enigmaMachine.encrypt(message)
        except Exception as e:
            results[index] = f"Error Encoding: '{message}' : {str(e)}"
            
    def save_result_file(self, results):
        try:
            with open('encryptedText.txt', 'w') as file:
                for result in results:
                    file.write(f"{result}\n")
                self.outputFiled.append(f"File written success")
        except IOError as e:
            self.outputFiled.append(f"IO error occured: {e}")
        except PermissionError as e:
            self.outputFiled.append(f"Permission Error occured: {e}")  
        except Exception as e:
            self.outputFiled.append(f"An error has occured: {e}")
        finally:
            
            file.close()            

#End of coding the simulator
#main function 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = EnigmaGUI()
    ex.setFixedSize(400, 300)
    ex.show()
    sys.exit(app.exec_())
    
        
        
        