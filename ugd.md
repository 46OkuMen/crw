* Header:
	* 00: 01 if a single image, 00 if a tileset...?
	* 01-02: Width in blocks. * 8 = pixel width
	* 03-04: Height in pixels

* It renders things in 8-pixel-wide blocks.
	* It might simultaneously render stuff 16 blocks away, moving left to right.
		* (Title screen disk glitch)
	
* No apparent "end" bytes.

* Anything interesting about double-bytes?
	* Repeating a8 twice does not do anything unusual. Yay!
		* Same for 00 00.

# Experiments
	* "Hello": ff 08 08 ff 00 f8 a8 b8 00 00 ff 80 00 ff 80 00 f8 90 90 f8
	*          ff 08 08 ff 00 f8 a8 a8 00 ff 80 00 ff 80 00 f8 90 90 f8
	* ff 08 08 ff 00 f8 a8 a8 00 ff 00 ff 00 18 24 42 24 18 00
	* o: 70 50 50 70



* 00: normal binary
* 10 skips 100 rows down.
	* 11 skips 2 rows down.
	* 12 skips 3 rows down.
	* 17 skips 8 rows down.
	* 1f skips 16 row down.
* 20 fills 100 rows solid.
	* 2f should fill 16 rows, right? (Yes)
* 30 fills 100 rows with 0000 1111.
* 40 fills 100 rows with 0000 1111, 0000 1110.
* 50: normal binary
* 60: go back 3 pixels, then copy 100 rows 1 at a time (repeat the last 3 rows a lot)
	* 61: go back 3 pixels, then copy 1 row
	* 62: go back 3 pixels, then copy 2 rows one at a time
	* 65: go back 3 pixels, then copy 5 rows one at a time
* 70: normal, I think
* 80 80 repeated seems to copy the previous 3 lines 40 times.
	* 80 40: repeats the previous 3 lines ~20 times.
	* 80 10: repeats the previous 3 lines ~5 times.
	* Does 81 repeat anything?
		* Yes
* 90 seems to repeat things as well.
	* 90 40: repeat the previous 4 lines for 0x40 pixels. (Ah, so not repeats)
* a0: normal binary
* b0: what?????
	* b8 is a control code... fills in a lot of stuff??
	* bf does a similar thing.
* c0: copies the column 3 times
	* c1: skips 2 rows...?
	* c2: skips 3 rows
	* c7: skips 8 rows
* d0: copies the column once, plus a lot of garbage
* e0: copies... something. Lots of garbage, then the beginning of the image again
	* e1: ...? The stuff after it doesn't show up.
	* e0 10: No effect, doesn't even skip the lines
	* e0 11: Same, no effect
* f0: normal binary

* So what I really need is an escape byte, to let me use all those things as normal binary.
	* e3 82 reads "82" as normal binary 1000 0010.
	* Which e* byte should be used to escape various things?
		* e1 15
		* e1 18
		* e3 1b
		* e1 1e
		* e1 1f
		* e1 43
		* e1 49
		* e1 38
		* e1 3f
		* e1 60
		* e1 67
		* e1 80
		* e1 45
		* e4 4b
		* e1 54
		* e1 7f
		* e1 9f
		* e1 b0
		* e1 bb
		* e1 be
		* e1 bf
		* e0 c0
		* e1 c2
		* e1 c3
		* e1 ca
		* e1 de
		* e1 d4
		* e1 e0
		* e1 e1
		* e1 e6
		* e1 e7
		* e1 ea
		* e1 ee
		* e1 ef

* Still wondering about the interaction of planes. What causes stuff to stay or float?


# FACE0.UGD

# BAR_A.UGD

(Old stuff from before I understood any of it)

40e = 0f;

412 = fc; planes are in a weird location

417 = e0;

419 = ee;

41a = e0; fills in first column, bytes 1110 0111 in 13th row.
41b = c0; fills in first column, bytes 1100 0010 in 14th row.
41c = 1f; fills in first column, bytes 1100 1110 in 15th row.
41d = 0f; fills in first column, bytes 1111 0000 in 16th row. Fills in with grey, rest is set to white (some grey earlier)

41e = f8: fills in second column, bytes 0000 1110 in 1st row. (also whites out that last 0, which was grey before)
41f = f8; nothing? (some speical meaning when a repeat of the previous one?)
420 = F0; fills in second column, bytes 0000 1110 in 3rd row.
421 = 08; fills in second column, bytes 0011 0111 in 4th row.
422 = 0c; fills in second column, bytes 0011 0011 in 5th row.
423 = 0e; fills in second column, bytes 0111 0001 in 6th row.
424 = 06; fills in second column, bytes 0011 0001 in 7th row.

5dd = e0; fills in last column, bytes 0010 0001 in 16th row.

white white grey white   blue blue grey orange
+ 1     1     0    0       0    0    0     0 =
white white white grey   blue blue grey  blue

Now FF?

white white grey white   blue blue grey orange
+ 1     1    1    1        1    1      1    1 =
white white white white  orange orange white orange

How about 00?
white white grey white   blue blue grey orange
+ 0   0      0     0       0    0   0     0 =
grey  grey   grey grey    blue  blue grey  blue

(end of file)

It's like the data is written to shine through windows. Writing data has no effect if it's already white, so it only shows up in the "window" of the blackness/grey/orange

# Palette
0000 black    #000000
0001 ltoran   #ff9933
0010 grngrey  #aaaa55
0011 orange   #ee8844
0100 blue     #5588dd
0101 brown    #663300
0110 dkgrey   #998899
0111 pale     #ffccaa
1000 purple   #4411aa
1001 red      #dd3311
1010 blugrey  #665577
1011 peach    #ffaa77
1100 green    #558800
1101 tan      #cc6611
1110 ltgrey   #ccccaa
1111 white    #ffffff

1f = 0
2f = 1