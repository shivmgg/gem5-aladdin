#!/usr/bin/env python
from __future__ import division
import re, sys

def usage():
    print '''\
Usage: %s [-E] [-F] [-d <db> ] [-g <get> ] [-h <host>] [-p]
       [-s <system>] [-r <runs> ] [-u <username>] <command> [command args]
''' % sys.argv[0]
    sys.exit(1)

def getopts(list, flags):
    import getopt
    try:
        opts, args = getopt.getopt(list, flags)
    except getopt.GetoptError:
        usage()

    return opts, args

def printval(name, value, invert = False):
    if invert and value != 0.0:
        value = 1 / value

    if value == (1e300*1e300):
        return

    if printval.mode == 'G':
        print '%s:    %g' % (name, value)
    elif printval.mode != 'F' and value > 1e6:
        print '%s:    %0.5e' % (name, value)
    else:
        print '%s:    %f' % (name, value)

printval.mode = 'G'

def unique(list):
    set = {}
    map(set.__setitem__, list, [])
    return set.keys()

def graphdata(runs, tag, label, value):
    import info
    configs = ['stx', 'ste', 'hte', 'htd', 'ocm', 'occ', 'ocp' ]
    benchmarks = [ 'm', 's' ]
    dmas = [ 'x', 'd', 'b' ]
    caches = [ '2', '4' ]
    checkpoints = [ '1' ]

    names = []
    for bench in benchmarks:
        for dma in dmas:
            for cache in caches:
                for cpt in checkpoints:
                    names.append([bench, dma, cache, cpt])

    for bench,dma,cache,cpt in names:
        base = '%s.%s.%s.%s' % (bench, dma, cache, cpt)
        fname = 'data/%s.%s.dat' % (tag, base)
        f = open(fname, 'w')
        print >>f, '#set TITLE = %s' % base
        print >>f, '#set xlbl = Configuration'
        print >>f, '#set ylbl = %s' % label
        print >>f, '#set sublabels = %s' % ' '.join(configs)

        for speed,freq in zip(['s', 'q'],['4GHz','10GHz']):
            print >>f, '"%s"' % freq,
            for conf in configs:
                name = '%s.%s.%s.%s.%s.%s' % (conf, bench, dma, speed, cache,
                                              cpt)
                run = info.source.allRunNames[name]
                info.display_run = run.run;
                val = float(value)
                if val == 1e300*1e300:
                    print >>f, 0.0,
                else:
                    print >>f, "%f" % val,
            print >>f
        f.close()

def printdata(runs, value, invert = False):
    import info
    for run in runs:
        info.display_run = run.run;
        val = float(value)
        printval(run.name, val)

class CommandException(Exception):
    pass

def commands(options, command, args):
    if command == 'database':
        if len(args) == 0: raise CommandException

        import dbinit
        mydb = dbinit.MyDB(options)

        if args[0] == 'drop':
            if len(args) > 2: raise CommandException
            mydb.admin()
            mydb.drop()
            if len(args) == 2 and args[1] == 'init':
                mydb.create()
                mydb.connect()
                mydb.populate()
            mydb.close()
            return

        if args[0] == 'init':
            if len(args) > 1: raise CommandException
            mydb.admin()
            mydb.create()
            mydb.connect()
            mydb.populate()
            mydb.close()
            return

        if args[0] == 'clean':
            if len(args) > 1: raise CommandException
            mydb.connect()
            mydb.clean()
            return

        raise CommandException

    import db, info
    info.source = db.Database()
    info.source.host = options.host
    info.source.db = options.db
    info.source.passwd = options.passwd
    info.source.user = options.user
    info.source.connect()
    info.source.update_dict(globals())

    system = info.source.__dict__[options.system]

    if type(options.get) is str:
        info.source.get = options.get

    if options.runs is None:
        runs = info.source.allRuns
    else:
        rx = re.compile(options.runs)
        runs = []
        for run in info.source.allRuns:
            if rx.match(run.name):
                runs.append(run)

    info.display_run = runs[0].run

    if command == 'runs':
        user = None
        opts, args = getopts(args, '-u')
        if len(args):
            raise CommandException
        for o,a in opts:
            if o == '-u':
                user = a
        info.source.listRuns(user)
        return

    if command == 'stats':
        if len(args) == 0:
            info.source.listStats()
        elif len(args) == 1:
            info.source.listStats(args[0])
        else:
            raise CommandException

        return

    if command == 'stat':
        if len(args) != 1:
            raise CommandException

        stats = info.source.getStat(args[0])
        for stat in stats:
            if options.graph:
                graphdata(runs, stat.name, stat.name, stat)
            else:
                if options.binned:
                    print 'kernel ticks'
                    stat.bins = 'kernel'
                    printdata(runs, stat)

                    print 'idle ticks'
                    stat.bins = 'idle'
                    printdata(runs, stat)

                    print 'user ticks'
                    stat.bins = 'user'
                    printdata(runs, stat)

                    print 'interrupt ticks'
                    stat.bins = 'user'
                    printdata(runs, stat)

                    print 'total ticks'

                stat.bins = None
                print stat.name
                printdata(runs, stat)
        return

    if command == 'bins':
        if len(args) == 0:
            info.source.listBins()
        elif len(args) == 1:
            info.source.listBins(args[0])
        else:
            raise CommandException

        return

    if command == 'formulas':
        if len(args) == 0:
            info.source.listFormulas()
        elif len(args) == 1:
            info.source.listFormulas(args[0])
        else:
            raise CommandException

        return

    if command == 'samples':
        if len(args):
            raise CommandException

        info.source.listTicks(runs)
        return

    if len(args):
        raise CommandException

    if command == 'usertime':
        import copy
        kernel = copy.copy(system.full_cpu.numCycles)
        kernel.bins = 'kernel'

        user = copy.copy(system.full_cpu.numCycles)
        user.bins = 'user'

        if options.graph:
            graphdata(runs, 'usertime', 'User Fraction',
                      user / system.full_cpu.numCycles)
        else:
            printdata(runs, user / system.full_cpu.numCycles)
        return

    if command == 'ticks':
        if options.binned:
            print 'kernel ticks'
            system.full_cpu.numCycles.bins = 'kernel'
            printdata(runs, system.full_cpu.numCycles)

            print 'idle ticks'
            system.full_cpu.numCycles.bins = 'idle'
            printdata(runs, system.full_cpu.numCycles)

            print 'user ticks'
            system.full_cpu.numCycles.bins = 'user'
            printdata(runs, system.full_cpu.numCycles)

            print 'total ticks'

        system.full_cpu.numCycles.bins = None
        printdata(runs, system.full_cpu.numCycles)
        return

    if command == 'packets':
        packets = system.tsunami.etherdev.rxPackets
        if options.graph:
            graphdata(runs, 'packets', 'Packets', packets)
        else:
            printdata(runs, packets)
        return

    if command == 'ppt' or command == 'tpp':
        ppt = system.tsunami.etherdev.rxPackets / sim_ticks
        printdata(runs, ppt, command == 'tpp')
        return

    if command == 'pps':
        pps = system.tsunami.etherdev.rxPackets / sim_seconds
        if options.graph:
            graphdata(runs, 'pps', 'Packets/s', pps)
        else:
            printdata(runs, pps)
        return

    if command == 'bpt' or command == 'tpb':
        bytes = system.tsunami.etherdev.rxBytes + system.tsunami.etherdev.txBytes
        bpt = bytes / sim_ticks * 8
        if options.graph:
            graphdata(runs, 'bpt', 'bps / Hz', bpt)
        else:
            printdata(runs, bpt, command == 'tpb')
        return

    if command == 'bptb' or command == 'tpbb':
        bytes = system.tsunami.etherdev.rxBytes + system.tsunami.etherdev.txBytes

        print 'kernel stats'
        bytes.bins = 'kernel'
        printdata(runs, bytes / ticks)

        print 'idle stats'
        bytes.bins = 'idle'
        printdata(runs, bytes / ticks)

        print 'user stats'
        bytes.bins = 'user'
        printdata(runs, bytes / ticks)

        return

    if command == 'bytes':
        stat = system.tsunami.etherdev.rxBytes + system.tsunami.etherdev.txBytes

        if options.binned:
            print '%s kernel stats' % stat.name
            stat.bins = 'kernel'
            printdata(runs, stat)

            print '%s idle stats' % stat.name
            stat.bins = 'idle'
            printdata(runs, stat)

            print '%s user stats' % stat.name
            stat.bins = 'user'
            printdata(runs, stat)

            print '%s total stats' % stat.name
            stat.bins = None

        printdata(runs, stat)
        return

    if command == 'rxbps':
        gbps = system.tsunami.etherdev.rxBandwidth / 1e9
        if options.graph:
            graphdata(runs, 'rxbps', 'Bandwidth (Gbps)',  gbps)
        else:
            printdata(runs, gbps)
        return

    if command == 'txbps':
        gbps = system.tsunami.etherdev.txBandwidth / 1e9
        if options.graph:
            graphdata(runs, 'txbps', 'Bandwidth (Gbps)',  gbps)
        else:
            printdata(runs, gbps)
        return

    if command == 'bps':
        rxbps = system.tsunami.etherdev.rxBandwidth
        txbps = system.tsunami.etherdev.txBandwidth
        gbps = (rxbps + txbps) / 1e9
        if options.graph:
            graphdata(runs, 'bps', 'Bandwidth (Gbps)',  gbps)
        else:
            printdata(runs, gbps)
        return

    if command == 'misses':
        stat = system.L2.overall_mshr_misses
        if options.binned:
            print '%s kernel stats' % stat.name
            stat.bins = 'kernel'
            printdata(runs, stat)

            print '%s idle stats' % stat.name
            stat.bins = 'idle'
            printdata(runs, stat)

            print '%s user stats' % stat.name
            stat.bins = 'user'
            printdata(runs, stat)

            print '%s total stats' % stat.name

        stat.bins = None
        if options.graph:
            graphdata(runs, 'misses', 'Overall MSHR Misses', stat)
        else:
            printdata(runs, stat)
        return

    if command == 'mpkb':
        misses = system.L2.overall_mshr_misses
        rxbytes = system.tsunami.etherdev.rxBytes
        txbytes = system.tsunami.etherdev.txBytes

        if options.binned:
            print 'mpkb kernel stats'
            misses.bins = 'kernel'
            mpkb = misses / ((rxbytes + txbytes) / 1024)
            printdata(runs, mpkb)

            print 'mpkb idle stats'
            misses.bins = 'idle'
            mpkb = misses / ((rxbytes + txbytes) / 1024)
            printdata(runs, mpkb)

            print 'mpkb user stats'
            misses.bins = 'user'
            mpkb = misses / ((rxbytes + txbytes) / 1024)
            printdata(runs, mpkb)

            print 'mpkb total stats'

        mpkb = misses / ((rxbytes + txbytes) / 1024)
        misses.bins = None
        if options.graph:
            graphdata(runs, 'mpkb', 'Misses / KB',  mpkb)
        else:
            printdata(runs, mpkb)
        return

    if command == 'execute':
        printdata(runs, system.full_cpu.ISSUE__count)
        return

    if command == 'commit':
        printdata(runs, system.full_cpu.COM__count)
        return

    if command == 'fetch':
        printdata(runs, system.full_cpu.FETCH__count)
        return

    if command == 'bpp':
        ed = system.tsunami.etherdev
        bpp = (ed.rxBytes + ed.txBytes) / (ed.rxPackets + ed.txPackets)
        if options.graph:
            graphdata(runs, 'bpp', 'Bytes / Packet',  bpp)
        else:
            printdata(runs, bpp)
        return

    if command == 'rxbpp':
        bpp = system.tsunami.etherdev.rxBytes / system.tsunami.etherdev.rxPackets
        if options.graph:
            graphdata(runs, 'rxbpp', 'Receive Bytes / Packet',  bpp)
        else:
            printdata(runs, bpp)
        return

    if command == 'txbpp':
        bpp = system.tsunami.etherdev.txBytes / system.tsunami.etherdev.txPackets
        if options.graph:
            graphdata(runs, 'txbpp', 'Transmit Bytes / Packet',  bpp)
        else:
            printdata(runs, bpp)
        return

    if command == 'rtp':
        rtp = system.tsunami.etherdev.rxPackets / system.tsunami.etherdev.txPackets
        if options.graph:
            graphdata(runs, 'rtp', 'rxPackets / txPackets',  rtp)
        else:
            printdata(runs, rtp)
        return

    if command == 'rtb':
        rtb = system.tsunami.etherdev.rxBytes / system.tsunami.etherdev.txBytes
        if options.graph:
            graphdata(runs, 'rtb', 'rxBytes / txBytes',  rtb)
        else:
            printdata(runs, rtb)
        return

    raise CommandException


class Options: pass

if __name__ == '__main__':
    import getpass

    options = Options()
    options.host = 'zizzer.pool'
    options.db = None
    options.passwd = ''
    options.user = getpass.getuser()
    options.runs = None
    options.system = 'client'
    options.get = None
    options.binned = False
    options.graph = False

    opts, args = getopts(sys.argv[1:], '-BEFGd:g:h:pr:s:u:')
    for o,a in opts:
        if o == '-B':
            options.binned = True
        if o == '-E':
            printval.mode = 'E'
        if o == '-F':
            printval.mode = 'F'
        if o == '-G':
            options.graph = True;
        if o == '-d':
            options.db = a
        if o == '-g':
            options.get = a
        if o == '-h':
            options.host = a
        if o == '-p':
            options.passwd = getpass.getpass()
        if o == '-r':
            options.runs = a
        if o == '-u':
            options.user = a
        if o == '-s':
            options.system = a

    if len(args) == 0:
        usage()

    command = args[0]
    args = args[1:]

    try:
        commands(options, command, args)
    except CommandException:
        usage()
