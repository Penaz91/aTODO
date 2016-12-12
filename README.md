# aTODO
A small JSON and Python based TODO application

## Description
aTODO is a very small and dirty way to take notes of what you have to do, but giving a bit more space to the description/status of said TODO, instead of focusing to "Buy milk" kind of stuff.

##Usage
`todo <action> <arguments>`

###Actions
- **list** Shows a list of all the TODOs saved
- **view** Shows the TODO with the ID specified in `<arguments>`
- **add** Adds a new TODO (The ID is automatically generated) with the title specified in `<arguments>` *remember to enclose the title in double quotes (")*
- **delete** Removes the TODO with the ID specified in `<arguments>`
- **edit** Opens the TODO with the ID specified in `<arguments>` with the program specified in the `$EDITOR` environment variable. Prepare for some JSON manual editing.

Calling `todo` without arguments is the same of calling `todo list`.

All the actions can be replaced with their initial (so `todo list` can be called via `todo l`)

###Arguments
The only argument accepted so far is the ID of the TODO (shown in `todo list`)

###Decoding the `todo list` output.
All lines in aTODO are formatted the same way:
> [ID] [M] Title

[ID] Represents the Identifier of the TODO

[M] Can appear or not, depending on the fact that the TODO is an "Extended Memo"

Title is simply the title of the TODO


###Extended Memos
An "Extended Memo" is something a bit more complex than a simple TODO, it can keep notes about the matter you're treating.

To Create an "Extended Memo", just create a normal TODO and then edit the "Message" part of the JSON via `todo e <id>`.
`todo list` will remind you that a TODO is an "Extended Memo" by placing the `[M]` mark on its line.

###Implementation Details
aTODO just creates some JSON files in .todo, placed inside your /home directory.

###Usage Examples
- `todo a "Buy Milk"` Simply creates a new TODO with Title "Buy Milk"
- `todo e 2` Edits the TODO with ID "2", making the "Message" value different from empty will make the TODO an "Extended Memo"
- `todo d 4` Deletes the TODO with ID "4"
- `todo` Lists the existing TODOs
- `todo v 1` Shows all the details of the TODO with ID "1", this will show the "Message" value too, if the TODO is an "Extended Memo"
