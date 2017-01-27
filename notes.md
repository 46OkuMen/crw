* Intro Timer ASM:
	* At 0x2e8e: 81fe0001, "cmp esi, 0x100"
	* Change the 0001 (0x100) to a higher number to accommodate the text.

* Intro Autostart Glitch:
	* Ensure that the length of TITOL.TXT, in bytes, is even.

* Scenario End-Of-Input Control Code Change:
	* 0df0:1c97 807efc20 cmp [bp-04], 20
		* What file is at 0df0? (OPEN.EXE)
		* This code is present in all CR*.EXE files and OPEN.EXE.
		* Replace all instances of 807efc20 -> 807efc1f. Use 1f as the control code instead.

* Formatting:
	* Scenario text: 50 chars to a line
	* Intro text: 50 chars