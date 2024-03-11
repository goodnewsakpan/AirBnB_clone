#!/usr/bin/python3
"""
This module represents a commandline
interpreter to manage the hbnb console
"""
from ast import literal_eval
import cmd

from models import classes, storage


class HBNBCommand(cmd.Cmd):
    """
    This class represents a commandline
    interpreter to manage the hbnb console
    """
    prompt = "(hbnb) "

    def emptyline(self):
        """Called when an empty line is passed"""
        pass

    def do_quit(self, _):
        """quit command to exit the interpreter"""
        return True

    def do_EOF(self, _):
        """End of file command to exit the interpreter"""

        return True

    def do_create(self, model):
        """create command to create a new instance of a specific model"""

        print(model)
        if not self.checker(model, ["n", 'ec']):
            return
        ins = classes[model]()
        ins.save()
        print(ins.id)

    def do_show(self, model):
        """show command to display information about a specific instance"""

        if not self.checker(model, ["n", "l", "ec", "es"]):
            return
        cls, key = model.split()
        print(classes[cls].show(key))

    def do_destroy(self, model):
        """destroy command to remove a specific instance"""

        if not self.checker(model, ["n", "l", "ec", "es"]):
            return
        cls, key = model.split()
        classes[cls].destroy(key)

    def do_all(self, model):
        """
        all command to display all instances of a specific model or
        all instances across all models if none is
        specified
        """

        if model and not self.checker(model, ["ec"]):
            return
        if model:
            print(classes[model].all())
        else:
            print(storage.get_all())

    def do_update(self, model):
        """update command to modify an instance attribute value"""

        keys = ["n", "l", "ec", "es", "a", "v"]
        if not self.checker(model, keys):
            return
        extras = model.split()
        classes[extras[0]].update(extras[1], extras[2], extras[3])

    def default(self, line):
        """
        default command to handle all other
        commands not explicitly defined
        """

        parse = self.parse_command(line)
        if parse:
            if not self.checker(parse[0], ["ec"]):
                return
            if len(parse) == 3:
                model = " ".join([parse[0], *parse[2]])
                if not self.checker(model, ["ec", "es"]):
                    return
                method = getattr(classes[parse[0]], parse[1])
                value = method(*parse[2])
            else:
                method = getattr(classes[parse[0]], parse[1])
                value = method()
            if value:
                print(value)

    @staticmethod
    def parse_command(line):
        """parse the command entered by the user"""

        parts = line.split('.')
        if len(parts) == 2 and parts[1].endswith(')'):
            cls = parts[0]
            parts = parts[1].split("(")
            if len(parts) == 2:
                method = parts[0]
                parts = parts[1].rstrip(")")
                if not parts:
                    return cls, method
                args = [literal_eval(i.strip()) for i in parts.split(",")]
                return cls, method, args
            return cls, parts[0]
        else:
            return None

    @staticmethod
    def checker(model, keys):
        """checks if the model string contains any of the specified keys"""

        part = model.split()
        if "n" in keys and not model:
            print("** class name missing **")
            return False
        if "l" in keys and len(model.split()) < 2:
            print("** instance id missing **")
            return False
        if "ec" in keys and part[0] not in classes:
            print("** class doesn't exist **")
            return False
        if "es" in keys and ".".join(part[0:2]) not in storage.all():
            print("** no instance found **")
            return False
        if "a" in keys and len(model.split()) < 3:
            print("** attribute name missing **")
            return
        if "v" in keys and len(model.split()) < 4:
            print("** value missing **")
            return
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
