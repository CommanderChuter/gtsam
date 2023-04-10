#!/usr/bin/env python3
"""
GTSAM Copyright 2010-2020, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved

See LICENSE for the license information

Code generator for wrapping a C++ module for Rust
Author: Duy Nguyen Ta, Fan Jiang, Matthew Sklar, Varun Agrawal, Frank Dellaert, and Ryker Chute
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
        self.symbols = {}

    def __repr__(self):
        return "{}::{}\n\t{}\n\t{}".format(self.top, self.name, self.path, self.original)
    
class Symbol():
    def __init__(self, obj):
        self.name = repr(obj)
        self.status = False
        self.obj = obj

    def __repr__(self) -> str:
        return self.name
        

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
    modules = []
    for root, dirs, files in os.walk(gtsam_dir):
        for file in files:
            if file.endswith(".i"):
                module = InterfaceModule(Path(root) / file, gtsam_dir)
                modules.append(module)
                log.debug(module)
    
    ## Instaniate Symbol database
    symboldb = {}

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
        ns_raw = str(namespace)
        ns_tab = ""
        tab = 0
        for line in ns_raw.splitlines():
            if line.count("}"):
                tab -= line.count("}")
            ns_tab += (("\t"*tab)+line+"\n")
            if line.count("{"):
                tab += line.count("{")
        with open(module.namespace_file, "w") as file:
            file.write(ns_tab)

        ## Add to symbols to database
        symboldb[module.name] = {}

        # Recursivly look through symbols in parse
        def recurs(obj, db):
            def foreach(obj, db):
                for each in obj:
                    recurs(each, db)

            id = repr(obj)
            
            if   isinstance(obj, parser.Namespace):
                if obj.name == "":
                    foreach(obj.content, db)
                else:
                    db[id] = {}
                    foreach(obj.content, db[id])
            elif isinstance(obj, parser.Class):
                db[id] = {}
                foreach(obj.ctors, db[id])
                foreach(obj.methods, db[id])
                foreach(obj.static_methods, db[id])
                foreach(obj.properties, db[id])
                foreach(obj.operators, db[id])
                foreach(obj.enums, db[id])
                foreach(obj.properties, db[id])
            else:
                db[id] = Symbol(obj)

        recurs(namespace, symboldb[module.name])
        module.symbols = symboldb[module.name]

        ## If symbol supported, generate
        

            ## If Function

                ## cxx

            ## If Class

                ## c++ constructor, destructor

                ## cxx methods and members

        ## Else, record failure
        
#TODO: interface script in wrap/scripts
if __name__ == "__main__":
    main()