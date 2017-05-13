### Reinsertion
* So Mission 1 crashes right after control is restored after "Looks like there's still more above us."
	* With the original CR1.EXE in place:
		* Works.
	* With the CR1 assembly hacks restored to normal:
		* Still breaks.
	* So that means it's something to do with text or pointers in CR1.
		* With the command text block inserted:
			* Works.
		* With command text & Save/Load/Quit text:
			* Works.
* Since the pointer format is so vague, this crash is likely caused by something that's not a pointer being edited mistakenly.

### Images
* Try messing with the Reiko portrait instead of the bar. Starker color differences, easier to load on demand, smaller.

### Patcher
* Gotta call it Pachy98-CRW.exe.