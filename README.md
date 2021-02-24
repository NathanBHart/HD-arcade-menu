# HD Arcade Menu
 This is the menu for the game systems we are making for HDCH

## Logs:

### Feb 23rd 2021
- Pre-Alpha v1: I have currently set up some infrastructure for a card-style menu system. Some key things I have implemented so far:
	- File reading and conversion system: This enables us to reference information from files in code. Currently reads every frame for each card object... I might want to create a "pre-load" system for efficiency.
	- Text system with (limited) wrapping abilities. You can choose from 3 levels of headers and a paragraph style, similar to markdown, and specify colour, location, and maximum amount of characters.
		- Fixes needed for character wrapping: (1) Break should be make at space, not in the middle of words. (2) Maximum amount of character wrapping should be converted to text-box based wrapping (length), using better math. This will simplify code and add to responsiveness.
	- Responsive card system: Cards will adjust based on viewport size, allowing this to work well on any monitor type. Elements will scale accordingly.
	- Scalable background image loader. Supports alpha, but alpha support may be depreciated for efficiency and consistency. Current bug: Renders and edits image every frame. Need to fix
	- I really need to add documentation...

### Feb 24th 2021
 - Pre-Alpha v2: Fixed background loader... It is much more efficient now! It can load in and run larger files with (relative) ease, but it is still recommended to file sizes that are not greater than 1MB and have a 4:3 ratio, if possible. I might want to fix the loader to adjust based on resolution so it can scale best for any display type.
 - Pre-Alpha v2.1: Updated the text function so it is more effective, breaks between words (unless too small), fits within a rectangle (text box) so it is more responsive.
 - Pre-Alpha v2.2: I added constants that configure based on screen size and resolution that can be used, such as padding, the display height and width, and an "ideal pixel ratio". This ratio scales things based on how much smaller/larger they are than the ideal ratio (1280 * 720), making things larger or smaller based on that. This is square rooted because values are determined based on two integer values (so the sqrt ensures that scaling is linear based on display, not exponential). Things scale according to this ratio, or inbuilt ratios, generally.
