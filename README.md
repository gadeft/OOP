# The simulated file system

It has CLI to work with. The created file system is not
preserved in your own file system on your PC. The program 
does not store it anywhere. 

The emulated file system is initialized every time you run
`main.py` file.

## Supported commads

```
<> - arguments
[] - optionals

mkdir <path> # creates a directory
touch <path> # creates a file
ls [<path>] # list all items in a directory. If <path> is not specified it is percieved as a currend working directory
cat <path> # show a content of a file
mv <source path> <destination path> # moves a file or a directory
cp <source path> <destination path> # copies a file or a directory
write <path> # writes a content to file. The escape sequence is '\n'
rm [-r] <path> # deletes a file or a directory
cd <path> # changes the curreng working directory
```

## Dependencies

```
lark~=1.3.1
pydantic~=2.13.4
pathvalidate~=3.3.1
```