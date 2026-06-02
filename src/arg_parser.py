from lark import Lark, Transformer


GRAMMAR = r"""
start: command

command: mkdir
       | cp
       | mv
       | touch
       | rm
       | cat
       | write
       | cd
       | ls

mkdir: "mkdir" path
cp: "cp" path path
mv: "mv" path path
touch: "touch" path

rm: rm_file
  | rm_recursive
  
rm_file: "rm" path
rm_recursive: "rm" "-r" path

cat: "cat" path

write: "write" path

cd: "cd" path

ls: "ls"
  | "ls" path

path: PATH

PATH: /[^\s]+/

%import common.WS
%ignore WS
"""


class CommandTransformer(Transformer):

    def start(self, items):
        return items[0]

    def command(self, items):
        return items[0]

    def rm(self, items):
        return items[0]

    def mkdir(self, items):
        return {
            "command": "mkdir",
            "path": str(items[0])
        }

    def cp(self, items):
        return {
            "command": "cp",
            "source": str(items[0]),
            "destination": str(items[1])
        }

    def mv(self, items):
        return {
            "command": "mv",
            "source": str(items[0]),
            "destination": str(items[1])
        }

    def touch(self, items):
        return {
            "command": "touch",
            "path": str(items[0])
        }

    def rm_file(self, items):
        return {
            "command": "rm",
            "recursive": False,
            "path": str(items[0])
        }

    def rm_recursive(self, items):
        return {
            "command": "rm",
            "recursive": True,
            "path": str(items[0])
        }

    def cat(self, items):
        return {
            "command": "cat",
            "path": str(items[0])
        }

    def write(self, items):
        return {
            "command": "write",
            "path": str(items[0])
        }

    def cd(self, items):
        return {
            "command": "cd",
            "path": str(items[0])
        }

    def ls(self, items):
        return {
            "command": "ls",
            "path": str(items[0]) if items else None
        }

    def path(self, items):
        return items[0]

    def text(self, items):
        return items[0]