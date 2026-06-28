#ifndef MANUAL_BENCHMARK_H
#define MANUAL_BENCHMARK_H

#include "benchmark.h"

class ManualBenchmark : public Benchmark {
public:
    ManualBenchmark(
        uint32_t nWifis, double txpDistance, double nodeSpeed,
        bool appLogging, uint32_t packetSize, uint32_t hopCount,
        uint32_t queueLength, Time queueEntryExpireTime,
        Time beaconInterval
    );

    void run();
    friend std::ostream& operator<<(std::ostream& os, ManualBenchmark &b);
};

#endif
