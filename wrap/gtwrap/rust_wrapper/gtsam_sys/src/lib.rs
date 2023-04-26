use autocxx::prelude::*;

//////////////
// geometry //
//////////////

include_cpp! {
	#include "gtsam/geometry/Point2.h"
	#include "gtsam/geometry/StereoPoint2.h"
	#include "gtsam/geometry/Point3.h"
	#include "gtsam/geometry/Rot2.h"
	#include "gtsam/geometry/SO3.h"
	#include "gtsam/geometry/SO4.h"
	#include "gtsam/geometry/SOn.h"
	#include "gtsam/geometry/Quaternion.h"
	#include "gtsam/geometry/Rot3.h"
	#include "gtsam/geometry/Pose2.h"
	#include "gtsam/geometry/Pose3.h"
	#include "gtsam/geometry/Unit3.h"
	#include "gtsam/geometry/EssentialMatrix.h"
	#include "gtsam/geometry/Cal3_S2.h"
	#include "gtsam/geometry/Cal3DS2_Base.h"
	#include "gtsam/geometry/Cal3DS2.h"
	#include "gtsam/geometry/Cal3Unified.h"
	#include "gtsam/geometry/Cal3Fisheye.h"
	#include "gtsam/geometry/Cal3_S2Stereo.h"
	#include "gtsam/geometry/Cal3Bundler.h"
	#include "gtsam/geometry/CalibratedCamera.h"
	#include "gtsam/geometry/PinholeCamera.h"
	#include "gtsam/geometry/SimpleCamera.h"
	#include "gtsam/geometry/PinholePose.h"
	#include "gtsam/geometry/Similarity2.h"
	#include "gtsam/geometry/Similarity3.h"
	#include "gtsam/geometry/StereoCamera.h"
	#include "gtsam/geometry/triangulation.h"
	#include "gtsam/geometry/BearingRange.h"
	generate!("gtsamPoint2")
	generate!("gtsamPoint2Pairs")
	generate!("gtsamPoint2Vector")
	generate!("gtsamStereoPoint2")
	generate!("gtsamPoint3")
	generate!("gtsamPoint3Pairs")
	generate!("gtsamRot2")
	generate!("gtsamSO3")
	generate!("gtsamSO4")
	generate!("gtsamSOn")
	generate!("gtsamQuaternion")
	generate!("gtsamRot3")
	generate!("gtsamPose2")
	generate!("gtsamPose3")
	generate!("gtsamPose3Pairs")
	generate!("gtsamPose3Vector")
	generate!("gtsamUnit3")
	generate!("gtsamEssentialMatrix")
	generate!("gtsamCal3_S2")
	generate!("gtsamCal3DS2_Base")
	generate!("gtsamCal3DS2")
	generate!("gtsamCal3Unified")
	generate!("gtsamCal3Fisheye")
	generate!("gtsamCal3_S2Stereo")
	generate!("gtsamCal3Bundler")
	generate!("gtsamCalibratedCamera")
	generate!("gtsamSimilarity2")
	generate!("gtsamSimilarity3")
	generate!("gtsamStereoCamera")
	generate!("gtsamTriangulationResult")
	generate!("gtsamTriangulationParameters")
	generate!("gtsamtriangulatePoint3")
	generate!("gtsamtriangulatePoint3")
	generate!("gtsamtriangulateNonlinear")
	generate!("gtsamtriangulateNonlinear")
	generate!("gtsamtriangulateSafe")
	generate!("gtsamtriangulatePoint3")
	generate!("gtsamtriangulatePoint3")
	generate!("gtsamtriangulateNonlinear")
	generate!("gtsamtriangulateNonlinear")
	generate!("gtsamtriangulateSafe")
	generate!("gtsamtriangulatePoint3")
	generate!("gtsamtriangulatePoint3")
	generate!("gtsamtriangulateNonlinear")
	generate!("gtsamtriangulateNonlinear")
	generate!("gtsamtriangulateSafe")
	generate!("gtsamtriangulatePoint3")
	generate!("gtsamtriangulatePoint3")
	generate!("gtsamtriangulateNonlinear")
	generate!("gtsamtriangulateNonlinear")
	generate!("gtsamtriangulateSafe")
	generate!("gtsamtriangulatePoint3")
	generate!("gtsamtriangulatePoint3")
	generate!("gtsamtriangulateNonlinear")
	generate!("gtsamtriangulateNonlinear")
	generate!("gtsamtriangulateSafe")
	generate!("gtsamPinholeCameraCal3_S2")
	generate!("gtsamPinholeCameraCal3DS2")
	generate!("gtsamPinholeCameraCal3Unified")
	generate!("gtsamPinholeCameraCal3Bundler")
	generate!("gtsamPinholeCameraCal3Fisheye")
	generate!("gtsamPinholePoseCal3_S2")
	generate!("gtsamPinholePoseCal3DS2")
	generate!("gtsamPinholePoseCal3Unified")
	generate!("gtsamPinholePoseCal3Bundler")
	generate!("gtsamPinholePoseCal3Fisheye")
	generate!("gtsamBearingRange2D")
	generate!("gtsamBearingRangePose2")
	generate!("gtsamBearingRange3D")
	generate!("gtsamBearingRangePose3")
	safety!(unsafe)
}

