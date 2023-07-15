#!/usr/bin/python3
"""program called console.py that contains
the entry point of the command interpreter"""
import cmd
from models.base_model import BaseModel
from models import storage
import ast


class HBNBCommand(cmd.Cmd):
    """class HBNBCommand"""
    prompt = '(hbnb) '

    def do_quit(self, line):
        """Exit the program\n"""
        return True

    def do_create(self, line):
        """Creates an instance\n"""
        classes = storage.classes()
        if line is None or line == "":
            print("** class name missing **")
        elif line not in classes:
            print("** class doesn't exist **")
        else:
            new_class = classes[line]()
            new_class.save()
            print(new_class.id)

    def do_show(self, line):
        """Prints the string representation of
an instance based on the class name and id\n"""
        if line is None or line == "":
            print("** class name missing **")
        else:
            a = line.split(' ')
            if a[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(a) < 2:
                print("** instance id missing **")
            else:
                instance = f"{a[0]}.{a[1]}"
                if instance not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[instance])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id
(save the change into the JSON file)\n"""
        if line is None or line == "":
            print("** class name missing **")
        else:
            a = line.split(' ')
            if a[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(a) < 2:
                print("** instance id missing **")
            else:
                instance = f"{a[0]}.{a[1]}"
                if instance not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[instance]
                    storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances
based or not on the class name\n"""
        if '.' in line:
            line = line.replace('.', ' ')
            if '(' or ')' in line:
                line = line.replace('(', '').replace(')', '')
            line = line.split(' ')
            line = f"{line[1]} {line[0]}"
        list = []
        if line == "" or line is None:
            for key, value in storage.all().items():
                list.append(str(value))
            print(list)
        else:
            if line not in storage.classes():
                print("** class doesn't exist **")
            else:
                for key, value in storage.all().items():
                    if type(value).__name__ == line:
                        list.append(str(value))
                print(list)

    def do_update(self, line):
        """Updates an instance based on the class name and id
by adding or updating attribute\n"""
        if line is None or line == "":
            print("** class name missing **")
        else:
            a = line.split(' ')
            if a[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(a) < 2:
                print("** instance id missing **")
            else:
                inst = f"{a[0]}.{a[1]}"
                if inst not in storage.all():
                    print("** no instance found **")
                elif len(a) < 3:
                    print("** attribute name missing **")
                elif len(a) < 4:
                    print("** value missing **")
                else:
                    if a[2] in storage.check_class()[a[0]]:
                        a[3] = ast.literal_eval(a[3])
                        t = type(storage.check_class()[a[0]][a[2]])
                        try:
                            a[3] = t(a[3])
                        except Exception:
                            return
                    setattr(storage.all()[inst], a[2], a[3])
                    storage.save()

    def do_EOF(self, line):
        """Handle the End-of-File (EOF) character.\n"""
        print()
        return True

    def emptyline(self):

        """Ignore empty a."""
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
