use autocxx_build::Builder;
use std::path::PathBuf;

fn main() -> miette::Result<()> {
    // Setup files and dirs
    let build_file = PathBuf::from("src/lib.rs");
    let gtsam_dir = PathBuf::from("../../../../"); //.canonicalize().unwrap();
                                                   //let lib_dir = gtsam_dir.join("install/lib");
                                                   //let lib_file = "libgtsamDebug.lib";
    let include_dir = gtsam_dir.join("install/include");
    let eigen_dir = gtsam_dir.join("../eigen");
    //println!("cargo:rustc-link-search=native={}", lib_dir.display());
    //println!("cargo:rustc-link-lib=static={}", lib_file);
    let auto_builder = Builder::new(&build_file, &[&include_dir, &eigen_dir])
        //.custom_gendir(PathBuf::from("gen"))
        .extra_clang_args(&["-std=c++17"]);
    let mut _cc_builder = auto_builder.build()?;
    /*cc_builder
    .include(&include_dir)
    .flag("/std:c++17")
    .compile("gtsam_sys_ffi");*/
    println!("cargo:rerun-if-changed={}", build_file.display());
    Ok(())
}
