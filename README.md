# aTODO

![Status:Active](https://img.shields.io/badge/Project_Status-Active-brightgreen.svg)

A small JSON and Python based TODO application

## Description
aTODO is a very small and dirty way to take notes of what you have to do, but giving a bit more space to the description/status of said TODO, instead of focusing to "Buy milk" kind of stuff.

## Usage
`todo <action> <arguments>`

### Actions
- **list** Shows a list of all the TODOs saved
- **view** Shows the TODO with the ID specified in `<arguments>`
- **add** Adds a new TODO (The ID is automatically generated), the details of the TODO are asked when necessary
- **delete** Removes the TODO with the ID specified in `<arguments>`
- **edit** Opens the TODO with the ID specified in `<arguments>` with a simple internal interface. (EXPERIMENTAL)

Calling `todo` without arguments is the same of calling `todo list`.

All the actions can be replaced with their initial (so `todo list` can be called via `todo l`)

### Arguments
The only arguments accepted are the ID of the TODO (shown in `todo list`) and eventually the `--legacy` option to use the legacy editing more (instead of the tempfile-based editing mode using your editor).

### Decoding the `todo list` output.
All lines in aTODO are formatted the same way:
> [ID] [M] Title

[ID] Represents the Identifier of the TODO

[M] Can appear or not, depending on the fact that the TODO is an "Extended Memo"

Title is simply the title of the TODO


### Extended Memos
An "Extended Memo" is something a bit more complex than a simple TODO, it can keep notes about the matter you're treating.

To Create an "Extended Memo", just create a normal TODO and then edit the "Message" part of the JSON via `todo e <id>`.
`todo list` will remind you that a TODO is an "Extended Memo" by placing the `[M]` mark on its line.

### Implementation Details
aTODO just creates a JSON file called .todo, placed inside your /home directory.

### Usage Examples
- `todo a` Simply creates a new TODO, you can then insert "Buy Milk" in "Title" and nothing in "message"
- `todo e 2` Edits the TODO with ID "2", making the "Message" value different from empty will make the TODO an "Extended Memo"
- `todo d 4` Deletes the TODO with ID "4"
- `todo` Lists the existing TODOs
- `todo v 1` Shows all the details of the TODO with ID "1", this will show the "Message" value too, if the TODO is an "Extended Memo"

### Conky Example
```
${font DejaVu Sans Mono:size=10}TODOs:${font DejaVu Sans Mono:size=8}
${execpi 600 python3 "/path/to/todo.py"}
```
