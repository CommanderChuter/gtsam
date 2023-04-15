use autocxx::prelude::*;

//////////////
// geometry //
//////////////
//	generate!("gtsam::Point2")

include_cpp! {
	#include "gtsam/geometry/Point2.h"
	safety!(unsafe)
}

