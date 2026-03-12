import os
import os.path as osp

from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

ROOT = osp.dirname(osp.abspath(__file__))


def _nvcc_arch_flags() -> list[str]:
    arch_list = os.environ.get("GAUSSIANPRO_CUDA_ARCH_LIST", "86;89")
    flags: list[str] = ["-O3"]
    for arch in arch_list.split(";"):
        arch = arch.strip()
        if not arch:
            continue
        flags.append(f"-gencode=arch=compute_{arch},code=sm_{arch}")
    return flags

setup(
    name='gaussianpro',
    ext_modules=[
        CUDAExtension('gaussianpro', 
            sources=[
                'PatchMatch.cpp', 
                'Propagation.cu',
                'pro.cpp'
            ],
            extra_compile_args={
                'cxx': ['-O3'],
                'nvcc': _nvcc_arch_flags(),
            }),
    ],
    cmdclass={ 'build_ext' : BuildExtension }
)
