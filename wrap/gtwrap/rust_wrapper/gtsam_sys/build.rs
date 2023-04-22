use std::path::PathBuf;
use autocxx_build::Builder;

fn main() -> miette::Result<()> {
    // Setup files and dirs
    let build_file = PathBuf::from("src/lib.rs");
    let gtsam_dir = PathBuf::from("../../../../");//.canonicalize().unwrap();
    let lib_dir = gtsam_dir.join("install/lib");
    let lib_file = "libgtsamDebug.lib";
    let include_dir = gtsam_dir.join("install/include");
    let file = include_dir.join("gtsam/geometry/Point2.h");
    dbg!(include_dir.exists());
    dbg!(file.exists());
    println!("cargo:rustc-link-search=native={}", lib_dir.display());
    println!("cargo:rustc-link-lib=static={}", lib_file);
    let mut builder = Builder::new(&build_file, &[&include_dir]).custom_gendir(PathBuf::from("gen")).build()?;
    builder
        .include(&include_dir)
        .flag_if_supported("-std=c++14")
        .compile("gtsam_sys_ffi");
    println!("cargo:rerun-if-changed={}", build_file.display());
    Ok(())
}