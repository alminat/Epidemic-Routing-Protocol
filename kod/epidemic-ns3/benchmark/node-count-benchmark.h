#ifndef NODE_COUNT_BENCHMARK_H
#define NODE_COUNT_BENCHMARK_H

#include "benchmark.h"

class NodeCountBenchmark : public Benchmark {
public:
    uint32_t minNodes;
    uint32_t maxNodes;
    uint32_t nodeStep;

    NodeCountBenchmark(
        uint32_t nWifis, double txpDistance, double nodeSpeed,
        bool appLogging, uint32_t packetSize, uint32_t hopCount,
        uint32_t queueLength, Time queueEntryExpireTime,
        Time beaconInterval, uint32_t minNodes,
        uint32_t maxNodes, uint32_t nodeStep
    );

    void run();
    friend std::ostream& operator<<(std::ostream& os, NodeCountBenchmark &b);
};

#endif

