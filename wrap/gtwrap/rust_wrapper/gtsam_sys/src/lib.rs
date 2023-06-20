use autocxx::prelude::*;

//////////////
// geometry //
//////////////
//#include "gtsam/dllexport.h"
//	generate!("gtsam::Point2")
//generate!("gtsam::Point2")

include_cpp! {
    #include "gtsam/geometry/Point2.h"
    generate!("gtsam::Point2")
    safety!(unsafe)
}
