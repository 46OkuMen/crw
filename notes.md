* Intro Timer ASM:
	* At 0x2e8e: 81fe0001, "cmp esi, 0x100"
	* Change the 0001 (0x100) to a higher number to accommodate the text.

* Intro Autostart Glitch:
	* Ensure that the length of TITOL.TXT, in bytes, is even.
	* Also make sure it ends in 0x1a.

* Scenario End-Of-Input Control Code Change:
	* 0df0:1c97 807efc20 cmp [bp-04], 20
		* What file is at 0df0? (OPEN.EXE)
		* This code is present in all CR*.EXE files and OPEN.EXE.
		* Replace all instances of 807efc20 -> 807efc1f. Use 1f as the control code instead.


* Pointers:
	* Loads strings pointed to by [si]. "Move" text (at 0x11862) has a [si] value of 0x0842, which would put 0x0 at 0x11020 (which is where the Borland compiler message is!)
		* 42 08 is at 0xaad3, and 47 08 ("Attk"?) is at 0xaae1.
			* Both are surrounded on both sides by 68.
			* (But this isn't all of them)
			* 49 68 69 08 68
			* 03 68 72 08 08
			* 00 68 7f 08 68
			* 04 68 86 08 68
			* 04 68 8d 08 68
			* 04 68 94 08 68
			* 04 68 9b 08 68
			* 00 68 a2 08 68
			* 04 68 ab 08 68
			* 04 68 b4 08 68
			* 00 68 bd 08 68
			* 04 68 c4 08 68
			* 02 68 cb 08 90
			* 52 68 d4 08 9a
			* 56 68 eb 08 9a
			* 56 68 00 09 9a
			* 56 68 13 09 eb
			* 56 68 24 09 9a
			* 57 68 35 09 9a
			* 08 68 3e 09 9a






* Formatting:
	* Scenario text: 50 chars to a line
	* Intro text: 50 chars