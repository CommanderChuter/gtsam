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
        if self.name in self.original.parent.name:
            self.path = Path(self.top) / original.relative_to(root).parent
        else:
            self.path = Path(self.top) / (original.relative_to(root).parent / self.name)
        self.interface_file = self.path / (self.name+".i")
        self.cpp_file = self.path / (self.name+".cpp")
        self.rust_file = self.path / (self.name+".rs")
        self.namespace_file = self.path / (self.name+".namespace")
 
    def __repr__(self):
        return "{}::{}\n\t{}\n\t{}".format(self.top, self.name, self.path, self.original)
    

class ParseResults():

    def __init__(self):
        self.rs: str = ""
        self.cpp: str = ""
        self.ns: list[str] = []

 
def parse_file(namespace:parser.Namespace) -> ParseResults:
    rr = ParseResults()
    if namespace.name != "":
        log.error("Pass in file level namespace, not " + namespace.name)
        raise Exception
 
    # Setup module file
    rr.rs += "use autocxx::prelude::*;\n"
    rr.rs += "\n"
    rr.rs += "include_cpp! {\n"
 
    # The only thing in file namespace should be other namespaces
    for each in namespace.content:
        if not isinstance(each, parser.Namespace):
            log.warning("Only expecting namespaces in top level, found " + str(type(each)))
            raise Exception
        else:
            parse_namespace(each, rr)

    rr.rs += "safety!(unsafe)\n"
    rr.rs += "}\n"

    rr.rs = pretty_brackets(rr.rs)

    return rr
 
def parse_namespace(namespace:parser.Namespace, rr:ParseResults):
    # Add namespace to ns
    rr.ns.append(namespace.name)
 
    for each in namespace.content:
        if   isinstance(each, parser.Namespace):
            parse_namespace(each, rr)
        elif isinstance(each, parser.Include):
            parse_include(each, rr)
        elif isinstance(each, instantiator.InstantiatedGlobalFunction):
            parse_global_function(each, rr)
        elif isinstance(each, instantiator.InstantiatedClass):
            parse_class(each, rr)
 
 
    # Remove namespace from ns
    rr.ns.pop()
 
def parse_include(include:parser.Include, rr: ParseResults):
    rr.rs += "#include \"{}\"\n".format(include.header)
    #rr.rs += "\n"
 
def parse_global_function(func:instantiator.InstantiatedGlobalFunction, rr: ParseResults):
    # Add Namespace
    ns = "::".join(rr.ns)
    rr.rs += "generate!(\"{}\")\n".format(ns+func.name)
    #rr.rs += "\n"

def parse_class(cls:instantiator.InstantiatedClass, rr: ParseResults):
    # Add Namespace
    ns = "::".join(rr.ns)
    rr.rs += "generate!(\"{}\")\n".format(ns+cls.name)
    #rr.rs += "\n"
 
def main():
    # Set up logging
    log.basicConfig(
        level=log.INFO,
        format="%(levelname)s::%(lineno)d\n%(message)s\n"
    )
 
    ## Set running folder to rust folder
    if Path(os.getcwd()) != Path(pwd_dir):
        os.chdir(pwd_dir)

    ## Setup and Clean temp dir
    gtsam_dir = Path("gtsam")
    if gtsam_dir.exists():
        shutil.rmtree(gtsam_dir)
    gtsam_dir.mkdir()
 
    ## Collect interface files
    gtsam_src_dir = root_dir / "gtsam"
    modules: list[InterfaceModule] = []
    #for root, dirs, files in os.walk(gtsam_src_dir):
    #    for file in files:
    #        if file.endswith(".i"):
    #            module = InterfaceModule(Path(root) / file, gtsam_src_dir)
    #            modules.append(module)
    #            log.debug(module)
    modules.append(InterfaceModule(gtsam_src_dir/"geometry"/"geometry.i", gtsam_src_dir))
 
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
        results = parse_file(namespace)
 
        with open(module.rust_file, 'w') as file:
            file.write(results.rs)
        with open(module.cpp_file, 'w') as file:
            file.write(results.cpp)
 
 
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