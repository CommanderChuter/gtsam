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
import json
import pprint

from pathlib import Path

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
        self.interface = self.path / (self.name+".i")
        self.cpp = self.path / (self.name+".cpp")
        self.rust = self.path / (self.name+".rs")

    def __repr__(self):
        return "{}::{}\n\t{}\n\t{}".format(self.top, self.name, self.path, self.original)
        
    

def main():
    # Set up logging
    log.basicConfig(level=log.DEBUG, format="%(levelname)s::%(lineno)d\n%(message)s\n")

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

    ## For each interface file
    for module in modules:

        ## Create file/folder tree
        module.path.mkdir(parents=True, exist_ok=True)
        shutil.copy(module.original, module.path)

        ## Parse file
        with open(module.interface, "r", encoding="UTF-8") as file: #TODO: do we need the UTF-8?
            content = file.read()

        # parseString is sappose to return a pyparsing.ParseResult
        # but instead returns gtwrap.interface_parser.Namespace
        # example shows that being replaced because with
        # insatior.instantiate_namepsace
        # because that also returns Namespace
        # TLDR: parseString -> Namespace -> instantiate_namespace -> Namespace
        namespace = parser.Module.parseString(content)
        log.debug(namespace)
        namespace = instantiator.instantiate_namespace(namespace)
        log.debug(namespace)

        #wrapped_namespace, includes = self.wrap_namespace(module)

        #DEBUG
        exit()

        ## Add to Symbol database

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