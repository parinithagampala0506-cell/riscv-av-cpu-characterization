import os
import argparse
import m5
from m5.objects import *

parser = argparse.ArgumentParser()
parser.add_argument("--cmd", required=True)
parser.add_argument("--cpu", choices=["minor", "o3_2", "o3_4"], default="o3_2")
parser.add_argument("--l1-size", choices=["16KiB", "32KiB", "64KiB"], default="32KiB")
args = parser.parse_args()


binary = os.path.abspath(args.cmd)

class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 8
    tgts_per_mshr = 16

class L2Cache(Cache):
    size = "256KiB"
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]

if args.cpu == "minor":
    system.cpu = RiscvMinorCPU()
else:
    system.cpu = RiscvO3CPU()
    width = 2 if args.cpu == "o3_2" else 4
    system.cpu.fetchWidth = width
    system.cpu.decodeWidth = width
    system.cpu.renameWidth = width
    system.cpu.dispatchWidth = width
    system.cpu.issueWidth = width
    system.cpu.wbWidth = width
    system.cpu.commitWidth = width
    system.cpu.backComSize = 10
    system.cpu.forwardComSize = 10
system.cpu.clk_domain = system.clk_domain
system.cpu.createInterruptController()

system.cpu.icache = L1Cache()
system.cpu.icache.size = args.l1_size

system.cpu.dcache = L1Cache()
system.cpu.dcache.size = args.l1_size

system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port

system.l2bus = L2XBar()
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports

system.l2cache = L2Cache()
system.l2cache.cpu_side = system.l2bus.mem_side_ports

system.membus = SystemXBar()
system.l2cache.mem_side = system.membus.cpu_side_ports
system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.workload = SEWorkload.init_compatible(binary)
process = Process()
process.cmd = [binary]
process.output = os.path.abspath("scenario_stdout.txt")
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

print("CPU model:", args.cpu)
print("L1 instruction cache:", args.l1_size)
print("L1 data cache:", args.l1_size)
print("L2 cache: 256KiB")
print("Clock: 1GHz")
print("Starting simulation")

event = m5.simulate()

print("Simulation ended at tick:", m5.curTick())
print("Exit cause:", event.getCause())
