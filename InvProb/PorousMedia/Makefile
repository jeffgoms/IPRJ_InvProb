SHELL = sh

serial_corner:	clean
		gmsh -2 -bin src/Simplegeom2.geo
		/data2/MultiFluids/ICFERST/bin/icferst cornerswells4.mpml

parallel_corner:clean
		gmsh -2 -bin src/Simplegeom2.geo
		/data2/MultiFluids/ICFERST/bin/fldecomp -n 8 -m gmsh src/Simplegeom2
		mpiexec -n 8 /data2/MultiFluids/ICFERST/bin/icferst cornerswells4.mpml

clean:
	rm -f *.vtu *.stat src/*halo src/*msh
	rm -f log
	rm -fr OneInjectOneProdt* OneInjectThreeProdts*
