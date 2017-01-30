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


* Pointers:
	* Loads strings pointed to by [si]. "Move" text (at 0x11862) has a [si] value of 0x0842, which would put 0x0 at 0x11020 (which is where the Borland compiler message is!)
		* 42 08 is at 0xaad3, and 47 08 ("Attk"?) is at 0xaae1.
			* Both are surrounded on both sides by 68.

* Formatting:
	* Scenario text: 50 chars to a line
	* Intro text: 50 chars