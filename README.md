# HD_arcade_menu
 This is the menu for the game systems we are making for HDCH

## Logs:
- Feb 23, 2021. Pre-Alpha v1: I have currently set up some infrastructure for a card-style menu system. Some key things I have implemented so far:
	- File reading and conversion system: This enables us to reference information from files in code. Currently reads every frame for each card object... I might want to create a "pre-load" system for efficiency.
	- Text system with (limited) wrapping abilities. You can choose from 3 levels of headers and a paragraph style, similar to markdown, and specify colour, location, and maximum amount of characters.
		- Fixes needed for character wrapping: (1) Break should be make at space, not in the middle of words. (2) Maximum amount of character wrapping should be converted to text-box based wrapping (length), using better math. This will simplify code and add to responsiveness.
	- Responsive card system: Cards will adjust based on viewport size, allowing this to work well on any monitor type. Elements will scale accordingly.
	- Scalable background image loader. Supports alpha, but alpha support may be depreciated for efficiency and consistency. Current bug: Renders and edits image every frame. Need to fix
	- I really need to add documentation...

