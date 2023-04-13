#!/usr/bin/env python3
"""
GTSAM Copyright 2010-2020, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved

See LICENSE for the license information

Code generator for wrapping a C++ module for Rust
Author: Ryker Chute
"""

import os
import shutil
import logging as log
from pathlib import Path
import json

import sys
pwd_dir = Path(__file__).parent.resolve()
wrap_dir = pwd_dir.parent.parent
root_dir = wrap_dir.parent
sys.path.append(str(wrap_dir))
from gtwrap import interface_parser as parser
from gtwrap import template_instantiator as instantiator


class InterfaceModule():

    def __init__(self, original:Path, root:Path):
        self.original = original
        self.name = original.name.replace(".i", "")
        self.top = root.name
        self.path = Path(self.top) / original.relative_to(root).parent
        self.interface_file = self.path / (self.name+".i")
        self.cpp_file = self.path / (self.name+".cpp")
        self.rust_file = self.path / (self.name+".rs")
        self.namespace_file = self.path / (self.name+".namespace")


    def __repr__(self):
        return "{}::{}\n\t{}\n\t{}".format(self.top, self.name, self.path, self.original)


def parse_file(namespace:parser.Namespace):
    rsf = ""
    cpf = ""
    ns: list[str] = []
    if namespace.name is not "":
        log.error("Pass in file level namespace, not " + namespace.name)
        raise Exception

    # Setup module file
    rsf += "mod ffi {\n"
    rsf += "unsafe extern \"C++\" {\n"

    # The only thing in file namespace should be other namespaces
    for each in namespace.content:
        if isinstance(each, parser.Namespace):
            log.warning("Only expecting namespaces in top level, found " + type(each))
            raise Exception
        else:
            parse_namespace(each, rsf, cpf, ns)

    rsf += "}\n}\n"

    return pretty_brackets(rsf), cpf

def parse_namespace(namespace:parser.Namespace, rsf:str, cpf:str, ns: list):
    # Add namespace to ns
    ns.append(namespace.name)

    # Setup rust file
    rsf += "#[namespace = \"\"]\n"
    rsf += "unsafe extern \"C++\" {\n"

    for each in namespace.content:
        if   isinstance(each, parser.Namespace):
            parse_namespace(each, rsf, cpf, ns)
        elif isinstance(each, parser.Include):
            parse_include(each, rsf, cpf, ns)
        elif isinstance(each, )


    # Remove namespace from ns
    ns.pop()

def parse_include(include:parser.Include, rsf:str, cpf:str, ns:list):
    rsf += "include!({})\n".format(include.header)

def main():
    # Set up logging
    log.basicConfig(
        level=log.INFO,
        format="%(levelname)s::%(lineno)d\n%(message)s\n"
    )

    ## Set running folder to rust folder
    gtsam_dir = root_dir / "gtsam"
    if Path(os.getcwd()) != Path(pwd_dir):
        os.chdir(pwd_dir)
        
    ## Collect interface files
    modules: list[InterfaceModule] = []
    for root, dirs, files in os.walk(gtsam_dir):
        for file in files:
            if file.endswith(".i"):
                module = InterfaceModule(Path(root) / file, gtsam_dir)
                modules.append(module)
                log.debug(module)

    ## For each interface file
    for module in modules:

        log.info(module)

        ## Create file/folder tree
        module.path.mkdir(parents=True, exist_ok=True)
        shutil.copy(module.original, module.path)

        ## Parse file
        with open(module.interface_file, "r") as file:
            content = file.read()
        namespace:parser.Namespace = parser.Module.parseString(content)
        instantiator.instantiate_namespace(namespace)

        # Dump namespace to file with tabs
        ns_tab = pretty_brackets(str(namespace))
        with open(module.namespace_file, "w") as file:
            file.write(ns_tab)

        ## Generate file strings
        rs_str, cxx_str = parse_file(namespace)

        with open(module.rust_file, 'w') as file:
            file.write(rs_str)
        with open(module.cpp_file, 'w') as file:
            file.write(cxx_str)


def pretty_brackets(input: str) -> str:
    output = ""
    tab = 0
    for line in input.splitlines():
        if line.count("}"):
            tab -= line.count("}")
        output += (("\t"*tab)+line+"\n")
        if line.count("{"):
            tab += line.count("{")
    return output

#TODO: interface script in wrap/scripts
if __name__ == "__main__":
    main()