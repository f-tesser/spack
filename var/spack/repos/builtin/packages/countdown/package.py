# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Countdown(CMakePackage, CudaPackage):

    """COUNTDOWN is a tool for identifying and automatically reducing the power
    consumption of the computing elements, during communication and
    synchronization primitives, filtering out phases which would detriment the
    time to solution of the application. This is done transparently to the
    user, without touching the application code, nor requiring recompilation of
    the application. We tested our methodology in a production Tier-0 system,
    on a production application with production datasets, which can scale up to
    3.5K cores.
    """

    homepage = "https://github.com/EEESlab/countdown"

    # ----------------------------------------------------------------------- #
    # The following two lines need the installation command: \"spack install
    # --no-checksum countdown\", because by default, Spack will only install a
    # tarball package if it has a checksum, and that checksum matches.

    # url      = "https://github.com/EEESlab/countdown/archive/refs/" \
    #            "heads/master.tar.gz"
    # ----------------------------------------------------------------------- #

    # ----------------------------------------------------------------------- #
    # The following two lines need the installation command: \"spack install
    # countdown\".

    git = "https://github.com/EEESlab/countdown.git"
    branch = "master"
    # ----------------------------------------------------------------------- #

    maintainers = [
        'f-tesser',
        'danielecesarini'
    ]

    version('1.0.0')

    depends_on('cmake@3.0.0:', type='build')
    depends_on('hwloc', type='link')
    depends_on('mpi@3.0.0:', type='link')

    variant(
        'disable_profiling_mpi',
        default='False',
        multi=False,
        description='Disable the instrumentation of MPI '
                    'functions'
    )
    variant(
        'disable_p2p_mpi',
        default='False',
        multi=False,

        # -------------------------------------------------------------------  #
        # The following line will create variant of type \"String\", instead of
        # \"Boolean\", which is the one needed by us, to set \"True\" or
        # \"False\" values, from \"spack install...\" line, from command line.
        # Otherwise, an error similar to \"Error: invalid values for variant
        # "cntd_disable_accessory_mpi" in package "countdown": [False]\" would
        # break the compilation, not recognising \"False\" as a correct value
        # a \"String\" variant.

        # values = ('False', 'True')                        ,
        # -------------------------------------------------------------------  #

        description='Disable the instrumentation of P2P MPI '
                    'functions'
    )
    variant(
        'disable_accessory_mpi',
        default='False',
        multi=False,
        description='Disable the instrumentation of accessory MPI '
                    'functions, focusing only on collective'
    )
    variant(
        'debug_mpi',
        default='False',
        multi=False,
        description='Enable the debug prints on MPI functions'
    )

    def cmake_args(self):
        # spec = self.spec

        sdfv = self.define_from_variant
        cmake_args = [
            sdfv('CNTD_ENABLE_CUDA', 'cntd_enable_cuda'),
            sdfv(
                'CNTD_DISABLE_PROFILING_MPI',
                'cntd_disable_profiling_mpi'
            ),
            sdfv('CNTD_DISABLE_P2P_MPI', 'cntd_disable_p2p_mpi'),
            sdfv(
                'CNTD_DISABLE_ACCESSORY_MPI',
                'cntd_disable_accessory_mpi'
            ),
            sdfv('CNTD_ENABLE_DEBUG_MPI', 'cntd_enable_debug_mpi')
        ]

        # -------------------------------------------------------------------  #
        # cmake_args = [
        #         '-DCNTD_ENABLE_CUDA:BOOL=OFF'          ,
        #         '-DCNTD_DISABLE_PROFILING_MPI:BOOL=OFF',
        #         '-DCNTD_DISABLE_P2P_MPI:BOOL=OFF'      ,
        #         '-DCNTD_DISABLE_ACCESSORY_MPI:BOOL=OFF',
        #         '-DCNTD_ENABLE_DEBUG_MPI:BOOL=OFF'
        # ]
        # -------------------------------------------------------------------  #

        return cmake_args
