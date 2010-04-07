/*
 * Simulated2DConfig.h
 *
 * Re-created on Feb 22, 2010 for compatibility with MATLAB
 * Author: Frank Dellaert
 */

#pragma once

#include "simulated2DOriented.h"

namespace gtsam {

	class Simulated2DOrientedConfig: public simulated2DOriented::Config {
	public:
		typedef boost::shared_ptr<Point2> sharedPoint;
		typedef boost::shared_ptr<Pose2> sharedPose;

		Simulated2DOrientedConfig() {
		}

		void insertPose(const simulated2DOriented::PoseKey& i, const Pose2& p) {
			insert(i, p);
		}

		void insertPoint(const simulated2DOriented::PointKey& j, const Point2& p) {
			insert(j, p);
		}

		int nrPoses() const {
			return this->first_.size();
		}

		int nrPoints() const {
			return this->second_.size();
		}

		sharedPose pose(const simulated2DOriented::PoseKey& i) {
			return sharedPose(new Pose2((*this)[i]));
		}

		sharedPoint point(const simulated2DOriented::PointKey& j) {
			return sharedPoint(new Point2((*this)[j]));
		}

	};

} // namespace gtsam

