from ast import literal_eval
from cmd import Cmd

from models import classes, storage


class HBNBCommand(Cmd):
    prompt = "(hbnb)"

    def do_quit(self, _):
        return True

    def do_EOF(self, _):
        return True

    def do_create(self, model):
        print(model)
        if not self.checker(model, ["n", 'ec']):
            return
        ins = classes[model]()
        ins.save()
        print(ins.id)

    def do_show(self, model):
        if not self.checker(model, ["n", "l", "ec", "es"]):
            return
        cls = model.split()[0]
        key = model.replace(' ', '.')
        print(classes[cls].show(key))

    def do_destroy(self, model):
        if not self.checker(model, ["n", "l", "ec", "es"]):
            return
        cls = model.split()[0]
        key = model.replace(' ', '.')
        classes[cls].destroy(key)

    def do_all(self, model):
        if model and not self.checker(model, ["ec"]):
            return
        print(classes[model].all())

    def do_update(self, model):
        if not self.checker(model, ["n", "l", "ec", "es", "a", "v"]):
            return
        extras = model.split()
        classes[extras[0]].update(extras[1], extras[2], extras[3])

    def default(self, line):
        parse = self.parse_command(line)
        if parse:
            if not self.checker(parse[0], ["ec"]):
                return
            if len(parse) == 3:
                if not self.checker(" ".join([parse[0], *parse[2]]), ["ec", "es"]):
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
        parts = line.split('.')
        if len(parts) == 2 and parts[1].endswith(')'):
            cls = parts[0]
            parts = parts[1].split("(")
            if len(parts) == 2:
                method = parts[0]
                parts = parts[1].rstrip(")")
                if not parts:
                    return cls, method
                args = [literal_eval(i) for i in parts.split()]
                return cls, method, args
            return cls, parts[0]
        else:
            return None

    @staticmethod
    def checker(model, keys):
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
