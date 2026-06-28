#include "benchmark/queue-length-benchmark.h"
#include "benchmark/hop-count-benchmark.h"
#include "benchmark/node-count-benchmark.h"
#include "benchmark/manual-benchmark.h"
#include <iostream>

using namespace ns3;

int main(int argc, char* argv[])
{
    uint32_t nWifis = 50;
    uint32_t queueLength = 2000;
    double txpDistance = 50.0;
    double nodeSpeed = 10.0;
    bool appLogging = false;

    uint32_t packetSize = 1024;

    uint32_t hopCount = 50;
    Time queueEntryExpireTime = Seconds(1000);
    Time beaconInterval = Seconds(5);

    bool queueLengthBenchmark = false;
    uint32_t maxQueueLength = 2000;
    uint32_t queueStep = 100;

    bool hopCountBenchmark = false;
    uint32_t maxHopCount = 50;
    uint32_t hopCountStep = 1;

    bool nodeCountBenchmark = true;
    uint32_t minNodes = 5;
    uint32_t maxNodes = 50;
    uint32_t nodeStep = 5;

    
    
    
    
    
	bool manualBenchmark = false;
    CommandLine cmd;
    cmd.Usage("Epidemic routing benchmark scenario.");

    cmd.AddValue("nWifis", "Number of Wifi nodes/devices", nWifis);
    cmd.AddValue("appLogging", "Tell applications to log if true", appLogging);
    cmd.AddValue("nodeSpeed", "Node speed in RandomWayPoint model", nodeSpeed);
    cmd.AddValue("packetSize", "The packet size", packetSize);
    cmd.AddValue("txpDistance", "Specify node transmit range", txpDistance);
    cmd.AddValue("hopCount", "Specify number of hopCount", hopCount);
    cmd.AddValue("queueLength", "Specify default queueLength", queueLength);
    cmd.AddValue("queueEntryExpireTime", "Specify queue Entry Expire Time", queueEntryExpireTime);
    cmd.AddValue("beaconInterval", "Specify beaconInterval", beaconInterval);

    cmd.AddValue("queueLengthBenchmark", "Run QueueLengthBenchmark if true", queueLengthBenchmark);
    cmd.AddValue("maxQueueLength", "Specify maxQueueLength", maxQueueLength);
    cmd.AddValue("queueStep", "Specify queueStep", queueStep);

    cmd.AddValue("hopCountBenchmark", "Run HopCountBenchmark if true", hopCountBenchmark);
    cmd.AddValue("maxHopCount", "Specify maxHopCount", maxHopCount);
    cmd.AddValue("hopCountStep", "Specify hopCountStep", hopCountStep);

    cmd.AddValue("nodeCountBenchmark", "Run NodeCountBenchmark if true", nodeCountBenchmark);
    cmd.AddValue("minNodes", "Minimum number of nodes", minNodes);
    cmd.AddValue("maxNodes", "Maximum number of nodes", maxNodes);
    cmd.AddValue("nodeStep", "Node step", nodeStep);


    cmd.Parse(argc, argv);

    if (queueLengthBenchmark)
    {
        std::cout << "###### QUEUE LENGTH BENCHMARK #####" << std::endl;

        QueueLengthBenchmark qlb(
            nWifis, txpDistance, nodeSpeed, appLogging, packetSize,
            hopCount, queueLength, queueEntryExpireTime, beaconInterval,
            maxQueueLength, queueStep
        );

        std::cout << qlb << std::endl;
        qlb.run();
    }

    if (hopCountBenchmark)
    {
        std::cout << "###### HOP COUNT BENCHMARK #####" << std::endl;

        HopCountBenchmark hcb(
            nWifis, txpDistance, nodeSpeed, appLogging, packetSize,
            hopCount, queueLength, queueEntryExpireTime, beaconInterval,
            maxHopCount, hopCountStep
        );

        std::cout << hcb << std::endl;
        hcb.run();
    }

    if (nodeCountBenchmark)
    {
        std::cout << "###### NODE COUNT BENCHMARK #####" << std::endl;

        NodeCountBenchmark ncb(
            nWifis, txpDistance, nodeSpeed, appLogging, packetSize,
            hopCount, queueLength, queueEntryExpireTime, beaconInterval,
            minNodes, maxNodes, nodeStep
        );

        std::cout << ncb << std::endl;
        ncb.run();
    }

  
if (manualBenchmark)
{
    std::cout << "###### MANUAL BENCHMARK #####" << std::endl;

    ManualBenchmark mb(
        nWifis,
        txpDistance,
        nodeSpeed,
        appLogging,
        packetSize,
        hopCount,
        queueLength,
        queueEntryExpireTime,
        beaconInterval
    );

    std::cout << mb << std::endl;
    mb.run();
}
    return 0;
}
