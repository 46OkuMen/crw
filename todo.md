### Reinsertion
* Some stray smiley hirigana at the beginning of IV3.
	* Check if it's still there.
* Some kind of crash on loading Mission 4 and 5?
	* Message begins with fullwidth DISK.
	* Has to do with something I'm reinserting, not the ASM hacks.
	* Just went away... weird.
* Weird yellow line after "Insert Data Disk 2 and left click the mouse" in Mission 5.
* Names aren't showing up right in the mech screen.
	* Also ATTACKER, EFENDER, NIPER, CONF, " "
	* Also the gun names... probably in that same block.
		* Fixed
* Kashiwada's "next battl ...." line never gets overwritten in IV9.TXT.
	* "Damn, that's a dirty move!" gets displayed twice for some reason?
		* Use two-line dialogue for now.
* Inserting the credits causes horrible glitches while changing mech's weapons.
	* Just inserting the weapons causes a minor glitch while highlighting something that's not equipped...?
	* "Assaul Rifle         I". Might be best to do the 8645 bytes...
		* Done
	* Removed most of the pointers in this range, since those are mostly just false positives.
		* Much better now.
* "ZOU" appears in highlighted empty slots in the mech weapons screen.
	* From "HANZOU".
	* Can I manually edit that pointer to go somewhere else?
* Need to pad out all the credits to 28 chars per line.
	* Or figure out how they're actually working...

### Images
* Waiting for image edits now.

### Patcher
* Gotta call it Pachy98-CRW.exe.

### Stuff for the Readme
* In Mission 5-7, not all the light areas are onscreen. Click on the minimap and go to the northwest corner (on Mission 5) to find the rest of them.