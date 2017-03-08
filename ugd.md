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