## Setting up Hail from source
I found that the easiest way to allow hail to use more memory is to build it from the source. I'll describe the process, but you can also take a look at the docs here : https://hail.is/docs/0.2/getting_started_developing.html.  To install hail you will need the following:
* Java 8 JDK 
* Python > 3.6
* Scala 2.12
* Spark 3.1.1
* A recent C and a C++ compiler, GCC 5.0, LLVM 3.4, or later versions of either suffice.
* BLAS and LAPACK.
* The LZ4 library