use autocxx::prelude::*;

//////////////
// geometry //
//////////////

include_cpp! {
	#include "gtsam/geometry/Point2.h"
	generate!("gtsamPoint2")
	safety!(unsafe)
}