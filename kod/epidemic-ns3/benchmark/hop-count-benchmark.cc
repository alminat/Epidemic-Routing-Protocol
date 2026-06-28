#include "hop-count-benchmark.h"
#include <fstream>

HopCountBenchmark::HopCountBenchmark(
    uint32_t nWifis, double txpDistance, double nodeSpeed,
    bool appLogging, uint32_t packetSize, uint32_t hopCount,
    uint32_t queueLength, Time queueEntryExpireTime,
    Time beaconInterval, uint32_t maxHopCount, uint32_t hopCountStep)
    : Benchmark(nWifis, txpDistance, nodeSpeed, appLogging, packetSize,
                hopCount, queueLength, queueEntryExpireTime, beaconInterval)
{
    this->maxHopCount = maxHopCount;
    this->hopCountStep = hopCountStep;
}

void HopCountBenchmark::run()
{
    if (appLogging)
    {
        LogComponentEnable("OnOffApplication", LOG_LEVEL_INFO);
        LogComponentEnable("PacketSink", LOG_LEVEL_INFO);
        LogComponentEnableAll(LOG_PREFIX_TIME);
        LogComponentEnableAll(LOG_PREFIX_NODE);
        LogComponentEnableAll(LOG_PREFIX_FUNC);
    }

    std::string fileNameWithNoExtension = "data-loss-hop-count" + std::to_string(maxHopCount);
    std::string graphicsFileName = fileNameWithNoExtension + ".png";
    std::string plotFileName = fileNameWithNoExtension + ".plt";
    std::string plotTitle = "Relationship between hop count and packet loss";
    std::string dataTitle = "Packet Loss %";

    Gnuplot plot(graphicsFileName);
    plot.SetTitle(plotTitle);
    plot.SetTerminal("png size 1920,1080");
    plot.SetLegend("Hop Count", "Packet Loss %");

    std::stringstream extra;
    extra << "set xrange [0:" << maxHopCount << "]";
    plot.AppendExtra(extra.str());

    Gnuplot2dDataset dataset;
    dataset.SetTitle(dataTitle);
    dataset.SetStyle(Gnuplot2dDataset::LINES_POINTS);

    std::ofstream csvFile;
    csvFile.open("drugi_scenarij_hop_count.csv", std::ios::out);

    csvFile << "nWifis,queueLength,hopCount,benchmark,parameter,sent,received,lost,packet_loss,delivery_ratio,overhead\n";

    for (uint32_t currentHopCount = 1;
         currentHopCount <= maxHopCount;
         currentHopCount += hopCountStep)
    {
        std::string tag = "hopCount: " + std::to_string(currentHopCount);

        this->st.setTag(tag);
        this->st.setReceivedPackets(0);
        this->st.setSendedPackets(0);

        NodeContainer nodeContainer;
        NetDeviceContainer devices;
        nodeContainer.Create(nWifis);

        MobilityHelper mobility;

        mobility.SetPositionAllocator("ns3::RandomRectanglePositionAllocator",
                                      "X",
                                      StringValue("ns3::UniformRandomVariable[Min=0.0|Max=300.0]"),
                                      "Y",
                                      StringValue("ns3::UniformRandomVariable[Min=0.0|Max=1500.0]"));

        mobility.SetMobilityModel("ns3::SteadyStateRandomWaypointMobilityModel",
                                  "MinSpeed",
                                  DoubleValue(0.01),
                                  "MaxSpeed",
                                  DoubleValue(nodeSpeed),
                                  "MinX",
                                  DoubleValue(0.0),
                                  "MaxX",
                                  DoubleValue(300.0),
                                  "MinPause",
                                  DoubleValue(10),
                                  "MaxPause",
                                  DoubleValue(20),
                                  "MinY",
                                  DoubleValue(0.0),
                                  "MaxY",
                                  DoubleValue(1500.0));

        mobility.Install(nodeContainer);

        WifiMacHelper wifiMac;
        wifiMac.SetType("ns3::AdhocWifiMac");

        YansWifiPhyHelper wifiPhy;
        YansWifiChannelHelper wifiChannel = YansWifiChannelHelper::Default();

        wifiChannel.AddPropagationLoss("ns3::RangePropagationLossModel",
                                       "MaxRange",
                                       DoubleValue(txpDistance));

        wifiPhy.SetChannel(wifiChannel.Create());

        WifiHelper wifi;
        wifi.SetStandard(WIFI_STANDARD_80211a);
        wifi.SetRemoteStationManager("ns3::ConstantRateWifiManager",
                                     "DataMode",
                                     StringValue("OfdmRate6Mbps"),
                                     "RtsCtsThreshold",
                                     UintegerValue(0));

        devices = wifi.Install(wifiPhy, wifiMac, nodeContainer);

        EpidemicHelper epidemic;
        epidemic.Set("HopCount", UintegerValue(currentHopCount));
        epidemic.Set("QueueLength", UintegerValue(queueLength));
        epidemic.Set("QueueEntryExpireTime", TimeValue(queueEntryExpireTime));
        epidemic.Set("BeaconInterval", TimeValue(beaconInterval));

        Ipv4ListRoutingHelper list;
        InternetStackHelper internet;
        internet.SetRoutingHelper(epidemic);
        internet.Install(nodeContainer);

        Ipv4AddressHelper ipv4;
        ipv4.SetBase("10.1.1.0", "255.255.255.0");
        Ipv4InterfaceContainer interfaces = ipv4.Assign(devices);

        uint32_t num_source = 45;
        uint32_t num_sink = 45;

        for (uint32_t i = 0; i < num_sink; ++i)
        {
            PacketSinkHelper sink("ns3::UdpSocketFactory",
                                  InetSocketAddress(Ipv4Address::GetAny(), 80));

            ApplicationContainer apps_sink = sink.Install(nodeContainer.Get(i));

            Ptr<PacketSink> pktSink = StaticCast<PacketSink>(apps_sink.Get(0));

            std::stringstream ss;
            ss << "Sink Application Callback";

            pktSink->TraceConnect("Rx", ss.str(),
                                  MakeCallback(&HopCountBenchmark::SinkRxTrace, this));

            apps_sink.Start(Seconds(0.0));
            apps_sink.Stop(Seconds(TotalTime));
        }

        for (uint32_t source = 0; source < num_source; ++source)
        {
            for (uint32_t sink = 0; sink < num_sink; ++sink)
            {
                if (sink != source)
                {
                    OnOffHelper onoff1("ns3::UdpSocketFactory",
                                       Address(InetSocketAddress(interfaces.GetAddress(sink), 80)));

                    onoff1.SetConstantRate(DataRate("1024B/s"));
                    onoff1.SetAttribute("PacketSize", UintegerValue(packetSize));

                    ApplicationContainer app = onoff1.Install(nodeContainer.Get(source));

                    app.Start(Seconds(dataStart));
                    app.Stop(Seconds(dataEnd));
                }
            }
        }

        this->st.setSendedPackets((dataEnd - dataStart - 1) * num_source * (num_sink - 1));

        Simulator::Stop(Seconds(TotalTime));
        Simulator::Run();

        uint64_t sent = this->st.getSendedPackets();
        uint64_t received = this->st.getReceivedPackets();
        uint64_t lost = this->st.getPacketLost();
        double packetLoss = this->st.getPacketLoss();

        double deliveryRatio = 0.0;
        double overhead = 0.0;

        if (sent > 0)
        {
            deliveryRatio = ((double)received / (double)sent) * 100.0;
        }

        if (received > 0)
        {
            overhead = ((double)sent / (double)received);
        }

        std::cout << st << std::endl;

        dataset.Add(currentHopCount, packetLoss);

        csvFile << nWifis << ","
                << queueLength << ","
                << currentHopCount << ","
                << "HopCount" << ","
                << currentHopCount << ","
                << sent << ","
                << received << ","
                << lost << ","
                << packetLoss << ","
                << deliveryRatio << ","
                << overhead << "\n";

        Simulator::Destroy();
    }

    csvFile.close();

    plot.AddDataset(dataset);

    std::ofstream plotFile(plotFileName.c_str());
    plot.GenerateOutput(plotFile);
    plotFile.close();
}

std::ostream &operator<<(std::ostream &os, HopCountBenchmark &b)
{
    operator<<(os, (Benchmark &)b);
    os << "Max HopCount: " << b.maxHopCount << std::endl;
    os << "HopCount Step: " << b.hopCountStep << std::endl;
    return os;
}
