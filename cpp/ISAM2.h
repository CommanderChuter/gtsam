/**
 * @file    ISAM2.h
 * @brief   Incremental update functionality (ISAM2) for BayesTree, with fluid relinearization.
 * @author  Michael Kaess
 */

// \callgraph

#pragma once

#include <map>
#include <list>
#include <vector>
#include <boost/serialization/map.hpp>
#include <boost/serialization/list.hpp>
#include <stdexcept>

#include "Testable.h"
#include "FactorGraph.h"
#include "NonlinearFactorGraph.h"
#include "BayesNet.h"
#include "BayesTree.h"
#include "Key.h"

namespace gtsam {

	typedef std::map<Symbol, GaussianFactor::shared_ptr> CachedFactors;

	template<class Conditional, class Config>
	class ISAM2: public BayesTree<Conditional> {

	protected:

		// current linearization point
		Config theta_;

		// for keeping all original nonlinear factors
		NonlinearFactorGraph<Config> nonlinearFactors_;

		// cached intermediate results for restarting computation in the middle
		CachedFactors cached_;

		// variables that have been updated, requiring the corresponding factors to be relinearized
		std::list<Symbol> marked_;

	public:

		/** Create an empty Bayes Tree */
		ISAM2();

		/** Create a Bayes Tree from a Bayes Net */
		ISAM2(const NonlinearFactorGraph<Config>& fg, const Ordering& ordering, const Config& config);

		/** Destructor */
		virtual ~ISAM2() {
		}

		typedef typename BayesTree<Conditional>::sharedClique sharedClique;

		typedef typename BayesTree<Conditional>::Cliques Cliques;

		/**
		 * ISAM2. (update_internal provides access to list of orphans for drawing purposes)
		 */
		void update_internal(const NonlinearFactorGraph<Config>& newFactors,
				const Config& config, Cliques& orphans,
				double wildfire_threshold, double relinearize_threshold);
		void update(const NonlinearFactorGraph<Config>& newFactors, const Config& config,
				double wildfire_threshold = 0., double relinearize_threshold = 0.);

		const Config estimate() const {return theta_;}

	private:

		boost::shared_ptr<FactorGraph<NonlinearFactor<Config> > > getAffectedFactors(const std::list<Symbol>& keys) const;
		FactorGraph<GaussianFactor> relinearizeAffectedFactors(const std::list<Symbol>& affectedKeys) const;
		FactorGraph<GaussianFactor> getCachedBoundaryFactors(Cliques& orphans);

	}; // ISAM2

} /// namespace gtsam
