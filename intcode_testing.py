from helpers.intcode import IntcodeComputer







cpu = IntcodeComputer([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])
cpu.run_step()
print(cpu.disasm_running())