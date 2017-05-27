### Reinsertion
* Kashiwada's "next battl ...." line never gets overwritten in IV9.TXT.
	* "Damn, that's a dirty move!" gets displayed twice for some reason?
		* Use two-line dialogue for now.
* "ZOU" appears in highlighted empty slots in the mech weapons screen.
	* From "HANZOU".
	* Can I manually edit that pointer to go somewhere else?
	* It's not a pointer at all. There's an instruction 05f50050 (add ax, 0xf5) that creates the 0xde value, and this gets pushed to the stack and loaded as a value later.
		* But this is used to line up every weapon name! Increasing it to 0xf8 causes problems while highlighting other weapons, cutting off the first three letters...
	* It would be better to just move Hanzou's name!
		* Giving the 0xdb location for Hanzou's name:
mov al, [3127]    ; now what's in [3127]? How does it compare for other characters?
				  ; 6 for Hanzou, 7 for Kashiwada, 0 for Reiko, etc.
cbw
imul ax, ax, 0d       ; what if I multiply this by 0c? (that works. Just decrease the padding by 1, then)
                      ; this is at 0df0:2f4c 6bc00d
058d00 add ax, 008d   ; this is at 0x10e4f. Changing it has the same effect for all characters.
* Credits are still a little glitchy.
	* Alignment gets messed up around Anime Studio Torotoro.
	* Random period after PRESENTED BY WIZ.
* Some kind of error when quitting Mission 2, involving CRW_IPL.COM.

### Images
* Waiting for image edits now.

### Other versions mystery
* So PSX is definitely inferior. Controls are bad, dialogue lacks character. Sweet opening though.
* What is with the version in that youtube video and from screenshots on the back of the box?
	* Characters named "GROSS", "SEIDOU", and "NINA"
	* A "MISSION" button up near SYSTEM during gameplay
	* "ENSEN. HAIRYU" instead of "POINT"
	* "TENTI. TOURAKU" instead of "TIME"
	* A bunch of romanized Japanese text above "Character"
	* A picture of a mech instead of the CRW logo in the bottom right
	* Kick and Punch things for the mech in the lower right??
	* Not the Chinese or Korean DOS versions, those are basically identical ports.
	* It's most likely some sort of beta.

### Stuff for the Readme
* In Mission 5-7, not all the light areas are onscreen. Click on the minimap and go to the northwest corner (on Mission 5) to find the rest of them.